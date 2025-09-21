"""
System Monitor Module - REAL Windows Implementation
Handles real-time monitoring of CPU, GPU, RAM, disk, and network usage using Windows APIs
"""

import psutil
import threading
import time
from datetime import datetime
import json
import os
import ctypes
from ctypes import windll, wintypes, Structure, byref, c_ulong, c_char_p, POINTER
import winreg

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

try:
    import wmi
    import win32api
    import win32con
    import win32pdh
    import win32pdhutil
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("Warning: pywin32 or wmi not available. Some monitoring features will be limited.")

# Windows API structures for memory info
class MEMORYSTATUSEX(Structure):
    _fields_ = [
        ('dwLength', wintypes.DWORD),
        ('dwMemoryLoad', wintypes.DWORD),
        ('ullTotalPhys', c_ulong),
        ('ullAvailPhys', c_ulong),
        ('ullTotalPageFile', c_ulong),
        ('ullAvailPageFile', c_ulong),
        ('ullTotalVirtual', c_ulong),
        ('ullAvailVirtual', c_ulong),
        ('ullAvailExtendedVirtual', c_ulong)
    ]

# Windows API structures for system info
class SYSTEM_INFO(Structure):
    _fields_ = [
        ('wProcessorArchitecture', wintypes.WORD),
        ('wReserved', wintypes.WORD),
        ('dwPageSize', wintypes.DWORD),
        ('lpMinimumApplicationAddress', wintypes.LPVOID),
        ('lpMaximumApplicationAddress', wintypes.LPVOID),
        ('dwActiveProcessorMask', POINTER(wintypes.DWORD)),
        ('dwNumberOfProcessors', wintypes.DWORD),
        ('dwProcessorType', wintypes.DWORD),
        ('dwAllocationGranularity', wintypes.DWORD),
        ('wProcessorLevel', wintypes.WORD),
        ('wProcessorRevision', wintypes.WORD)
    ]

