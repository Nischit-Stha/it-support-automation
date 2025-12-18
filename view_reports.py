#!/usr/bin/env python3
"""
Report Viewer - Simple utility to view generated IT support reports
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime


def list_reports():
    """List all available report files."""
    report_files = {
        'txt': [],
        'csv': [],
        'json': []
    }
    
    current_dir = Path('.')
    
    for file in current_dir.glob('it_support_report_*'):
        if file.suffix == '.txt':
            report_files['txt'].append(file)
        elif file.suffix == '.csv':
            report_files['csv'].append(file)
        elif file.suffix == '.json':
            report_files['json'].append(file)
    
    return report_files


def display_report_summary(report_files):
    """Display a summary of available reports."""
    print("=" * 60)
    print("AVAILABLE IT SUPPORT REPORTS")
    print("=" * 60)
    
    all_reports = []
    for format_type, files in report_files.items():
        for file in files:
            stat = file.stat()
            modified = datetime.fromtimestamp(stat.st_mtime)
            all_reports.append({
                'file': file,
                'format': format_type.upper(),
                'size': stat.st_size,
                'modified': modified
            })
    
    if not all_reports:
        print("\nNo reports found in current directory.")
        print("Run the toolkit first: python it_support_toolkit.py")
        return None
    
    # Sort by modified time (newest first)
    all_reports.sort(key=lambda x: x['modified'], reverse=True)
    
    print(f"\nFound {len(all_reports)} report(s):\n")
    
    for idx, report in enumerate(all_reports, 1):
        size_kb = report['size'] / 1024
        print(f"{idx}. {report['file'].name}")
        print(f"   Format: {report['format']} | "
              f"Size: {size_kb:.2f} KB | "
              f"Modified: {report['modified'].strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    return all_reports


def view_txt_report(filepath):
    """View a text report."""
    print("\n" + "=" * 60)
    print(f"VIEWING: {filepath.name}")
    print("=" * 60 + "\n")
    
    with open(filepath, 'r') as f:
        print(f.read())


def view_json_report(filepath):
    """View a JSON report in formatted style."""
    print("\n" + "=" * 60)
    print(f"VIEWING: {filepath.name}")
    print("=" * 60 + "\n")
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    print(f"Timestamp: {data['timestamp']}")
    print(f"Hostname: {data['hostname']}")
    print(f"OS: {data['os']}")
    print()
    
    if 'disk_space' in data['checks']:
        print("DISK SPACE:")
        for disk in data['checks']['disk_space']:
            print(f"  {disk['device']} ({disk['mountpoint']}): "
                  f"{disk['used_gb']} GB / {disk['total_gb']} GB "
                  f"({disk['percent_used']}%)")
        print()
    
    if 'cpu' in data['checks']:
        cpu = data['checks']['cpu']
        print(f"CPU: {cpu['usage_percent']}% usage, "
              f"{cpu['physical_cores']} cores")
        print()
    
    if 'ram' in data['checks']:
        ram = data['checks']['ram']
        print(f"RAM: {ram['used_gb']} GB / {ram['total_gb']} GB "
              f"({ram['percent_used']}%)")
        print()
    
    if 'users' in data['checks'] and data['checks']['users']:
        print("LOGGED IN USERS:")
        for user in data['checks']['users']:
            print(f"  {user['name']} on {user['terminal']} "
                  f"since {user['started']}")
        print()


def view_csv_report(filepath):
    """View a CSV report."""
    print("\n" + "=" * 60)
    print(f"VIEWING: {filepath.name}")
    print("=" * 60 + "\n")
    
    with open(filepath, 'r') as f:
        # Read CSV and display in a simple format
        import csv
        reader = csv.reader(f)
        
        for row in reader:
            if row:  # Skip empty rows
                print(' | '.join(row))


def compare_reports(report1, report2):
    """Compare two JSON reports to show changes."""
    print("\n" + "=" * 60)
    print("COMPARING REPORTS")
    print("=" * 60)
    
    if not (report1.suffix == '.json' and report2.suffix == '.json'):
        print("\n⚠️  Comparison only works with JSON reports.")
        return
    
    with open(report1, 'r') as f:
        data1 = json.load(f)
    
    with open(report2, 'r') as f:
        data2 = json.load(f)
    
    print(f"\nReport 1: {data1['timestamp']}")
    print(f"Report 2: {data2['timestamp']}")
    print()
    
    # Compare RAM
    if 'ram' in data1['checks'] and 'ram' in data2['checks']:
        ram1 = data1['checks']['ram']['percent_used']
        ram2 = data2['checks']['ram']['percent_used']
        diff = ram2 - ram1
        arrow = "↑" if diff > 0 else "↓" if diff < 0 else "→"
        print(f"RAM Usage: {ram1}% → {ram2}% ({arrow} {abs(diff):.1f}%)")
    
    # Compare CPU
    if 'cpu' in data1['checks'] and 'cpu' in data2['checks']:
        cpu1 = data1['checks']['cpu']['usage_percent']
        cpu2 = data2['checks']['cpu']['usage_percent']
        diff = cpu2 - cpu1
        arrow = "↑" if diff > 0 else "↓" if diff < 0 else "→"
        print(f"CPU Usage: {cpu1}% → {cpu2}% ({arrow} {abs(diff):.1f}%)")
    
    # Compare Disk Space
    if 'disk_space' in data1['checks'] and 'disk_space' in data2['checks']:
        print("\nDisk Space Changes:")
        for disk1 in data1['checks']['disk_space']:
            for disk2 in data2['checks']['disk_space']:
                if disk1['device'] == disk2['device']:
                    diff = disk2['percent_used'] - disk1['percent_used']
                    if abs(diff) > 0.1:  # Only show if changed
                        arrow = "↑" if diff > 0 else "↓"
                        print(f"  {disk1['device']}: {disk1['percent_used']}% → "
                              f"{disk2['percent_used']}% ({arrow} {abs(diff):.1f}%)")


def main():
    """Main entry point for report viewer."""
    report_files = list_reports()
    reports = display_report_summary(report_files)
    
    if not reports:
        return
    
    print("=" * 60)
    print("\nOptions:")
    print("  1-N  : View report by number")
    print("  c    : Compare two reports (JSON only)")
    print("  q    : Quit")
    print()
    
    try:
        choice = input("Select option: ").strip().lower()
        
        if choice == 'q':
            return
        
        elif choice == 'c':
            print("\nSelect first report:")
            idx1 = int(input("Report number: ").strip())
            print("Select second report:")
            idx2 = int(input("Report number: ").strip())
            
            if 1 <= idx1 <= len(reports) and 1 <= idx2 <= len(reports):
                compare_reports(reports[idx1-1]['file'], reports[idx2-1]['file'])
            else:
                print("Invalid report number(s)")
        
        elif choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(reports):
                report = reports[idx-1]
                
                if report['format'] == 'TXT':
                    view_txt_report(report['file'])
                elif report['format'] == 'JSON':
                    view_json_report(report['file'])
                elif report['format'] == 'CSV':
                    view_csv_report(report['file'])
            else:
                print("Invalid report number")
        
        else:
            print("Invalid option")
    
    except (ValueError, KeyboardInterrupt):
        print("\nExiting...")


if __name__ == '__main__':
    main()
