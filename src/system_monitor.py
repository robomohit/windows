"""
System Monitor Module
Handles real-time monitoring of CPU, GPU, RAM, disk, and network usage
"""

import psutil
import threading
import time
from datetime import datetime
import json
import os

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

class SystemMonitor:
    def __init__(self):
        self.stats = {
            'cpu': {
                'usage_percent': 0.0,
                'frequency': 0.0,
                'cores': psutil.cpu_count(),
                'threads': psutil.cpu_count(logical=True),
                'temperature': 0.0,
                'per_core_usage': []
            },
            'memory': {
                'total': 0,
                'available': 0,
                'used': 0,
                'percent': 0.0,
                'swap_total': 0,
                'swap_used': 0,
                'swap_percent': 0.0
            },
            'disk': {
                'total': 0,
                'used': 0,
                'free': 0,
                'percent': 0.0,
                'read_speed': 0.0,
                'write_speed': 0.0
            },
            'network': {
                'bytes_sent': 0,
                'bytes_recv': 0,
                'packets_sent': 0,
                'packets_recv': 0,
                'upload_speed': 0.0,
                'download_speed': 0.0
            },
            'gpu': {
                'available': GPU_AVAILABLE,
                'usage_percent': 0.0,
                'memory_used': 0,
                'memory_total': 0,
                'memory_percent': 0.0,
                'temperature': 0.0,
                'name': 'N/A'
            },
            'processes': [],
            'system': {
                'boot_time': psutil.boot_time(),
                'uptime': 0,
                'users': 0
            }
        }
        
        # Initialize WMI for Windows-specific features
        if WMI_AVAILABLE and os.name == 'nt':
            try:
                self.wmi = wmi.WMI()
            except:
                self.wmi = None
                WMI_AVAILABLE = False
        else:
            self.wmi = None
            
        # Previous network stats for speed calculation
        self.prev_network_stats = None
        self.prev_disk_stats = None
        self.last_update_time = time.time()
        
        # History for graphs (last 60 seconds)
        self.history_size = 60
        self.cpu_history = []
        self.memory_history = []
        self.gpu_history = []
        self.network_history = []
        
    def update_stats(self):
        """Update all system statistics"""
        current_time = time.time()
        time_delta = current_time - self.last_update_time
        
        self._update_cpu_stats()
        self._update_memory_stats()
        self._update_disk_stats(time_delta)
        self._update_network_stats(time_delta)
        self._update_gpu_stats()
        self._update_process_stats()
        self._update_system_stats()
        
        # Update history for graphs
        self._update_history()
        
        self.last_update_time = current_time
        
    def _update_cpu_stats(self):
        """Update CPU statistics"""
        # CPU usage percentage
        self.stats['cpu']['usage_percent'] = psutil.cpu_percent(interval=None)
        
        # Per-core usage
        self.stats['cpu']['per_core_usage'] = psutil.cpu_percent(interval=None, percpu=True)
        
        # CPU frequency
        try:
            freq = psutil.cpu_freq()
            if freq:
                self.stats['cpu']['frequency'] = freq.current
        except:
            pass
            
        # CPU temperature (Windows specific)
        if self.wmi:
            try:
                temp_info = self.wmi.MSAcpi_ThermalZoneTemperature()
                if temp_info:
                    # Convert from tenths of Kelvin to Celsius
                    temp_kelvin = temp_info[0].CurrentTemperature / 10.0
                    self.stats['cpu']['temperature'] = temp_kelvin - 273.15
            except:
                pass
                
    def _update_memory_stats(self):
        """Update memory statistics"""
        # Physical memory
        memory = psutil.virtual_memory()
        self.stats['memory']['total'] = memory.total
        self.stats['memory']['available'] = memory.available
        self.stats['memory']['used'] = memory.used
        self.stats['memory']['percent'] = memory.percent
        
        # Swap memory
        swap = psutil.swap_memory()
        self.stats['memory']['swap_total'] = swap.total
        self.stats['memory']['swap_used'] = swap.used
        self.stats['memory']['swap_percent'] = swap.percent
        
    def _update_disk_stats(self, time_delta):
        """Update disk statistics"""
        # Disk usage for main drive
        try:
            disk_usage = psutil.disk_usage('/')
            self.stats['disk']['total'] = disk_usage.total
            self.stats['disk']['used'] = disk_usage.used
            self.stats['disk']['free'] = disk_usage.free
            self.stats['disk']['percent'] = (disk_usage.used / disk_usage.total) * 100
        except:
            # For Windows, try C: drive
            try:
                disk_usage = psutil.disk_usage('C:')
                self.stats['disk']['total'] = disk_usage.total
                self.stats['disk']['used'] = disk_usage.used
                self.stats['disk']['free'] = disk_usage.free
                self.stats['disk']['percent'] = (disk_usage.used / disk_usage.total) * 100
            except:
                pass
                
        # Disk I/O speeds
        try:
            disk_io = psutil.disk_io_counters()
            if disk_io and self.prev_disk_stats and time_delta > 0:
                read_bytes_diff = disk_io.read_bytes - self.prev_disk_stats.read_bytes
                write_bytes_diff = disk_io.write_bytes - self.prev_disk_stats.write_bytes
                
                self.stats['disk']['read_speed'] = read_bytes_diff / time_delta / 1024 / 1024  # MB/s
                self.stats['disk']['write_speed'] = write_bytes_diff / time_delta / 1024 / 1024  # MB/s
                
            self.prev_disk_stats = disk_io
        except:
            pass
            
    def _update_network_stats(self, time_delta):
        """Update network statistics"""
        try:
            network = psutil.net_io_counters()
            
            self.stats['network']['bytes_sent'] = network.bytes_sent
            self.stats['network']['bytes_recv'] = network.bytes_recv
            self.stats['network']['packets_sent'] = network.packets_sent
            self.stats['network']['packets_recv'] = network.packets_recv
            
            # Calculate network speeds
            if self.prev_network_stats and time_delta > 0:
                sent_diff = network.bytes_sent - self.prev_network_stats.bytes_sent
                recv_diff = network.bytes_recv - self.prev_network_stats.bytes_recv
                
                self.stats['network']['upload_speed'] = sent_diff / time_delta / 1024  # KB/s
                self.stats['network']['download_speed'] = recv_diff / time_delta / 1024  # KB/s
                
            self.prev_network_stats = network
        except:
            pass
            
    def _update_gpu_stats(self):
        """Update GPU statistics"""
        if not GPU_AVAILABLE:
            return
            
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]  # Use first GPU
                self.stats['gpu']['usage_percent'] = gpu.load * 100
                self.stats['gpu']['memory_used'] = gpu.memoryUsed
                self.stats['gpu']['memory_total'] = gpu.memoryTotal
                self.stats['gpu']['memory_percent'] = gpu.memoryUtil * 100
                self.stats['gpu']['temperature'] = gpu.temperature
                self.stats['gpu']['name'] = gpu.name
        except:
            pass
            
    def _update_process_stats(self):
        """Update top processes by CPU and memory usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    if proc_info['cpu_percent'] > 0 or proc_info['memory_percent'] > 0:
                        processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cpu_percent': proc_info['cpu_percent'],
                            'memory_percent': proc_info['memory_percent']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            # Sort by CPU usage and keep top 10
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            self.stats['processes'] = processes[:10]
        except:
            pass
            
    def _update_system_stats(self):
        """Update general system statistics"""
        # System uptime
        boot_time = psutil.boot_time()
        self.stats['system']['uptime'] = time.time() - boot_time
        
        # Active users
        try:
            users = psutil.users()
            self.stats['system']['users'] = len(users)
        except:
            pass
            
    def _update_history(self):
        """Update history arrays for graphing"""
        # Add current values to history
        self.cpu_history.append(self.stats['cpu']['usage_percent'])
        self.memory_history.append(self.stats['memory']['percent'])
        self.gpu_history.append(self.stats['gpu']['usage_percent'])
        self.network_history.append({
            'upload': self.stats['network']['upload_speed'],
            'download': self.stats['network']['download_speed']
        })
        
        # Keep only last N values
        if len(self.cpu_history) > self.history_size:
            self.cpu_history.pop(0)
        if len(self.memory_history) > self.history_size:
            self.memory_history.pop(0)
        if len(self.gpu_history) > self.history_size:
            self.gpu_history.pop(0)
        if len(self.network_history) > self.history_size:
            self.network_history.pop(0)
            
    def get_stats(self):
        """Get current system statistics"""
        return self.stats.copy()
        
    def get_cpu_history(self):
        """Get CPU usage history for graphing"""
        return self.cpu_history.copy()
        
    def get_memory_history(self):
        """Get memory usage history for graphing"""
        return self.memory_history.copy()
        
    def get_gpu_history(self):
        """Get GPU usage history for graphing"""
        return self.gpu_history.copy()
        
    def get_network_history(self):
        """Get network usage history for graphing"""
        return self.network_history.copy()
        
    def format_bytes(self, bytes_value):
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
        
    def format_uptime(self, uptime_seconds):
        """Format uptime to human readable format"""
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
            
    def export_stats_to_json(self, filename):
        """Export current stats to JSON file"""
        try:
            stats_with_timestamp = {
                'timestamp': datetime.now().isoformat(),
                'stats': self.stats
            }
            with open(filename, 'w') as f:
                json.dump(stats_with_timestamp, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting stats: {e}")
            return False