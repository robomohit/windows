"""
Gaming Optimizer Module
Handles gaming performance optimizations including process priority, memory cleanup, and system tweaks
"""

import psutil
import subprocess
import os
import sys
import time
import gc
import threading
from ctypes import windll, wintypes, byref, c_ulong, c_void_p, Structure

try:
    import win32api
    import win32con
    import win32process
    import win32gui
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

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

class GamingOptimizer:
    def __init__(self):
        self.boost_mode_active = False
        self.original_priorities = {}
        self.original_affinities = {}
        self.gaming_processes = []
        self.background_processes_paused = []
        
        # Common gaming process names to prioritize
        self.gaming_process_names = [
            'steam.exe', 'steamwebhelper.exe',
            'origin.exe', 'originwebhelperservice.exe',
            'epicgameslauncher.exe', 'unrealcefsubprocess.exe',
            'battle.net.exe', 'agent.exe',
            'uplay.exe', 'uplayservice.exe',
            'gog.com.exe', 'goggalaxy.exe',
            # Add common game executables
            'csgo.exe', 'dota2.exe', 'pubg.exe', 'fortnite.exe',
            'apex_legends.exe', 'valorant.exe', 'overwatch.exe',
            'minecraft.exe', 'wow.exe', 'lol.exe'
        ]
        
        # Background processes to pause/deprioritize during gaming
        self.background_process_names = [
            'chrome.exe', 'firefox.exe', 'edge.exe', 'opera.exe',
            'spotify.exe', 'discord.exe', 'skype.exe',
            'dropbox.exe', 'onedrive.exe', 'googledrivesync.exe',
            'backup.exe', 'antivirus.exe', 'defender.exe',
            'updater.exe', 'installer.exe'
        ]
        
    def enable_boost_mode(self):
        """Enable gaming boost mode with various optimizations"""
        if self.boost_mode_active:
            return
            
        try:
            print("Enabling Gaming Boost Mode...")
            
            # 1. Optimize process priorities
            self._optimize_process_priorities()
            
            # 2. Set high performance power plan
            self._set_high_performance_power_plan()
            
            # 3. Disable Windows Game Mode conflicts
            self._optimize_windows_gaming()
            
            # 4. Optimize system services
            self._optimize_system_services()
            
            # 5. Clear system cache
            self._clear_system_cache()
            
            # 6. Optimize network settings
            self._optimize_network_for_gaming()
            
            # 7. Set process affinity for better CPU usage
            self._optimize_cpu_affinity()
            
            self.boost_mode_active = True
            print("Gaming Boost Mode enabled successfully!")
            
        except Exception as e:
            print(f"Error enabling boost mode: {e}")
            raise
            
    def disable_boost_mode(self):
        """Disable gaming boost mode and restore original settings"""
        if not self.boost_mode_active:
            return
            
        try:
            print("Disabling Gaming Boost Mode...")
            
            # Restore original process priorities
            self._restore_process_priorities()
            
            # Restore original CPU affinities
            self._restore_cpu_affinities()
            
            # Resume paused background processes
            self._resume_background_processes()
            
            # Restore balanced power plan
            self._set_balanced_power_plan()
            
            self.boost_mode_active = False
            print("Gaming Boost Mode disabled successfully!")
            
        except Exception as e:
            print(f"Error disabling boost mode: {e}")
            raise
            
    def _optimize_process_priorities(self):
        """Optimize process priorities for gaming"""
        if not WIN32_AVAILABLE:
            return
            
        try:
            # Find and prioritize gaming processes
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    pid = proc.info['pid']
                    
                    # Prioritize gaming processes
                    if any(game_proc in proc_name for game_proc in self.gaming_process_names):
                        self._set_process_priority(pid, win32process.HIGH_PRIORITY_CLASS)
                        self.gaming_processes.append(pid)
                        
                    # Deprioritize background processes
                    elif any(bg_proc in proc_name for bg_proc in self.background_process_names):
                        original_priority = self._get_process_priority(pid)
                        if original_priority:
                            self.original_priorities[pid] = original_priority
                            self._set_process_priority(pid, win32process.BELOW_NORMAL_PRIORITY_CLASS)
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            print(f"Error optimizing process priorities: {e}")
            
    def _set_process_priority(self, pid, priority_class):
        """Set process priority using Windows API"""
        if not WIN32_AVAILABLE:
            return False
            
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_SET_INFORMATION, False, pid)
            win32process.SetPriorityClass(handle, priority_class)
            win32api.CloseHandle(handle)
            return True
        except Exception as e:
            print(f"Error setting priority for PID {pid}: {e}")
            return False
            
    def _get_process_priority(self, pid):
        """Get current process priority"""
        if not WIN32_AVAILABLE:
            return None
            
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
            priority = win32process.GetPriorityClass(handle)
            win32api.CloseHandle(handle)
            return priority
        except:
            return None
            
    def _restore_process_priorities(self):
        """Restore original process priorities"""
        for pid, original_priority in self.original_priorities.items():
            try:
                self._set_process_priority(pid, original_priority)
            except:
                pass
        self.original_priorities.clear()
        
    def _optimize_cpu_affinity(self):
        """Optimize CPU core affinity for gaming processes"""
        if not WIN32_AVAILABLE:
            return
            
        try:
            cpu_count = psutil.cpu_count()
            if cpu_count <= 2:
                return  # Not enough cores to optimize
                
            # Reserve last 2 cores for gaming processes
            gaming_affinity = (1 << cpu_count) - 1  # All cores initially
            background_affinity = (1 << (cpu_count - 2)) - 1  # First N-2 cores
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    pid = proc.info['pid']
                    
                    # Set affinity for gaming processes
                    if any(game_proc in proc_name for game_proc in self.gaming_process_names):
                        self._set_process_affinity(pid, gaming_affinity)
                        
                    # Limit background processes to fewer cores
                    elif any(bg_proc in proc_name for bg_proc in self.background_process_names):
                        original_affinity = self._get_process_affinity(pid)
                        if original_affinity:
                            self.original_affinities[pid] = original_affinity
                            self._set_process_affinity(pid, background_affinity)
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            print(f"Error optimizing CPU affinity: {e}")
            
    def _set_process_affinity(self, pid, affinity_mask):
        """Set process CPU affinity"""
        if not WIN32_AVAILABLE:
            return False
            
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_SET_INFORMATION, False, pid)
            win32process.SetProcessAffinityMask(handle, affinity_mask)
            win32api.CloseHandle(handle)
            return True
        except:
            return False
            
    def _get_process_affinity(self, pid):
        """Get current process CPU affinity"""
        if not WIN32_AVAILABLE:
            return None
            
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
            affinity = win32process.GetProcessAffinityMask(handle)[0]
            win32api.CloseHandle(handle)
            return affinity
        except:
            return None
            
    def _restore_cpu_affinities(self):
        """Restore original CPU affinities"""
        for pid, original_affinity in self.original_affinities.items():
            try:
                self._set_process_affinity(pid, original_affinity)
            except:
                pass
        self.original_affinities.clear()
        
    def _set_high_performance_power_plan(self):
        """Set Windows power plan to high performance"""
        try:
            # High Performance GUID
            high_perf_guid = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
            subprocess.run([
                "powercfg", "/setactive", high_perf_guid
            ], check=True, capture_output=True)
            
            # Additional power optimizations
            power_settings = [
                ("processor-idle-disable", "1"),  # Disable processor idle
                ("processor-perf-boost-mode", "0"),  # Disable boost mode throttling
                ("processor-perf-core-parking-min-cores", "100"),  # Minimum cores
            ]
            
            for setting, value in power_settings:
                try:
                    subprocess.run([
                        "powercfg", "/setacvalueindex", "SCHEME_CURRENT", 
                        "processor", setting, value
                    ], check=True, capture_output=True)
                except:
                    pass
                    
        except Exception as e:
            print(f"Error setting high performance power plan: {e}")
            
    def _set_balanced_power_plan(self):
        """Restore balanced power plan"""
        try:
            # Balanced GUID
            balanced_guid = "381b4222-f694-41f0-9685-ff5bb260df2e"
            subprocess.run([
                "powercfg", "/setactive", balanced_guid
            ], check=True, capture_output=True)
        except Exception as e:
            print(f"Error setting balanced power plan: {e}")
            
    def _optimize_windows_gaming(self):
        """Optimize Windows gaming settings"""
        try:
            # Disable Windows Game Bar
            subprocess.run([
                "reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR",
                "/v", "AppCaptureEnabled", "/t", "REG_DWORD", "/d", "0", "/f"
            ], check=True, capture_output=True)
            
            # Disable Game Mode conflicts
            subprocess.run([
                "reg", "add", "HKCU\\Software\\Microsoft\\GameBar",
                "/v", "AllowAutoGameMode", "/t", "REG_DWORD", "/d", "0", "/f"
            ], check=True, capture_output=True)
            
            # Disable fullscreen optimizations
            subprocess.run([
                "reg", "add", "HKCU\\System\\GameConfigStore",
                "/v", "GameDVR_Enabled", "/t", "REG_DWORD", "/d", "0", "/f"
            ], check=True, capture_output=True)
            
        except Exception as e:
            print(f"Error optimizing Windows gaming settings: {e}")
            
    def _optimize_system_services(self):
        """Optimize system services for gaming"""
        # Services to disable temporarily during gaming
        services_to_stop = [
            "Fax", "WSearch", "Spooler", "SysMain",  # Superfetch
            "Themes", "TabletInputService", "WbioSrvc"
        ]
        
        for service in services_to_stop:
            try:
                subprocess.run([
                    "sc", "stop", service
                ], check=True, capture_output=True)
            except:
                pass  # Service might not exist or already stopped
                
    def _clear_system_cache(self):
        """Clear various system caches"""
        try:
            # Clear DNS cache
            subprocess.run(["ipconfig", "/flushdns"], check=True, capture_output=True)
            
            # Clear Windows temporary files
            temp_paths = [
                os.path.expandvars("%TEMP%"),
                os.path.expandvars("%WINDIR%\\Temp"),
                os.path.expandvars("%WINDIR%\\Prefetch")
            ]
            
            for temp_path in temp_paths:
                if os.path.exists(temp_path):
                    try:
                        for file in os.listdir(temp_path):
                            file_path = os.path.join(temp_path, file)
                            try:
                                if os.path.isfile(file_path):
                                    os.remove(file_path)
                            except:
                                pass
                    except:
                        pass
                        
        except Exception as e:
            print(f"Error clearing system cache: {e}")
            
    def _optimize_network_for_gaming(self):
        """Optimize network settings for gaming"""
        try:
            # Disable Nagle's algorithm for gaming
            subprocess.run([
                "reg", "add", "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters",
                "/v", "TcpAckFrequency", "/t", "REG_DWORD", "/d", "1", "/f"
            ], check=True, capture_output=True)
            
            subprocess.run([
                "reg", "add", "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters",
                "/v", "TCPNoDelay", "/t", "REG_DWORD", "/d", "1", "/f"
            ], check=True, capture_output=True)
            
            # Optimize network adapter settings
            subprocess.run([
                "netsh", "int", "tcp", "set", "global", "autotuninglevel=normal"
            ], check=True, capture_output=True)
            
        except Exception as e:
            print(f"Error optimizing network for gaming: {e}")
            
    def _resume_background_processes(self):
        """Resume paused background processes"""
        for pid in self.background_processes_paused:
            try:
                proc = psutil.Process(pid)
                proc.resume()
            except:
                pass
        self.background_processes_paused.clear()
        
    def cleanup_memory(self):
        """Clean up system memory and return amount freed"""
        try:
            # Get initial memory info
            initial_memory = psutil.virtual_memory()
            initial_available = initial_memory.available
            
            # Force garbage collection
            gc.collect()
            
            # Clear working set for current process
            if WIN32_AVAILABLE:
                try:
                    windll.psapi.EmptyWorkingSet(-1)
                except:
                    pass
                    
            # Clear standby memory (requires admin privileges)
            try:
                subprocess.run([
                    "rundll32.exe", "advapi32.dll,ProcessIdleTasks"
                ], check=True, capture_output=True)
            except:
                pass
                
            # Wait a moment for cleanup to take effect
            time.sleep(1)
            
            # Calculate freed memory
            final_memory = psutil.virtual_memory()
            final_available = final_memory.available
            freed_mb = (final_available - initial_available) / 1024 / 1024
            
            return max(0, freed_mb)  # Return 0 if negative
            
        except Exception as e:
            print(f"Error cleaning up memory: {e}")
            return 0
            
    def get_gaming_processes(self):
        """Get list of currently running gaming processes"""
        gaming_procs = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(game_proc in proc_name for game_proc in self.gaming_process_names):
                        gaming_procs.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cpu_percent': proc.info['cpu_percent'],
                            'memory_percent': proc.info['memory_percent']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except:
            pass
            
        return gaming_procs
        
    def set_process_priority_by_name(self, process_name, priority_level):
        """Set priority for all processes matching the given name"""
        if not WIN32_AVAILABLE:
            return False
            
        priority_map = {
            'low': win32process.IDLE_PRIORITY_CLASS,
            'below_normal': win32process.BELOW_NORMAL_PRIORITY_CLASS,
            'normal': win32process.NORMAL_PRIORITY_CLASS,
            'above_normal': win32process.ABOVE_NORMAL_PRIORITY_CLASS,
            'high': win32process.HIGH_PRIORITY_CLASS,
            'realtime': win32process.REALTIME_PRIORITY_CLASS
        }
        
        priority_class = priority_map.get(priority_level.lower())
        if not priority_class:
            return False
            
        success_count = 0
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() == process_name.lower():
                        if self._set_process_priority(proc.info['pid'], priority_class):
                            success_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except:
            pass
            
        return success_count > 0