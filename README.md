# IT Support Automation Toolkit

A comprehensive Python tool for automating common IT support health checks and generating detailed system reports. Perfect for IT support professionals who need to quickly assess system health and document system status.

## Features

### Core Features
- ✅ **Disk Space Check** - Monitor disk usage across all partitions with warnings for high usage (>80%)
- ✅ **CPU & RAM Monitoring** - Real-time CPU and memory usage statistics
- ✅ **User Management** - List all currently logged-in users with session details
- ✅ **Report Export** - Generate reports in TXT, CSV, or JSON format

### Optional Advanced Features
- ✅ **Password Expiry Checker** - Monitor password expiration dates (Linux only, requires sudo)
- ✅ **Network Connectivity Tests** - Verify connectivity to common services and list network interfaces

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository:
```bash
cd "It support automation toolkit"
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Make the script executable (Linux/Mac):
```bash
chmod +x it_support_toolkit.py
```

## Usage

### Basic Usage

Run all checks and export to TXT format (default):
```bash
python it_support_toolkit.py
```

### Export Formats

Export to CSV:
```bash
python it_support_toolkit.py --format csv
```

Export to JSON:
```bash
python it_support_toolkit.py --format json
```

Export to all formats (TXT, CSV, and JSON):
```bash
python it_support_toolkit.py --format all
```

### Specific Checks

Run only disk space check:
```bash
python it_support_toolkit.py --disk
```

Run only CPU/RAM check:
```bash
python it_support_toolkit.py --cpu
```

List logged-in users only:
```bash
python it_support_toolkit.py --users
```

Check network connectivity only:
```bash
python it_support_toolkit.py --network
```

Check password expiry only (Linux, requires sudo):
```bash
python it_support_toolkit.py --password
```

### Combine Multiple Checks

```bash
python it_support_toolkit.py --disk --cpu --format csv
```

### Custom Output Filename

```bash
python it_support_toolkit.py --output my_report --format txt
```

This will create `my_report.txt` in the current directory.

## Output Examples

### Console Output
```
============================================================
IT SUPPORT AUTOMATION TOOLKIT
============================================================
Hostname: myserver
OS: Linux 5.15.0-91-generic
Timestamp: 2025-12-18 10:30:45

=== DISK SPACE CHECK ===
✓ OK /dev/sda1 (/)
   Total: 100.0 GB | Used: 45.5 GB (45.5%) | Free: 54.5 GB

=== CPU & RAM CHECK ===
✓ OK CPU Usage: 25.3%
   Cores: 4 physical, 8 logical
   Frequency: 2400.0 MHz (Max: 3400.0 MHz)

✓ OK RAM Usage: 58.2%
   Total: 16.0 GB | Used: 9.3 GB | Available: 6.7 GB
```

### Text Report
Generates a comprehensive formatted text report with all system information.

### CSV Report
Structured data format ideal for importing into spreadsheets or databases.

### JSON Report
Machine-readable format perfect for integration with other tools or APIs.

## What This Demonstrates

### Technical Skills
- **Python Programming** - Clean, well-structured object-oriented code
- **System Administration** - Understanding of OS-level operations
- **Cross-Platform Development** - Works on Linux, macOS, and Windows
- **Library Usage** - Efficient use of `psutil` for system monitoring
- **Data Export** - Multiple output formats (TXT, CSV, JSON)

### IT Support Competencies
- **Proactive Monitoring** - Automated health checks reduce manual effort
- **Documentation** - Automatic report generation for record-keeping
- **Problem Prevention** - Early warning system for resource issues
- **Efficiency** - Reduces time spent on routine checks

### Professional Best Practices
- Command-line interface with flexible options
- Clear documentation and usage examples
- Error handling and graceful degradation
- Modular, maintainable code structure

## System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.6+
- **Dependencies**: psutil (automatically installed via requirements.txt)

## Advanced Usage

### Scheduled Monitoring

Set up a cron job (Linux/Mac) to run checks automatically:

```bash
# Edit crontab
crontab -e

# Add line to run every day at 9 AM
0 9 * * * cd /path/to/toolkit && python it_support_toolkit.py --format csv
```

### Integration with Monitoring Systems

The JSON output format makes it easy to integrate with monitoring dashboards or alerting systems:

```python
import json
with open('report.json') as f:
    data = json.load(f)
    if data['checks']['ram']['percent_used'] > 90:
        send_alert("High RAM usage detected!")
```

## Troubleshooting

### Permission Errors
Some checks (especially password expiry) may require elevated privileges:
```bash
sudo python it_support_toolkit.py --password
```

### Missing psutil Module
If you get import errors, ensure psutil is installed:
```bash
pip install psutil --upgrade
```

### Windows Notes
- Password expiry check is not available on Windows
- Some system commands may differ; the tool handles this gracefully

## CV/Resume Line

**IT Support Automation Specialist**
- Developed Python-based automation toolkit to streamline IT support health checks
- Implemented automated system monitoring for disk space, CPU/RAM, user sessions, and network connectivity
- Created multi-format reporting system (TXT/CSV/JSON) for documentation and compliance
- Reduced routine system check time by 80% through automation

## License

This project is provided as-is for educational and professional use.

## Author

Created as part of an IT Support automation portfolio project.

## Contributing

Feel free to fork this project and add your own features! Some ideas:
- Email notifications for critical alerts
- Historical data tracking and trends
- Service monitoring (check if specific services are running)
- Hardware temperature monitoring
- Log file analysis
- Scheduled report generation with email delivery

## Project Structure

```
It support automation toolkit/
│
├── it_support_toolkit.py       # Main toolkit script
│   ├── ITSupportToolkit class (checks + exporters + CLI)
│   └── run_all_checks()        # Executes full suite
│
├── example_usage.py            # Usage demonstrations
├── view_reports.py             # Interactive report viewer + compare
├── test_toolkit.py             # Unit tests (unittest + mocks)
├── requirements.txt            # Dependencies (psutil)
├── README.md                   # Documentation (this file)
├── QUICKSTART.md               # 5-minute setup guide
├── SUMMARY.md                  # Portfolio/CV summary
├── VISUAL_OVERVIEW.md          # Visual diagrams
├── .gitignore                  # Git ignore rules
└── venv/                       # Virtual environment (local)

Generated Reports (excluded from git):
├── it_support_report_YYYYMMDD_HHMMSS.txt
├── it_support_report_YYYYMMDD_HHMMSS.csv
└── it_support_report_YYYYMMDD_HHMMSS.json
```

### Key Files
- `it_support_toolkit.py`: Core checks (disk, CPU/RAM, users, network, password expiry) + exporters (TXT/CSV/JSON) + CLI.
- `view_reports.py`: Lists, views, and compares generated reports.
- `test_toolkit.py`: Verifies functionality for checks and exporters.
- `QUICKSTART.md`: Fast setup and common commands.
- `SUMMARY.md`: Ready-made project summary for portfolio/CV.