class SystemMonitor:
    def __init__(self):
        # Initialize Windows performance counters
        self.performance_counters = {}
        self.wmi_conn = None
        
        # Initialize WMI connection
        if WIN32_AVAILABLE:
            try:
                self.wmi_conn = wmi.WMI()
                self._initialize_performance_counters()
            except Exception as e:
                print(f"⚠️ Warning: Could not initialize WMI: {e}")
                self.wmi_conn = None
                
        # Get system info using Windows API
        self.system_info = self._get_system_info()
        
        self.stats = {
            'cpu': {
                'usage_percent': 0.0,
                'frequency': 0.0,
                'base_frequency': 0.0,
                'max_frequency': 0.0,
                'cores': self.system_info.get('cores', psutil.cpu_count()),
                'threads': self.system_info.get('threads', psutil.cpu_count(logical=True)),
                'temperature': 0.0,
                'per_core_usage': [],
                'name': self.system_info.get('cpu_name', 'Unknown'),
                'architecture': self.system_info.get('architecture', 'Unknown'),
                'cache_l1': self.system_info.get('cache_l1', 0),
                'cache_l2': self.system_info.get('cache_l2', 0),
                'cache_l3': self.system_info.get('cache_l3', 0)
            },
            'memory': {
                'total': 0,
                'available': 0,
                'used': 0,
                'percent': 0.0,
                'swap_total': 0,
                'swap_used': 0,
                'swap_percent': 0.0,
                'committed': 0,
                'committed_percent': 0.0,
                'cached': 0,
                'paged_pool': 0,
                'non_paged_pool': 0
            },
            'disk': {
                'total': 0,
                'used': 0,
                'free': 0,
                'percent': 0.0,
                'read_speed': 0.0,
                'write_speed': 0.0,
                'read_iops': 0.0,
                'write_iops': 0.0,
                'queue_length': 0.0,
                'disks': []
            },
            'network': {
                'bytes_sent': 0,
                'bytes_recv': 0,
                'packets_sent': 0,
                'packets_recv': 0,
                'upload_speed': 0.0,
                'download_speed': 0.0,
                'interfaces': []
            },
            'gpu': {
                'available': GPU_AVAILABLE,
                'usage_percent': 0.0,
                'memory_used': 0,
                'memory_total': 0,
                'memory_percent': 0.0,
                'temperature': 0.0,
                'name': 'N/A',
                'driver_version': 'N/A',
                'gpus': []
            },
            'processes': [],
            'system': {
                'boot_time': psutil.boot_time(),
                'uptime': 0,
                'users': 0,
                'os_version': self.system_info.get('os_version', 'Unknown'),
                'computer_name': self.system_info.get('computer_name', 'Unknown'),
                'total_handles': 0,
                'total_threads': 0,
                'total_processes': 0
            }
        }
            
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
        
    def _get_system_info(self):
        """Get detailed system information using Windows APIs"""
        system_info = {}
        
        try:
            if WIN32_AVAILABLE and self.wmi_conn:
                # Get CPU information
                cpu_info = self.wmi_conn.Win32_Processor()[0]
                system_info['cpu_name'] = cpu_info.Name.strip()
                system_info['cores'] = cpu_info.NumberOfCores
                system_info['threads'] = cpu_info.NumberOfLogicalProcessors
                system_info['base_frequency'] = getattr(cpu_info, 'MaxClockSpeed', 0)
                system_info['cache_l2'] = getattr(cpu_info, 'L2CacheSize', 0)
                system_info['cache_l3'] = getattr(cpu_info, 'L3CacheSize', 0)
                
                # Get OS information
                os_info = self.wmi_conn.Win32_OperatingSystem()[0]
                system_info['os_version'] = f"{os_info.Caption} {os_info.Version}"
                system_info['computer_name'] = os_info.CSName
                
                # Get system architecture
                sys_info = SYSTEM_INFO()
                windll.kernel32.GetSystemInfo(byref(sys_info))
                arch_map = {0: 'x86', 5: 'ARM', 9: 'x64', 12: 'ARM64'}
                system_info['architecture'] = arch_map.get(sys_info.wProcessorArchitecture, 'Unknown')
                
        except Exception as e:
            print(f"⚠️ Warning: Could not get detailed system info: {e}")
            
        return system_info
        
    def _initialize_performance_counters(self):
        """Initialize Windows performance counters for accurate monitoring"""
        try:
            if not WIN32_AVAILABLE:
                return
                
            # Initialize performance counters for detailed monitoring
            counter_paths = {
                'cpu_total': r'\Processor(_Total)\% Processor Time',
                'memory_available': r'\Memory\Available Bytes',
                'memory_committed': r'\Memory\Committed Bytes',
                'memory_cache': r'\Memory\Cache Bytes',
                'memory_paged_pool': r'\Memory\Pool Paged Bytes',
                'memory_non_paged_pool': r'\Memory\Pool Nonpaged Bytes',
                'disk_queue': r'\PhysicalDisk(_Total)\Current Disk Queue Length',
                'disk_read_iops': r'\PhysicalDisk(_Total)\Disk Reads/sec',
                'disk_write_iops': r'\PhysicalDisk(_Total)\Disk Writes/sec',
                'system_processes': r'\System\Processes',
                'system_threads': r'\System\Threads',
                'system_handles': r'\Process(_Total)\Handle Count'
            }
            
            for counter_name, counter_path in counter_paths.items():
                try:
                    counter = win32pdh.OpenQuery()
                    counter_handle = win32pdh.AddCounter(counter, counter_path)
                    self.performance_counters[counter_name] = {
                        'query': counter,
                        'handle': counter_handle,
                        'path': counter_path
                    }
                except Exception as e:
                    print(f"⚠️ Warning: Could not initialize counter {counter_name}: {e}")
                    
        except Exception as e:
            print(f"⚠️ Warning: Error initializing performance counters: {e}")
        
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
        """Update CPU statistics using Windows APIs and WMI"""
        try:
            # CPU usage percentage (using psutil as fallback)
            self.stats['cpu']['usage_percent'] = psutil.cpu_percent(interval=None)
            
            # Per-core usage
            self.stats['cpu']['per_core_usage'] = psutil.cpu_percent(interval=None, percpu=True)
            
            # CPU frequency using WMI for more accuracy
            if WIN32_AVAILABLE and self.wmi_conn:
                try:
                    cpu_info = self.wmi_conn.Win32_Processor()[0]
                    self.stats['cpu']['frequency'] = getattr(cpu_info, 'CurrentClockSpeed', 0)
                    self.stats['cpu']['max_frequency'] = getattr(cpu_info, 'MaxClockSpeed', 0)
                    
                    # Load percentage from WMI
                    cpu_load = getattr(cpu_info, 'LoadPercentage', None)
                    if cpu_load is not None:
                        self.stats['cpu']['usage_percent'] = cpu_load
                        
                except Exception as e:
                    # Fallback to psutil
                    try:
                        freq = psutil.cpu_freq()
                        if freq:
                            self.stats['cpu']['frequency'] = freq.current
                            self.stats['cpu']['max_frequency'] = freq.max
                    except:
                        pass
            else:
                # Fallback to psutil
                try:
                    freq = psutil.cpu_freq()
                    if freq:
                        self.stats['cpu']['frequency'] = freq.current
                        self.stats['cpu']['max_frequency'] = freq.max
                except:
                    pass
                    
            # CPU temperature using WMI thermal zones
            if WIN32_AVAILABLE and self.wmi_conn:
                try:
                    # Try multiple methods to get CPU temperature
                    temp_methods = [
                        # Method 1: MSAcpi_ThermalZoneTemperature
                        lambda: self.wmi_conn.MSAcpi_ThermalZoneTemperature(),
                        # Method 2: Win32_TemperatureProbe
                        lambda: self.wmi_conn.Win32_TemperatureProbe(),
                        # Method 3: OpenHardwareMonitor WMI (if installed)
                        lambda: self.wmi_conn.query("SELECT * FROM Sensor WHERE SensorType='Temperature' AND Name LIKE '%CPU%'")
                    ]
                    
                    for method in temp_methods:
                        try:
                            temp_info = method()
                            if temp_info:
                                for temp_sensor in temp_info:
                                    if hasattr(temp_sensor, 'CurrentTemperature'):
                                        # Convert from tenths of Kelvin to Celsius
                                        temp_kelvin = temp_sensor.CurrentTemperature / 10.0
                                        temp_celsius = temp_kelvin - 273.15
                                        if 0 < temp_celsius < 150:  # Reasonable temperature range
                                            self.stats['cpu']['temperature'] = temp_celsius
                                            break
                                    elif hasattr(temp_sensor, 'CurrentReading'):
                                        # Some sensors report in different units
                                        temp = temp_sensor.CurrentReading / 10.0
                                        if 0 < temp < 150:
                                            self.stats['cpu']['temperature'] = temp
                                            break
                                if self.stats['cpu']['temperature'] > 0:
                                    break
                        except:
                            continue
                            
                except Exception as e:
                    pass  # Temperature monitoring is optional
                    
        except Exception as e:
            print(f"⚠️ Warning: Error updating CPU stats: {e}")
            # Fallback to basic psutil monitoring
            try:
                self.stats['cpu']['usage_percent'] = psutil.cpu_percent(interval=None)
                self.stats['cpu']['per_core_usage'] = psutil.cpu_percent(interval=None, percpu=True)
            except:
                pass
                
    def _update_memory_stats(self):
        """Update memory statistics using Windows APIs"""
        try:
            # Use Windows API for more detailed memory information
            mem_status = MEMORYSTATUSEX()
            mem_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            windll.kernel32.GlobalMemoryStatusEx(byref(mem_status))
            
            self.stats['memory']['total'] = mem_status.ullTotalPhys
            self.stats['memory']['available'] = mem_status.ullAvailPhys
            self.stats['memory']['used'] = mem_status.ullTotalPhys - mem_status.ullAvailPhys
            self.stats['memory']['percent'] = mem_status.dwMemoryLoad
            
            # Page file (swap) information
            self.stats['memory']['swap_total'] = mem_status.ullTotalPageFile
            self.stats['memory']['swap_used'] = mem_status.ullTotalPageFile - mem_status.ullAvailPageFile
            if mem_status.ullTotalPageFile > 0:
                self.stats['memory']['swap_percent'] = (self.stats['memory']['swap_used'] / mem_status.ullTotalPageFile) * 100
            else:
                self.stats['memory']['swap_percent'] = 0
                
            # Get additional memory details using WMI and performance counters
            if WIN32_AVAILABLE and self.wmi_conn:
                try:
                    # Get committed memory from performance counters
                    if 'memory_committed' in self.performance_counters:
                        counter_info = self.performance_counters['memory_committed']
                        win32pdh.CollectQueryData(counter_info['query'])
                        committed_bytes = win32pdh.GetFormattedCounterValue(counter_info['handle'], win32pdh.PDH_FMT_LARGE)[1]
                        self.stats['memory']['committed'] = committed_bytes
                        self.stats['memory']['committed_percent'] = (committed_bytes / mem_status.ullTotalPhys) * 100
                        
                    # Get cache information
                    if 'memory_cache' in self.performance_counters:
                        counter_info = self.performance_counters['memory_cache']
                        win32pdh.CollectQueryData(counter_info['query'])
                        cache_bytes = win32pdh.GetFormattedCounterValue(counter_info['handle'], win32pdh.PDH_FMT_LARGE)[1]
                        self.stats['memory']['cached'] = cache_bytes
                        
                    # Get pool information
                    if 'memory_paged_pool' in self.performance_counters:
                        counter_info = self.performance_counters['memory_paged_pool']
                        win32pdh.CollectQueryData(counter_info['query'])
                        paged_pool = win32pdh.GetFormattedCounterValue(counter_info['handle'], win32pdh.PDH_FMT_LARGE)[1]
                        self.stats['memory']['paged_pool'] = paged_pool
                        
                    if 'memory_non_paged_pool' in self.performance_counters:
                        counter_info = self.performance_counters['memory_non_paged_pool']
                        win32pdh.CollectQueryData(counter_info['query'])
                        non_paged_pool = win32pdh.GetFormattedCounterValue(counter_info['handle'], win32pdh.PDH_FMT_LARGE)[1]
                        self.stats['memory']['non_paged_pool'] = non_paged_pool
                        
                except Exception as e:
                    pass  # Performance counter errors are non-critical
                    
        except Exception as e:
            print(f"⚠️ Warning: Error updating memory stats: {e}")
            # Fallback to psutil
            try:
                memory = psutil.virtual_memory()
                self.stats['memory']['total'] = memory.total
                self.stats['memory']['available'] = memory.available
                self.stats['memory']['used'] = memory.used
                self.stats['memory']['percent'] = memory.percent
                
                swap = psutil.swap_memory()
                self.stats['memory']['swap_total'] = swap.total
                self.stats['memory']['swap_used'] = swap.used
                self.stats['memory']['swap_percent'] = swap.percent
            except:
                pass
        
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
        """Update GPU statistics using multiple methods"""
        self.stats['gpu']['gpus'] = []
        
        # Method 1: Use GPUtil if available
        if GPU_AVAILABLE:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    for gpu in gpus:
                        gpu_info = {
                            'id': gpu.id,
                            'name': gpu.name,
                            'usage_percent': gpu.load * 100,
                            'memory_used': gpu.memoryUsed,
                            'memory_total': gpu.memoryTotal,
                            'memory_percent': gpu.memoryUtil * 100,
                            'temperature': gpu.temperature,
                            'driver_version': getattr(gpu, 'driver', 'Unknown')
                        }
                        self.stats['gpu']['gpus'].append(gpu_info)
                        
                    # Set primary GPU stats (first GPU)
                    if self.stats['gpu']['gpus']:
                        primary_gpu = self.stats['gpu']['gpus'][0]
                        self.stats['gpu']['usage_percent'] = primary_gpu['usage_percent']
                        self.stats['gpu']['memory_used'] = primary_gpu['memory_used']
                        self.stats['gpu']['memory_total'] = primary_gpu['memory_total']
                        self.stats['gpu']['memory_percent'] = primary_gpu['memory_percent']
                        self.stats['gpu']['temperature'] = primary_gpu['temperature']
                        self.stats['gpu']['name'] = primary_gpu['name']
                        self.stats['gpu']['driver_version'] = primary_gpu['driver_version']
                        
            except Exception as e:
                print(f"⚠️ Warning: GPUtil error: {e}")
                
        # Method 2: Use WMI for additional GPU information
        if WIN32_AVAILABLE and self.wmi_conn:
            try:
                video_controllers = self.wmi_conn.Win32_VideoController()
                
                for i, controller in enumerate(video_controllers):
                    # Skip basic VGA adapters
                    if 'VGA' in controller.Name or 'Basic' in controller.Name:
                        continue
                        
                    gpu_info = {
                        'id': i,
                        'name': controller.Name,
                        'driver_version': getattr(controller, 'DriverVersion', 'Unknown'),
                        'driver_date': getattr(controller, 'DriverDate', 'Unknown'),
                        'memory_total': getattr(controller, 'AdapterRAM', 0) // (1024 * 1024),  # Convert to MB
                        'pnp_device_id': getattr(controller, 'PNPDeviceID', 'Unknown'),
                        'status': getattr(controller, 'Status', 'Unknown')
                    }
                    
                    # If we don't have this GPU from GPUtil, add it
                    existing_gpu = None
                    for existing in self.stats['gpu']['gpus']:
                        if existing['name'] == gpu_info['name']:
                            existing_gpu = existing
                            break
                            
                    if existing_gpu:
                        # Update existing GPU info with WMI data
                        existing_gpu.update({
                            'driver_version': gpu_info['driver_version'],
                            'driver_date': gpu_info['driver_date'],
                            'pnp_device_id': gpu_info['pnp_device_id'],
                            'status': gpu_info['status']
                        })
                        if existing_gpu['memory_total'] == 0 and gpu_info['memory_total'] > 0:
                            existing_gpu['memory_total'] = gpu_info['memory_total']
                    else:
                        # Add new GPU (without usage stats)
                        gpu_info.update({
                            'usage_percent': 0,
                            'memory_used': 0,
                            'memory_percent': 0,
                            'temperature': 0
                        })
                        self.stats['gpu']['gpus'].append(gpu_info)
                        
                    # If this is the first GPU and we don't have primary stats yet
                    if (i == 0 and self.stats['gpu']['name'] == 'N/A' and 
                        'NVIDIA' in controller.Name or 'AMD' in controller.Name or 'Intel' in controller.Name):
                        self.stats['gpu']['name'] = controller.Name
                        self.stats['gpu']['driver_version'] = gpu_info['driver_version']
                        if gpu_info['memory_total'] > 0:
                            self.stats['gpu']['memory_total'] = gpu_info['memory_total']
                            
            except Exception as e:
                print(f"⚠️ Warning: WMI GPU error: {e}")
                
        # Method 3: Try to get NVIDIA GPU stats using nvidia-ml-py or nvidia-smi
        try:
            import subprocess
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu', 
                                   '--format=csv,noheader,nounits'], 
                                   capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for i, line in enumerate(lines):
                    if line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 5:
                            nvidia_gpu = {
                                'id': f'nvidia_{i}',
                                'name': parts[0],
                                'usage_percent': float(parts[1]) if parts[1] != 'N/A' else 0,
                                'memory_used': int(parts[2]) if parts[2] != 'N/A' else 0,
                                'memory_total': int(parts[3]) if parts[3] != 'N/A' else 0,
                                'temperature': float(parts[4]) if parts[4] != 'N/A' else 0,
                                'driver_version': 'NVIDIA',
                                'source': 'nvidia-smi'
                            }
                            
                            if nvidia_gpu['memory_total'] > 0:
                                nvidia_gpu['memory_percent'] = (nvidia_gpu['memory_used'] / nvidia_gpu['memory_total']) * 100
                            else:
                                nvidia_gpu['memory_percent'] = 0
                                
                            # Update existing or add new
                            existing = None
                            for gpu in self.stats['gpu']['gpus']:
                                if nvidia_gpu['name'] in gpu['name'] or gpu['name'] in nvidia_gpu['name']:
                                    existing = gpu
                                    break
                                    
                            if existing:
                                existing.update(nvidia_gpu)
                            else:
                                self.stats['gpu']['gpus'].append(nvidia_gpu)
                                
                            # Update primary GPU if this is the first NVIDIA GPU
                            if i == 0:
                                self.stats['gpu'].update({
                                    'name': nvidia_gpu['name'],
                                    'usage_percent': nvidia_gpu['usage_percent'],
                                    'memory_used': nvidia_gpu['memory_used'],
                                    'memory_total': nvidia_gpu['memory_total'],
                                    'memory_percent': nvidia_gpu['memory_percent'],
                                    'temperature': nvidia_gpu['temperature']
                                })
                                
        except Exception as e:
            pass  # nvidia-smi not available or failed
            
        # Update availability flag
        self.stats['gpu']['available'] = len(self.stats['gpu']['gpus']) > 0
            
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