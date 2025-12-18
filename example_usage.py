#!/usr/bin/env python3
"""
Example script demonstrating usage of the IT Support Toolkit
"""

from it_support_toolkit import ITSupportToolkit

def basic_example():
    """Run all checks and export to all formats."""
    print("=== BASIC EXAMPLE: Running all checks ===\n")
    
    toolkit = ITSupportToolkit()
    toolkit.run_all_checks(export_format='all')

def specific_checks_example():
    """Run only specific checks."""
    print("\n\n=== SPECIFIC CHECKS EXAMPLE ===\n")
    
    toolkit = ITSupportToolkit()
    
    # Run individual checks
    print("Running disk space check only...")
    toolkit.check_disk_space()
    
    print("\nRunning CPU/RAM check only...")
    toolkit.check_cpu_ram()
    
    # Export results
    toolkit.export_report_txt("specific_checks_report.txt")

def custom_report_example():
    """Generate custom report with specific checks."""
    print("\n\n=== CUSTOM REPORT EXAMPLE ===\n")
    
    toolkit = ITSupportToolkit()
    
    # Check resources
    disk_info = toolkit.check_disk_space()
    cpu_data, ram_data = toolkit.check_cpu_ram()
    
    # Check if any warnings
    warnings = []
    
    for disk in disk_info:
        if disk['percent_used'] > 80:
            warnings.append(f"High disk usage on {disk['device']}: {disk['percent_used']}%")
    
    if cpu_data['usage_percent'] > 80:
        warnings.append(f"High CPU usage: {cpu_data['usage_percent']}%")
    
    if ram_data['percent_used'] > 80:
        warnings.append(f"High RAM usage: {ram_data['percent_used']}%")
    
    if warnings:
        print("\n⚠️  WARNINGS DETECTED:")
        for warning in warnings:
            print(f"   - {warning}")
    else:
        print("\n✓ All systems operating normally")
    
    # Export
    toolkit.export_report_csv("custom_report.csv")

if __name__ == '__main__':
    # Uncomment the example you want to run
    
    basic_example()
    # specific_checks_example()
    # custom_report_example()
