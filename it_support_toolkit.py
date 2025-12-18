#!/usr/bin/env python3
"""
IT Support Automation Toolkit
A comprehensive tool for automating common IT support health checks and reporting.
"""

import psutil
import platform
import socket
import csv
import json
from datetime import datetime
from pathlib import Path
import subprocess
import sys


class ITSupportToolkit:
    """Main class for IT support automation tasks."""
    
    def __init__(self):
        self.report_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'hostname': socket.gethostname(),
            'os': f"{platform.system()} {platform.release()}",
            'checks': {}
        }
    
    def check_disk_space(self):
        """Check disk space usage for all partitions."""
        print("\n=== DISK SPACE CHECK ===")
        disk_info = []
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partition_data = {
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'filesystem': partition.fstype,
                    'total_gb': round(usage.total / (1024**3), 2),
                    'used_gb': round(usage.used / (1024**3), 2),
                    'free_gb': round(usage.free / (1024**3), 2),
                    'percent_used': usage.percent
                }
                disk_info.append(partition_data)
                
                status = "⚠️ WARNING" if usage.percent > 80 else "✓ OK"
                print(f"{status} {partition.device} ({partition.mountpoint})")
                print(f"   Total: {partition_data['total_gb']} GB | "
                      f"Used: {partition_data['used_gb']} GB ({usage.percent}%) | "
                      f"Free: {partition_data['free_gb']} GB")
            except PermissionError:
                continue
        
        self.report_data['checks']['disk_space'] = disk_info
        return disk_info
    
    def check_cpu_ram(self):
        """Check CPU and RAM usage."""
        print("\n=== CPU & RAM CHECK ===")
        
        # CPU Information
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        
        cpu_data = {
            'usage_percent': cpu_percent,
            'physical_cores': cpu_count,
            'logical_cores': cpu_count_logical,
            'current_freq_mhz': round(cpu_freq.current, 2) if cpu_freq else 'N/A',
            'max_freq_mhz': round(cpu_freq.max, 2) if cpu_freq else 'N/A'
        }
        
        cpu_status = "⚠️ WARNING" if cpu_percent > 80 else "✓ OK"
        print(f"{cpu_status} CPU Usage: {cpu_percent}%")
        print(f"   Cores: {cpu_count} physical, {cpu_count_logical} logical")
        if cpu_freq:
            print(f"   Frequency: {cpu_data['current_freq_mhz']} MHz "
                  f"(Max: {cpu_data['max_freq_mhz']} MHz)")
        
        # RAM Information
        ram = psutil.virtual_memory()
        ram_data = {
            'total_gb': round(ram.total / (1024**3), 2),
            'available_gb': round(ram.available / (1024**3), 2),
            'used_gb': round(ram.used / (1024**3), 2),
            'percent_used': ram.percent
        }
        
        ram_status = "⚠️ WARNING" if ram.percent > 80 else "✓ OK"
        print(f"\n{ram_status} RAM Usage: {ram.percent}%")
        print(f"   Total: {ram_data['total_gb']} GB | "
              f"Used: {ram_data['used_gb']} GB | "
              f"Available: {ram_data['available_gb']} GB")
        
        self.report_data['checks']['cpu'] = cpu_data
        self.report_data['checks']['ram'] = ram_data
        return cpu_data, ram_data
    
    def list_users(self):
        """List all users currently logged in."""
        print("\n=== LOGGED IN USERS ===")
        users_info = []
        
        users = psutil.users()
        if not users:
            print("No users currently logged in.")
            self.report_data['checks']['users'] = []
            return []
        
        for user in users:
            user_data = {
                'name': user.name,
                'terminal': user.terminal,
                'host': user.host,
                'started': datetime.fromtimestamp(user.started).strftime('%Y-%m-%d %H:%M:%S')
            }
            users_info.append(user_data)
            print(f"✓ User: {user.name}")
            print(f"   Terminal: {user.terminal} | Host: {user.host} | "
                  f"Since: {user_data['started']}")
        
        self.report_data['checks']['users'] = users_info
        return users_info
    
    def check_password_expiry(self):
        """Check password expiry for system users (Linux only)."""
        print("\n=== PASSWORD EXPIRY CHECK ===")
        
        if platform.system() != 'Linux':
            print("⚠️  Password expiry check only available on Linux systems.")
            self.report_data['checks']['password_expiry'] = {'error': 'Not available on this OS'}
            return None
        
        password_info = []
        
        try:
            # Get list of users from /etc/passwd
            result = subprocess.run(['cat', '/etc/passwd'], 
                                  capture_output=True, text=True, check=True)
            
            for line in result.stdout.split('\n'):
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split(':')
                if len(parts) < 7:
                    continue
                
                username = parts[0]
                # Skip system users (UID < 1000)
                try:
                    uid = int(parts[2])
                    if uid < 1000:
                        continue
                except ValueError:
                    continue
                
                # Check password expiry using chage
                try:
                    chage_result = subprocess.run(['sudo', 'chage', '-l', username],
                                                capture_output=True, text=True, 
                                                timeout=5)
                    
                    if chage_result.returncode == 0:
                        expiry_date = 'N/A'
                        for line in chage_result.stdout.split('\n'):
                            if 'Password expires' in line:
                                expiry_date = line.split(':', 1)[1].strip()
                                break
                        
                        user_data = {
                            'username': username,
                            'password_expires': expiry_date
                        }
                        password_info.append(user_data)
                        
                        status = "⚠️" if expiry_date != 'never' and expiry_date != 'N/A' else "✓"
                        print(f"{status} {username}: Password expires {expiry_date}")
                except subprocess.TimeoutExpired:
                    continue
                except Exception:
                    continue
        
        except Exception as e:
            print(f"⚠️  Could not check password expiry: {str(e)}")
            print("   Note: This check may require sudo privileges.")
        
        self.report_data['checks']['password_expiry'] = password_info
        return password_info
    
    def check_network_connectivity(self):
        """Check network connectivity to common services."""
        print("\n=== NETWORK CONNECTIVITY CHECK ===")
        
        # Get network interfaces
        network_info = {
            'interfaces': [],
            'connectivity_tests': []
        }
        
        # List network interfaces
        print("Network Interfaces:")
        interfaces = psutil.net_if_addrs()
        for interface_name, addresses in interfaces.items():
            for addr in addresses:
                if addr.family == socket.AF_INET:  # IPv4
                    interface_data = {
                        'interface': interface_name,
                        'ip_address': addr.address,
                        'netmask': addr.netmask
                    }
                    network_info['interfaces'].append(interface_data)
                    print(f"✓ {interface_name}: {addr.address} (Netmask: {addr.netmask})")
        
        # Test connectivity to common services
        print("\nConnectivity Tests:")
        test_hosts = [
            ('8.8.8.8', 53, 'Google DNS'),
            ('1.1.1.1', 53, 'Cloudflare DNS'),
            ('google.com', 80, 'Google HTTP'),
        ]
        
        for host, port, description in test_hosts:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((host, port))
                sock.close()
                
                is_reachable = result == 0
                test_data = {
                    'host': host,
                    'port': port,
                    'description': description,
                    'reachable': is_reachable
                }
                network_info['connectivity_tests'].append(test_data)
                
                status = "✓ OK" if is_reachable else "✗ FAILED"
                print(f"{status} {description} ({host}:{port})")
            except Exception as e:
                test_data = {
                    'host': host,
                    'port': port,
                    'description': description,
                    'reachable': False,
                    'error': str(e)
                }
                network_info['connectivity_tests'].append(test_data)
                print(f"✗ FAILED {description} ({host}:{port}) - {str(e)}")
        
        self.report_data['checks']['network'] = network_info
        return network_info
    
    def export_report_txt(self, filename=None):
        """Export report to text file."""
        if filename is None:
            filename = f"it_support_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = Path(filename)
        
        with open(filepath, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("IT SUPPORT SYSTEM HEALTH CHECK REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {self.report_data['timestamp']}\n")
            f.write(f"Hostname: {self.report_data['hostname']}\n")
            f.write(f"Operating System: {self.report_data['os']}\n")
            f.write("\n" + "=" * 60 + "\n\n")
            
            # Disk Space
            if 'disk_space' in self.report_data['checks']:
                f.write("DISK SPACE\n")
                f.write("-" * 60 + "\n")
                for disk in self.report_data['checks']['disk_space']:
                    f.write(f"Device: {disk['device']} ({disk['mountpoint']})\n")
                    f.write(f"  Filesystem: {disk['filesystem']}\n")
                    f.write(f"  Total: {disk['total_gb']} GB\n")
                    f.write(f"  Used: {disk['used_gb']} GB ({disk['percent_used']}%)\n")
                    f.write(f"  Free: {disk['free_gb']} GB\n\n")
            
            # CPU & RAM
            if 'cpu' in self.report_data['checks']:
                f.write("CPU INFORMATION\n")
                f.write("-" * 60 + "\n")
                cpu = self.report_data['checks']['cpu']
                f.write(f"Usage: {cpu['usage_percent']}%\n")
                f.write(f"Physical Cores: {cpu['physical_cores']}\n")
                f.write(f"Logical Cores: {cpu['logical_cores']}\n")
                f.write(f"Current Frequency: {cpu['current_freq_mhz']} MHz\n\n")
            
            if 'ram' in self.report_data['checks']:
                f.write("RAM INFORMATION\n")
                f.write("-" * 60 + "\n")
                ram = self.report_data['checks']['ram']
                f.write(f"Total: {ram['total_gb']} GB\n")
                f.write(f"Used: {ram['used_gb']} GB ({ram['percent_used']}%)\n")
                f.write(f"Available: {ram['available_gb']} GB\n\n")
            
            # Users
            if 'users' in self.report_data['checks']:
                f.write("LOGGED IN USERS\n")
                f.write("-" * 60 + "\n")
                if self.report_data['checks']['users']:
                    for user in self.report_data['checks']['users']:
                        f.write(f"User: {user['name']}\n")
                        f.write(f"  Terminal: {user['terminal']}\n")
                        f.write(f"  Host: {user['host']}\n")
                        f.write(f"  Login Time: {user['started']}\n\n")
                else:
                    f.write("No users currently logged in.\n\n")
            
            # Password Expiry
            if 'password_expiry' in self.report_data['checks']:
                f.write("PASSWORD EXPIRY\n")
                f.write("-" * 60 + "\n")
                pwd_exp = self.report_data['checks']['password_expiry']
                if isinstance(pwd_exp, list) and pwd_exp:
                    for user in pwd_exp:
                        f.write(f"{user['username']}: {user['password_expires']}\n")
                else:
                    f.write("Password expiry information not available.\n")
                f.write("\n")
            
            # Network
            if 'network' in self.report_data['checks']:
                f.write("NETWORK INFORMATION\n")
                f.write("-" * 60 + "\n")
                net = self.report_data['checks']['network']
                
                f.write("Network Interfaces:\n")
                for iface in net.get('interfaces', []):
                    f.write(f"  {iface['interface']}: {iface['ip_address']} "
                           f"(Netmask: {iface['netmask']})\n")
                
                f.write("\nConnectivity Tests:\n")
                for test in net.get('connectivity_tests', []):
                    status = "OK" if test['reachable'] else "FAILED"
                    f.write(f"  {test['description']} ({test['host']}:{test['port']}): {status}\n")
                f.write("\n")
            
            f.write("=" * 60 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 60 + "\n")
        
        print(f"\n✓ Report exported to: {filepath.absolute()}")
        return str(filepath.absolute())
    
    def export_report_csv(self, filename=None):
        """Export report to CSV file."""
        if filename is None:
            filename = f"it_support_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = Path(filename)
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header information
            writer.writerow(['IT Support System Health Check Report'])
            writer.writerow(['Generated', self.report_data['timestamp']])
            writer.writerow(['Hostname', self.report_data['hostname']])
            writer.writerow(['Operating System', self.report_data['os']])
            writer.writerow([])
            
            # Disk Space
            if 'disk_space' in self.report_data['checks']:
                writer.writerow(['DISK SPACE'])
                writer.writerow(['Device', 'Mountpoint', 'Filesystem', 'Total (GB)', 
                               'Used (GB)', 'Free (GB)', 'Used (%)'])
                for disk in self.report_data['checks']['disk_space']:
                    writer.writerow([
                        disk['device'], disk['mountpoint'], disk['filesystem'],
                        disk['total_gb'], disk['used_gb'], disk['free_gb'],
                        disk['percent_used']
                    ])
                writer.writerow([])
            
            # CPU
            if 'cpu' in self.report_data['checks']:
                writer.writerow(['CPU INFORMATION'])
                writer.writerow(['Metric', 'Value'])
                cpu = self.report_data['checks']['cpu']
                writer.writerow(['Usage (%)', cpu['usage_percent']])
                writer.writerow(['Physical Cores', cpu['physical_cores']])
                writer.writerow(['Logical Cores', cpu['logical_cores']])
                writer.writerow(['Current Frequency (MHz)', cpu['current_freq_mhz']])
                writer.writerow([])
            
            # RAM
            if 'ram' in self.report_data['checks']:
                writer.writerow(['RAM INFORMATION'])
                writer.writerow(['Metric', 'Value'])
                ram = self.report_data['checks']['ram']
                writer.writerow(['Total (GB)', ram['total_gb']])
                writer.writerow(['Used (GB)', ram['used_gb']])
                writer.writerow(['Available (GB)', ram['available_gb']])
                writer.writerow(['Used (%)', ram['percent_used']])
                writer.writerow([])
            
            # Users
            if 'users' in self.report_data['checks']:
                writer.writerow(['LOGGED IN USERS'])
                writer.writerow(['Username', 'Terminal', 'Host', 'Login Time'])
                for user in self.report_data['checks']['users']:
                    writer.writerow([user['name'], user['terminal'], 
                                   user['host'], user['started']])
                writer.writerow([])
            
            # Password Expiry
            if 'password_expiry' in self.report_data['checks']:
                writer.writerow(['PASSWORD EXPIRY'])
                writer.writerow(['Username', 'Expiry Date'])
                pwd_exp = self.report_data['checks']['password_expiry']
                if isinstance(pwd_exp, list):
                    for user in pwd_exp:
                        writer.writerow([user['username'], user['password_expires']])
                writer.writerow([])
            
            # Network
            if 'network' in self.report_data['checks']:
                writer.writerow(['NETWORK INTERFACES'])
                writer.writerow(['Interface', 'IP Address', 'Netmask'])
                net = self.report_data['checks']['network']
                for iface in net.get('interfaces', []):
                    writer.writerow([iface['interface'], iface['ip_address'], 
                                   iface['netmask']])
                writer.writerow([])
                
                writer.writerow(['CONNECTIVITY TESTS'])
                writer.writerow(['Description', 'Host', 'Port', 'Status'])
                for test in net.get('connectivity_tests', []):
                    status = 'OK' if test['reachable'] else 'FAILED'
                    writer.writerow([test['description'], test['host'], 
                                   test['port'], status])
        
        print(f"✓ Report exported to: {filepath.absolute()}")
        return str(filepath.absolute())
    
    def export_report_json(self, filename=None):
        """Export report to JSON file."""
        if filename is None:
            filename = f"it_support_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = Path(filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.report_data, f, indent=2)
        
        print(f"✓ Report exported to: {filepath.absolute()}")
        return str(filepath.absolute())
    
    def run_all_checks(self, export_format='txt'):
        """Run all health checks and export report."""
        print("=" * 60)
        print("IT SUPPORT AUTOMATION TOOLKIT")
        print("=" * 60)
        print(f"Hostname: {self.report_data['hostname']}")
        print(f"OS: {self.report_data['os']}")
        print(f"Timestamp: {self.report_data['timestamp']}")
        
        self.check_disk_space()
        self.check_cpu_ram()
        self.list_users()
        self.check_network_connectivity()
        self.check_password_expiry()
        
        print("\n" + "=" * 60)
        print("EXPORTING REPORT")
        print("=" * 60)
        
        if export_format.lower() == 'txt':
            self.export_report_txt()
        elif export_format.lower() == 'csv':
            self.export_report_csv()
        elif export_format.lower() == 'json':
            self.export_report_json()
        elif export_format.lower() == 'all':
            self.export_report_txt()
            self.export_report_csv()
            self.export_report_json()
        else:
            print(f"⚠️  Unknown format: {export_format}. Using TXT.")
            self.export_report_txt()


def main():
    """Main entry point for the toolkit."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='IT Support Automation Toolkit - System Health Checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run all checks, export to TXT
  %(prog)s --format csv       # Run all checks, export to CSV
  %(prog)s --format all       # Export to TXT, CSV, and JSON
  %(prog)s --disk             # Run only disk space check
  %(prog)s --cpu              # Run only CPU/RAM check
  %(prog)s --users            # List logged in users only
  %(prog)s --network          # Check network connectivity only
  %(prog)s --password         # Check password expiry only
        """
    )
    
    parser.add_argument('--format', '-f', 
                       choices=['txt', 'csv', 'json', 'all'],
                       default='txt',
                       help='Export format (default: txt)')
    
    parser.add_argument('--disk', action='store_true',
                       help='Run only disk space check')
    parser.add_argument('--cpu', action='store_true',
                       help='Run only CPU/RAM check')
    parser.add_argument('--users', action='store_true',
                       help='List logged in users only')
    parser.add_argument('--network', action='store_true',
                       help='Check network connectivity only')
    parser.add_argument('--password', action='store_true',
                       help='Check password expiry only')
    
    parser.add_argument('--output', '-o',
                       help='Output filename (without extension)')
    
    args = parser.parse_args()
    
    toolkit = ITSupportToolkit()
    
    # Check if any specific check is requested
    specific_checks = args.disk or args.cpu or args.users or args.network or args.password
    
    if not specific_checks:
        # Run all checks
        toolkit.run_all_checks(export_format=args.format)
    else:
        # Run specific checks
        print("=" * 60)
        print("IT SUPPORT AUTOMATION TOOLKIT")
        print("=" * 60)
        print(f"Hostname: {toolkit.report_data['hostname']}")
        print(f"OS: {toolkit.report_data['os']}")
        
        if args.disk:
            toolkit.check_disk_space()
        if args.cpu:
            toolkit.check_cpu_ram()
        if args.users:
            toolkit.list_users()
        if args.network:
            toolkit.check_network_connectivity()
        if args.password:
            toolkit.check_password_expiry()
        
        # Export results
        print("\n" + "=" * 60)
        print("EXPORTING REPORT")
        print("=" * 60)
        
        if args.output:
            if args.format == 'txt':
                toolkit.export_report_txt(f"{args.output}.txt")
            elif args.format == 'csv':
                toolkit.export_report_csv(f"{args.output}.csv")
            elif args.format == 'json':
                toolkit.export_report_json(f"{args.output}.json")
            elif args.format == 'all':
                toolkit.export_report_txt(f"{args.output}.txt")
                toolkit.export_report_csv(f"{args.output}.csv")
                toolkit.export_report_json(f"{args.output}.json")
        else:
            if args.format == 'txt':
                toolkit.export_report_txt()
            elif args.format == 'csv':
                toolkit.export_report_csv()
            elif args.format == 'json':
                toolkit.export_report_json()
            elif args.format == 'all':
                toolkit.export_report_txt()
                toolkit.export_report_csv()
                toolkit.export_report_json()


if __name__ == '__main__':
    main()
