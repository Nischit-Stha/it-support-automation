# Quick Start Guide - IT Support Automation Toolkit

## 🚀 5-Minute Setup

### Step 1: Install Dependencies

```bash
# Navigate to the project directory
cd "It support automation toolkit"

# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt
```

### Step 2: Run Your First Check

```bash
# Basic usage - run all checks
python it_support_toolkit.py

# This will:
# ✓ Check disk space on all partitions
# ✓ Monitor CPU and RAM usage
# ✓ List logged-in users
# ✓ Test network connectivity
# ✓ Generate a report file
```

### Step 3: View Your Report

The toolkit will create a report file like `it_support_report_20251218_094237.txt` in the current directory.

## 📋 Common Use Cases

### Quick Health Check
```bash
python it_support_toolkit.py
```

### Check Only Disk Space
```bash
python it_support_toolkit.py --disk
```

### Check Only CPU/RAM
```bash
python it_support_toolkit.py --cpu
```

### Export to CSV for Spreadsheets
```bash
python it_support_toolkit.py --format csv
```

### Export to All Formats
```bash
python it_support_toolkit.py --format all
```

### Custom Report Name
```bash
python it_support_toolkit.py --output server01_health --format csv
```

## 🎯 Example Output

```
============================================================
IT SUPPORT AUTOMATION TOOLKIT
============================================================
Hostname: parrot
OS: Linux 6.12.32-amd64

=== DISK SPACE CHECK ===
✓ OK /dev/nvme0n1p1 (/)
   Total: 238.47 GB | Used: 128.17 GB (54.1%) | Free: 108.6 GB

=== CPU & RAM CHECK ===
✓ OK CPU Usage: 24.6%
   Cores: 4 physical, 8 logical
   Frequency: 2799.99 MHz (Max: 3900.0 MHz)

✓ OK RAM Usage: 49.5%
   Total: 14.72 GB | Used: 7.29 GB | Available: 7.43 GB

=== LOGGED IN USERS ===
✓ User: redmoon
   Terminal: :1 | Host: :1 | Since: 2025-12-18 08:30:00
```

## 🔧 Troubleshooting

### "No module named 'psutil'"
```bash
# Make sure you activated the virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### Permission Errors for Password Check
```bash
# Password expiry check requires sudo on Linux
sudo python it_support_toolkit.py --password
```

### Want to Run Without Virtual Environment?
```bash
# Install psutil system-wide (not recommended)
pip install psutil --user
```

## 📊 What Gets Checked?

| Check | What It Does | Warning Threshold |
|-------|--------------|-------------------|
| **Disk Space** | Monitors all partitions | > 80% used |
| **CPU Usage** | Current processor load | > 80% usage |
| **RAM Usage** | Memory consumption | > 80% used |
| **Users** | Currently logged-in users | N/A |
| **Network** | Connectivity tests | Failed connections |
| **Passwords** | Expiry dates (Linux) | Requires sudo |

## 💡 Pro Tips

1. **Schedule Regular Checks**
   ```bash
   # Add to crontab for daily 9 AM checks
   0 9 * * * cd /path/to/toolkit && source venv/bin/activate && python it_support_toolkit.py --format csv
   ```

2. **Check Multiple Servers**
   - Install on each server
   - Use `--output servername_report` to identify reports

3. **Quick Resource Check**
   ```bash
   # Just disk and CPU (fastest)
   python it_support_toolkit.py --disk --cpu
   ```

4. **Keep Historical Records**
   - Reports include timestamps
   - Save in dated folders for trend analysis

## 🎓 For Your CV/Resume

**What to highlight:**
- "Developed Python automation toolkit for IT system health monitoring"
- "Reduced manual health check time from 15 minutes to 30 seconds"
- "Automated disk space, CPU/RAM, user session, and network monitoring"
- "Implemented multi-format reporting (TXT/CSV/JSON) for documentation"

## 📝 Next Steps

1. Run the example script: `python example_usage.py`
2. Run the test suite: `python test_toolkit.py`
3. Customize for your environment
4. Add to your daily IT workflow

## ❓ Need Help?

Check the full README.md for detailed documentation and advanced features.
