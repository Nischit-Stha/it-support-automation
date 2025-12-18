# IT Support Automation Toolkit - Test Suite
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from it_support_toolkit import ITSupportToolkit


class TestITSupportToolkit(unittest.TestCase):
    """Test cases for IT Support Toolkit."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.toolkit = ITSupportToolkit()
    
    def test_initialization(self):
        """Test toolkit initialization."""
        self.assertIsNotNone(self.toolkit.report_data)
        self.assertIn('timestamp', self.toolkit.report_data)
        self.assertIn('hostname', self.toolkit.report_data)
        self.assertIn('os', self.toolkit.report_data)
        self.assertIn('checks', self.toolkit.report_data)
    
    @patch('psutil.disk_partitions')
    @patch('psutil.disk_usage')
    def test_check_disk_space(self, mock_disk_usage, mock_disk_partitions):
        """Test disk space checking."""
        # Mock disk partition
        mock_partition = Mock()
        mock_partition.device = '/dev/sda1'
        mock_partition.mountpoint = '/'
        mock_partition.fstype = 'ext4'
        mock_disk_partitions.return_value = [mock_partition]
        
        # Mock disk usage
        mock_usage = Mock()
        mock_usage.total = 100 * (1024**3)  # 100 GB
        mock_usage.used = 50 * (1024**3)    # 50 GB
        mock_usage.free = 50 * (1024**3)    # 50 GB
        mock_usage.percent = 50.0
        mock_disk_usage.return_value = mock_usage
        
        result = self.toolkit.check_disk_space()
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]['device'], '/dev/sda1')
        self.assertEqual(result[0]['percent_used'], 50.0)
    
    @patch('psutil.cpu_percent')
    @patch('psutil.cpu_count')
    @patch('psutil.cpu_freq')
    @patch('psutil.virtual_memory')
    def test_check_cpu_ram(self, mock_vmem, mock_cpu_freq, mock_cpu_count, mock_cpu_percent):
        """Test CPU and RAM checking."""
        # Mock CPU
        mock_cpu_percent.return_value = 25.5
        mock_cpu_count.side_effect = [4, 8]  # physical, logical
        
        mock_freq = Mock()
        mock_freq.current = 2400.0
        mock_freq.max = 3400.0
        mock_cpu_freq.return_value = mock_freq
        
        # Mock RAM
        mock_ram = Mock()
        mock_ram.total = 16 * (1024**3)      # 16 GB
        mock_ram.used = 8 * (1024**3)        # 8 GB
        mock_ram.available = 8 * (1024**3)   # 8 GB
        mock_ram.percent = 50.0
        mock_vmem.return_value = mock_ram
        
        cpu_data, ram_data = self.toolkit.check_cpu_ram()
        
        self.assertEqual(cpu_data['usage_percent'], 25.5)
        self.assertEqual(cpu_data['physical_cores'], 4)
        self.assertEqual(cpu_data['logical_cores'], 8)
        
        self.assertEqual(ram_data['percent_used'], 50.0)
        self.assertEqual(ram_data['total_gb'], 16.0)
    
    @patch('psutil.users')
    def test_list_users(self, mock_users):
        """Test user listing."""
        # Mock user
        mock_user = Mock()
        mock_user.name = 'testuser'
        mock_user.terminal = 'pts/0'
        mock_user.host = 'localhost'
        mock_user.started = 1234567890.0
        mock_users.return_value = [mock_user]
        
        result = self.toolkit.list_users()
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'testuser')
        self.assertEqual(result[0]['terminal'], 'pts/0')
    
    @patch('psutil.users')
    def test_list_users_empty(self, mock_users):
        """Test user listing when no users logged in."""
        mock_users.return_value = []
        
        result = self.toolkit.list_users()
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
    
    def test_export_report_txt(self):
        """Test TXT report export."""
        # Add some test data
        self.toolkit.report_data['checks']['disk_space'] = [{
            'device': '/dev/sda1',
            'mountpoint': '/',
            'filesystem': 'ext4',
            'total_gb': 100.0,
            'used_gb': 50.0,
            'free_gb': 50.0,
            'percent_used': 50.0
        }]
        
        filepath = self.toolkit.export_report_txt('test_report.txt')
        
        self.assertTrue(os.path.exists(filepath))
        
        with open(filepath, 'r') as f:
            content = f.read()
            self.assertIn('IT SUPPORT SYSTEM HEALTH CHECK REPORT', content)
            self.assertIn('/dev/sda1', content)
        
        # Cleanup
        os.remove(filepath)
    
    def test_export_report_csv(self):
        """Test CSV report export."""
        self.toolkit.report_data['checks']['cpu'] = {
            'usage_percent': 25.5,
            'physical_cores': 4,
            'logical_cores': 8,
            'current_freq_mhz': 2400.0,
            'max_freq_mhz': 3400.0
        }
        
        filepath = self.toolkit.export_report_csv('test_report.csv')
        
        self.assertTrue(os.path.exists(filepath))
        
        with open(filepath, 'r') as f:
            content = f.read()
            self.assertIn('IT Support System Health Check Report', content)
            self.assertIn('CPU INFORMATION', content)
        
        # Cleanup
        os.remove(filepath)
    
    def test_export_report_json(self):
        """Test JSON report export."""
        self.toolkit.report_data['checks']['ram'] = {
            'total_gb': 16.0,
            'used_gb': 8.0,
            'available_gb': 8.0,
            'percent_used': 50.0
        }
        
        filepath = self.toolkit.export_report_json('test_report.json')
        
        self.assertTrue(os.path.exists(filepath))
        
        import json
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.assertIn('timestamp', data)
            self.assertIn('checks', data)
            self.assertIn('ram', data['checks'])
        
        # Cleanup
        os.remove(filepath)


if __name__ == '__main__':
    print("Running IT Support Toolkit Tests...")
    print("=" * 60)
    unittest.main(verbosity=2)
