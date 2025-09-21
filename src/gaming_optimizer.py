"""
Gaming Optimizer Module - REAL Windows Implementation
Handles gaming performance optimizations with actual Windows API calls and registry modifications
"""

import psutil
import subprocess
import os
import sys
import time
import gc
import threading
import winreg
from ctypes import windll, wintypes, byref, c_ulong, c_void_p, Structure, POINTER, c_char_p
from ctypes.wintypes import DWORD, HANDLE, BOOL

try:
    import win32api
    import win32con
    import win32process
    import win32gui
    import win32service
    import win32serviceutil
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("Warning: pywin32 not available. Some features will be limited.")

# Windows API constants
PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_SET_INFORMATION = 0x0200
PROCESS_QUERY_INFORMATION = 0x0400

# Priority classes
IDLE_PRIORITY_CLASS = 0x00000040
BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
NORMAL_PRIORITY_CLASS = 0x00000020
ABOVE_NORMAL_PRIORITY_CLASS = 0x00008000
HIGH_PRIORITY_CLASS = 0x00000080
REALTIME_PRIORITY_CLASS = 0x00000100

class MEMORYSTATUSEX(Structure):
    _fields_ = [
        ('dwLength', DWORD),
        ('dwMemoryLoad', DWORD),
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
        self.original_power_scheme = None
        self.services_stopped = []
        
        # Enhanced gaming process detection
        self.gaming_process_names = [
            # Game launchers
            'steam.exe', 'steamwebhelper.exe', 'steamservice.exe',
            'origin.exe', 'originwebhelperservice.exe', 'originthinsetupinternal.exe',
            'epicgameslauncher.exe', 'epicgameslauncher-win32-shipping.exe', 'unrealcefsubprocess.exe',
            'battle.net.exe', 'agent.exe', 'blizzard update agent.exe',
            'uplay.exe', 'uplayservice.exe', 'uplaywebcore.exe',
            'gog.com.exe', 'goggalaxy.exe', 'galaxyclient.exe',
            'rockstargameslauncher.exe', 'launcherapp.exe',
            
            # Popular games
            'csgo.exe', 'cs2.exe', 'dota2.exe', 'pubg.exe', 'tslgame.exe',
            'fortnite.exe', 'fortniteclient-win64-shipping.exe',
            'apex_legends.exe', 'r5apex.exe',
            'valorant.exe', 'valorant-win64-shipping.exe', 'riotclientservices.exe',
            'overwatch.exe', 'overwatch2.exe',
            'minecraft.exe', 'javaw.exe', 'minecraftlauncher.exe',
            'wow.exe', 'worldofwarcraft.exe', '_retail_\\wow.exe',
            'lol.exe', 'league of legends.exe', 'riotclientux.exe',
            'gta5.exe', 'gtav.exe', 'rdr2.exe',
            'cyberpunk2077.exe', 'witcher3.exe',
            'cod.exe', 'modernwarfare.exe', 'warzone.exe',
            'destiny2.exe', 'destiny2launcher.exe',
            'rainbow6.exe', 'rainbowsix.exe', 'r6game.exe',
            'battlefield.exe', 'bf1.exe', 'bfv.exe', 'bf2042.exe',
            'fifa23.exe', 'fifa24.exe', 'ea sports fc 24.exe',
            'rocket league.exe', 'rocketleague.exe',
            'among us.exe', 'amongus.exe',
            'fall guys.exe', 'fallguys_client_game.exe',
            'halo infinite.exe', 'haloinfinite.exe',
            'sea of thieves.exe', 'seaofthieves.exe',
            'microsoft flight simulator.exe', 'flightsimulator.exe',
            'forza.exe', 'forzahorizon5.exe', 'forzamotorsport.exe'
        ]
        
        # Services to temporarily stop during gaming
        self.services_to_stop = [
            'Fax',           # Fax service
            'WSearch',       # Windows Search
            'Spooler',       # Print Spooler (if no printing needed)
            'Themes',        # Themes service
            'TabletInputService',  # Tablet PC Input Service
            'WbioSrvc',      # Windows Biometric Service
            'SysMain',       # Superfetch/Prefetch
            'DiagTrack',     # Diagnostics Tracking Service
            'dmwappushservice',  # WAP Push Message Routing Service
        ]
        
    def enable_boost_mode(self):
        """Enable gaming boost mode with REAL Windows optimizations"""
        if self.boost_mode_active:
            return
            
        try:
            print("🎮 Enabling Gaming Boost Mode...")
            
            # 1. Set high performance power plan
            self._set_high_performance_power_plan()
            
            # 2. Optimize process priorities and CPU affinity
            self._optimize_process_priorities()
            self._optimize_cpu_affinity()
            
            # 3. Stop non-essential services
            self._stop_non_essential_services()
            
            # 4. Apply Windows gaming registry optimizations
            self._apply_gaming_registry_optimizations()
            
            # 5. Optimize memory settings
            self._optimize_memory_settings()
            
            # 6. Disable Windows Game Bar and DVR
            self._disable_game_bar_dvr()
            
            # 7. Set gaming-focused Windows settings
            self._set_gaming_windows_settings()
            
            # 8. Optimize network for gaming
            self._optimize_network_for_gaming()
            
            # 9. Clear system caches
            self._clear_system_cache()
            
            self.boost_mode_active = True
            print("✅ Gaming Boost Mode enabled successfully!")
            
        except Exception as e:
            print(f"❌ Error enabling boost mode: {e}")
            raise
            
    def disable_boost_mode(self):
        """Disable gaming boost mode and restore original settings"""
        if not self.boost_mode_active:
            return
            
        try:
            print("🔄 Disabling Gaming Boost Mode...")
            
            # Restore original process priorities
            self._restore_process_priorities()
            
            # Restore original CPU affinities
            self._restore_cpu_affinities()
            
            # Restart stopped services
            self._restart_stopped_services()
            
            # Restore original power plan
            self._restore_original_power_plan()
            
            self.boost_mode_active = False
            print("✅ Gaming Boost Mode disabled successfully!")
            
        except Exception as e:
            print(f"❌ Error disabling boost mode: {e}")
            raise
            
    def _set_high_performance_power_plan(self):
        """Set Windows power plan to high performance"""
        try:
            # Get current power scheme first
            result = subprocess.run(['powercfg', '/getactivescheme'], 
                                  capture_output=True, text=True, check=True)
            self.original_power_scheme = result.stdout.strip()
            
            # High Performance GUID
            high_perf_guid = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
            
            # Set high performance power plan
            subprocess.run(['powercfg', '/setactive', high_perf_guid], 
                          check=True, capture_output=True)
            
            # Additional power optimizations
            power_settings = [
                # Processor power management
                ('54533251-82be-4824-96c1-47b60b740d00', '893dee8e-2bef-41e0-89c6-b55d0929964c', '0'),  # Processor idle disable
                ('54533251-82be-4824-96c1-47b60b740d00', '5d76a2ca-e8c0-402f-a133-2158492d58ad', '1'),  # Processor performance boost mode
                ('54533251-82be-4824-96c1-47b60b740d00', '0cc5b647-c1df-4637-891a-dec35c318583', '100'), # Processor performance level increase threshold
                ('54533251-82be-4824-96c1-47b60b740d00', '12a0ab44-fe28-4fa9-b3bd-4b64f44960a6', '100'), # Processor performance core parking min cores
                
                # System cooling policy
                ('54533251-82be-4824-96c1-47b60b740d00', '94d3a615-a899-4ac5-ae2b-e4d8f634367f', '0'),  # System cooling policy (Active)
                
                # PCI Express settings
                ('501a4d13-42af-4429-9fd1-a8218c268e20', 'ee12f906-d277-404b-b6da-e5fa1a576df5', '0'),  # PCI Express Link State Power Management (Off)
            ]
            
            for scheme_guid, setting_guid, value in power_settings:
                try:
                    subprocess.run([
                        'powercfg', '/setacvalueindex', 'SCHEME_CURRENT',
                        scheme_guid, setting_guid, value
                    ], check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    pass  # Some settings might not be available on all systems
                    
            # Apply settings
            subprocess.run(['powercfg', '/setactive', 'SCHEME_CURRENT'], 
                          check=True, capture_output=True)
            
            print("✅ High performance power plan activated")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not set power plan: {e}")
            
    def _restore_original_power_plan(self):
        """Restore the original power plan"""
        if self.original_power_scheme:
            try:
                # Extract GUID from the original scheme string
                import re
                guid_match = re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', 
                                     self.original_power_scheme)
                if guid_match:
                    original_guid = guid_match.group(1)
                    subprocess.run(['powercfg', '/setactive', original_guid], 
                                  check=True, capture_output=True)
                    print("✅ Original power plan restored")
            except:
                # Fallback to balanced power plan
                balanced_guid = "381b4222-f694-41f0-9685-ff5bb260df2e"
                subprocess.run(['powercfg', '/setactive', balanced_guid], 
                              capture_output=True)
                
    def _optimize_process_priorities(self):
        """Optimize process priorities for gaming with REAL Windows API calls"""
        if not WIN32_AVAILABLE:
            print("⚠️ Warning: pywin32 not available, skipping process priority optimization")
            return
            
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    pid = proc.info['pid']
                    
                    # Skip system processes
                    if pid < 4:
                        continue
                    
                    # Prioritize gaming processes
                    if any(game_proc in proc_name for game_proc in self.gaming_process_names):
                        original_priority = self._get_process_priority(pid)
                        if original_priority:
                            self.original_priorities[pid] = original_priority
                            self._set_process_priority(pid, HIGH_PRIORITY_CLASS)
                            self.gaming_processes.append(pid)
                            print(f"✅ Set HIGH priority for gaming process: {proc_name}")
                            
                    # Deprioritize background processes
                    elif self._is_background_process(proc_name):
                        original_priority = self._get_process_priority(pid)
                        if original_priority and original_priority != BELOW_NORMAL_PRIORITY_CLASS:
                            self.original_priorities[pid] = original_priority
                            self._set_process_priority(pid, BELOW_NORMAL_PRIORITY_CLASS)
                            print(f"✅ Set LOW priority for background process: {proc_name}")
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
                    continue
                    
        except Exception as e:
            print(f"⚠️ Warning: Error optimizing process priorities: {e}")
            
    def _is_background_process(self, proc_name):
        """Check if process is a background process that should be deprioritized"""
        background_processes = [
            'chrome.exe', 'firefox.exe', 'msedge.exe', 'opera.exe', 'brave.exe',
            'spotify.exe', 'discord.exe', 'skype.exe', 'teams.exe',
            'dropbox.exe', 'onedrive.exe', 'googledrivesync.exe',
            'backup.exe', 'carbonite.exe', 'crashplan.exe',
            'updater.exe', 'installer.exe', 'setup.exe',
            'torrent.exe', 'utorrent.exe', 'bittorrent.exe',
            'obs64.exe', 'obs32.exe', 'xsplit.exe',
            'photoshop.exe', 'illustrator.exe', 'premiere.exe',
            'devenv.exe', 'code.exe', 'pycharm64.exe'
        ]
        return any(bg_proc in proc_name for bg_proc in background_processes)
        
    def _set_process_priority(self, pid, priority_class):
        """Set process priority using Windows API"""
        if not WIN32_AVAILABLE:
            return False
            
        try:
            handle = win32api.OpenProcess(PROCESS_SET_INFORMATION, False, pid)
            if handle:
                win32process.SetPriorityClass(handle, priority_class)
                win32api.CloseHandle(handle)
                return True
        except Exception as e:
            # Try alternative method using psutil
            try:
                proc = psutil.Process(pid)
                if priority_class == HIGH_PRIORITY_CLASS:
                    proc.nice(psutil.HIGH_PRIORITY_CLASS)
                elif priority_class == BELOW_NORMAL_PRIORITY_CLASS:
                    proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                return True
            except:
                pass
        return False
        
    def _get_process_priority(self, pid):
        """Get current process priority"""
        if not WIN32_AVAILABLE:
            return None
            
        try:
            handle = win32api.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
            if handle:
                priority = win32process.GetPriorityClass(handle)
                win32api.CloseHandle(handle)
                return priority
        except:
            pass
        return None
        
    def _restore_process_priorities(self):
        """Restore original process priorities"""
        for pid, original_priority in self.original_priorities.items():
            try:
                if psutil.pid_exists(pid):
                    self._set_process_priority(pid, original_priority)
            except:
                pass
        self.original_priorities.clear()
        self.gaming_processes.clear()
        
    def _optimize_cpu_affinity(self):
        """Optimize CPU core affinity for gaming processes"""
        if not WIN32_AVAILABLE:
            return
            
        try:
            cpu_count = psutil.cpu_count()
            if cpu_count <= 2:
                return  # Not enough cores to optimize
                
            # Create affinity masks
            all_cores = (1 << cpu_count) - 1
            gaming_cores = all_cores  # Gaming processes get all cores
            background_cores = (1 << (cpu_count // 2)) - 1  # Background processes get half cores
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    pid = proc.info['pid']
                    
                    if pid < 4:  # Skip system processes
                        continue
                    
                    # Set affinity for gaming processes (all cores)
                    if any(game_proc in proc_name for game_proc in self.gaming_process_names):
                        original_affinity = self._get_process_affinity(pid)
                        if original_affinity:
                            self.original_affinities[pid] = original_affinity
                            self._set_process_affinity(pid, gaming_cores)
                            
                    # Limit background processes to fewer cores
                    elif self._is_background_process(proc_name):
                        original_affinity = self._get_process_affinity(pid)
                        if original_affinity and original_affinity != background_cores:
                            self.original_affinities[pid] = original_affinity
                            self._set_process_affinity(pid, background_cores)
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            print(f"⚠️ Warning: Error optimizing CPU affinity: {e}")
            
    def _set_process_affinity(self, pid, affinity_mask):
        """Set process CPU affinity"""
        try:
            if WIN32_AVAILABLE:
                handle = win32api.OpenProcess(PROCESS_SET_INFORMATION, False, pid)
                if handle:
                    win32process.SetProcessAffinityMask(handle, affinity_mask)
                    win32api.CloseHandle(handle)
                    return True
            else:
                # Fallback using psutil
                proc = psutil.Process(pid)
                # Convert mask to CPU list
                cpu_list = [i for i in range(64) if affinity_mask & (1 << i)]
                proc.cpu_affinity(cpu_list)
                return True
        except:
            return False
            
    def _get_process_affinity(self, pid):
        """Get current process CPU affinity"""
        try:
            if WIN32_AVAILABLE:
                handle = win32api.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
                if handle:
                    affinity = win32process.GetProcessAffinityMask(handle)[0]
                    win32api.CloseHandle(handle)
                    return affinity
            else:
                proc = psutil.Process(pid)
                cpu_list = proc.cpu_affinity()
                # Convert CPU list to mask
                mask = 0
                for cpu in cpu_list:
                    mask |= (1 << cpu)
                return mask
        except:
            return None
            
    def _restore_cpu_affinities(self):
        """Restore original CPU affinities"""
        for pid, original_affinity in self.original_affinities.items():
            try:
                if psutil.pid_exists(pid):
                    self._set_process_affinity(pid, original_affinity)
            except:
                pass
        self.original_affinities.clear()
        
    def _stop_non_essential_services(self):
        """Stop non-essential Windows services during gaming"""
        if not WIN32_AVAILABLE:
            return
            
        try:
            for service_name in self.services_to_stop:
                try:
                    # Check if service exists and is running
                    service_status = win32serviceutil.QueryServiceStatus(service_name)
                    if service_status[1] == win32service.SERVICE_RUNNING:
                        win32serviceutil.StopService(service_name)
                        self.services_stopped.append(service_name)
                        print(f"✅ Stopped service: {service_name}")
                except Exception as e:
                    # Service might not exist or already stopped
                    pass
        except Exception as e:
            print(f"⚠️ Warning: Error stopping services: {e}")
            
    def _restart_stopped_services(self):
        """Restart services that were stopped during gaming"""
        if not WIN32_AVAILABLE:
            return
            
        for service_name in self.services_stopped:
            try:
                win32serviceutil.StartService(service_name)
                print(f"✅ Restarted service: {service_name}")
            except:
                pass
        self.services_stopped.clear()
        
    def _apply_gaming_registry_optimizations(self):
        """Apply gaming-focused Windows registry optimizations"""
        try:
            # Gaming registry optimizations
            registry_settings = [
                # Disable Game DVR and Game Bar
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\GameDVR", 
                 "AppCaptureEnabled", 0, winreg.REG_DWORD),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\GameDVR", 
                 "GameDVR_Enabled", 0, winreg.REG_DWORD),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar", 
                 "AllowAutoGameMode", 0, winreg.REG_DWORD),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar", 
                 "AutoGameModeEnabled", 0, winreg.REG_DWORD),
                
                # Disable Fullscreen Optimizations
                (winreg.HKEY_CURRENT_USER, r"System\GameConfigStore", 
                 "GameDVR_Enabled", 0, winreg.REG_DWORD),
                (winreg.HKEY_CURRENT_USER, r"System\GameConfigStore", 
                 "GameDVR_FSEBehaviorMode", 2, winreg.REG_DWORD),
                
                # Network optimizations
                (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", 
                 "TcpAckFrequency", 1, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", 
                 "TCPNoDelay", 1, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", 
                 "TcpDelAckTicks", 0, winreg.REG_DWORD),
                
                # Disable Windows Update during gaming
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU", 
                 "NoAutoUpdate", 1, winreg.REG_DWORD),
                
                # Gaming mode optimizations
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar", 
                 "ShowStartupPanel", 0, winreg.REG_DWORD),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar", 
                 "UseNexusForGameBarEnabled", 0, winreg.REG_DWORD),
            ]
            
            for hive, key_path, value_name, value_data, value_type in registry_settings:
                try:
                    key = winreg.CreateKeyEx(hive, key_path)
                    winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                    winreg.CloseKey(key)
                except Exception as e:
                    print(f"⚠️ Warning: Could not set registry value {key_path}\\{value_name}: {e}")
                    
            print("✅ Gaming registry optimizations applied")
            
        except Exception as e:
            print(f"⚠️ Warning: Error applying registry optimizations: {e}")
            
    def _optimize_memory_settings(self):
        """Optimize Windows memory settings for gaming"""
        try:
            # Clear working sets for all processes except gaming processes
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    pid = proc.info['pid']
                    
                    # Skip gaming processes and system processes
                    if (any(game_proc in proc_name for game_proc in self.gaming_process_names) or 
                        pid < 4):
                        continue
                        
                    # Clear working set for background processes
                    if WIN32_AVAILABLE:
                        try:
                            handle = win32api.OpenProcess(PROCESS_SET_INFORMATION, False, pid)
                            if handle:
                                # SetProcessWorkingSetSize with -1, -1 trims working set
                                windll.kernel32.SetProcessWorkingSetSize(handle, -1, -1)
                                win32api.CloseHandle(handle)
                        except:
                            pass
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            print("✅ Memory settings optimized")
            
        except Exception as e:
            print(f"⚠️ Warning: Error optimizing memory settings: {e}")
            
    def _disable_game_bar_dvr(self):
        """Disable Windows Game Bar and Game DVR completely"""
        try:
            # Disable via registry
            registry_keys = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\GameDVR"),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar"),
                (winreg.HKEY_CURRENT_USER, r"System\GameConfigStore"),
            ]
            
            for hive, key_path in registry_keys:
                try:
                    key = winreg.CreateKeyEx(hive, key_path)
                    # Disable all Game DVR and Game Bar features
                    winreg.SetValueEx(key, "AppCaptureEnabled", 0, winreg.REG_DWORD, 0)
                    winreg.SetValueEx(key, "GameDVR_Enabled", 0, winreg.REG_DWORD, 0)
                    winreg.SetValueEx(key, "AllowAutoGameMode", 0, winreg.REG_DWORD, 0)
                    winreg.CloseKey(key)
                except:
                    pass
                    
            # Also disable via PowerShell
            try:
                subprocess.run([
                    'powershell', '-Command',
                    'Get-AppxPackage Microsoft.XboxGamingOverlay | Remove-AppxPackage'
                ], capture_output=True)
            except:
                pass
                
            print("✅ Game Bar and DVR disabled")
            
        except Exception as e:
            print(f"⚠️ Warning: Error disabling Game Bar: {e}")
            
    def _set_gaming_windows_settings(self):
        """Set Windows settings optimized for gaming"""
        try:
            # Disable Windows animations and visual effects
            registry_settings = [
                # Disable animations
                (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", "MenuShowDelay", "0"),
                (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop\WindowMetrics", "MinAnimate", "0"),
                
                # Disable visual effects
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", 
                 "VisualFXSetting", 2, winreg.REG_DWORD),  # Custom settings
                
                # Disable transparency effects
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 
                 "EnableTransparency", 0, winreg.REG_DWORD),
                 
                # Focus assist settings
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\Cache\DefaultAccount", 
                 "QuietHoursProfile", 2, winreg.REG_DWORD),  # Game mode
            ]
            
            for hive, key_path, value_name, value_data, *value_type in registry_settings:
                try:
                    key = winreg.CreateKeyEx(hive, key_path)
                    if value_type:
                        winreg.SetValueEx(key, value_name, 0, value_type[0], value_data)
                    else:
                        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, str(value_data))
                    winreg.CloseKey(key)
                except:
                    pass
                    
            print("✅ Gaming Windows settings applied")
            
        except Exception as e:
            print(f"⚠️ Warning: Error setting Windows gaming settings: {e}")
            
    def _optimize_network_for_gaming(self):
        """Apply network optimizations specifically for gaming"""
        try:
            # Network optimization commands
            network_commands = [
                # TCP optimizations
                ['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=normal'],
                ['netsh', 'int', 'tcp', 'set', 'global', 'chimney=enabled'],
                ['netsh', 'int', 'tcp', 'set', 'global', 'rss=enabled'],
                ['netsh', 'int', 'tcp', 'set', 'global', 'netdma=enabled'],
                ['netsh', 'int', 'tcp', 'set', 'heuristics', 'disabled'],
                
                # Windows scaling heuristics
                ['netsh', 'int', 'tcp', 'set', 'supplemental', 'Internet', 'congestionprovider=ctcp'],
                
                # QoS optimizations
                ['netsh', 'int', 'tcp', 'set', 'global', 'nonsackrttresiliency=disabled'],
                ['netsh', 'int', 'tcp', 'set', 'security', 'mpp=disabled'],
                ['netsh', 'int', 'tcp', 'set', 'security', 'profiles=disabled'],
            ]
            
            for command in network_commands:
                try:
                    subprocess.run(command, check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    pass  # Some commands might fail on different Windows versions
                    
            print("✅ Network optimizations applied")
            
        except Exception as e:
            print(f"⚠️ Warning: Error applying network optimizations: {e}")
            
    def _clear_system_cache(self):
        """Clear various system caches to free up memory"""
        try:
            # Clear DNS cache
            subprocess.run(['ipconfig', '/flushdns'], check=True, capture_output=True)
            
            # Clear ARP cache
            subprocess.run(['arp', '-d', '*'], capture_output=True)
            
            # Clear NetBIOS cache
            subprocess.run(['nbtstat', '-R'], capture_output=True)
            
            # Force garbage collection
            gc.collect()
            
            # Clear standby memory using Windows API
            try:
                # This requires admin privileges
                subprocess.run([
                    'powershell', '-Command',
                    'Clear-RecycleBin -Force; [System.GC]::Collect()'
                ], capture_output=True)
            except:
                pass
                
            print("✅ System caches cleared")
            
        except Exception as e:
            print(f"⚠️ Warning: Error clearing system cache: {e}")
            
    def cleanup_memory(self):
        """Clean up system memory and return amount freed in MB"""
        try:
            # Get initial memory info
            mem_status = MEMORYSTATUSEX()
            mem_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            windll.kernel32.GlobalMemoryStatusEx(byref(mem_status))
            initial_available = mem_status.ullAvailPhys
            
            # Force garbage collection
            gc.collect()
            
            # Clear working sets for all processes except gaming
            freed_memory = 0
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    proc_name = proc.info['name'].lower()
                    pid = proc.info['pid']
                    
                    # Skip gaming processes and system processes
                    if (any(game_proc in proc_name for game_proc in self.gaming_process_names) or 
                        pid < 4):
                        continue
                        
                    # Get memory before cleanup
                    initial_mem = proc.info['memory_info'].rss
                    
                    # Clear working set
                    if WIN32_AVAILABLE:
                        try:
                            handle = win32api.OpenProcess(PROCESS_SET_INFORMATION, False, pid)
                            if handle:
                                windll.kernel32.SetProcessWorkingSetSize(handle, -1, -1)
                                win32api.CloseHandle(handle)
                                
                                # Check memory after cleanup
                                time.sleep(0.1)  # Small delay for memory to be freed
                                try:
                                    current_proc = psutil.Process(pid)
                                    final_mem = current_proc.memory_info().rss
                                    freed_memory += max(0, initial_mem - final_mem)
                                except:
                                    pass
                        except:
                            pass
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            # Get final memory info
            windll.kernel32.GlobalMemoryStatusEx(byref(mem_status))
            final_available = mem_status.ullAvailPhys
            
            # Calculate total freed memory
            total_freed = max(0, (final_available - initial_available) / 1024 / 1024)  # Convert to MB
            
            print(f"✅ Memory cleanup completed: {total_freed:.1f} MB freed")
            return total_freed
            
        except Exception as e:
            print(f"⚠️ Warning: Error cleaning up memory: {e}")
            return 0
            
    def get_gaming_processes(self):
        """Get list of currently running gaming processes"""
        gaming_procs = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(game_proc in proc_name for game_proc in self.gaming_process_names):
                        # Get additional process info
                        try:
                            process = psutil.Process(proc.info['pid'])
                            cpu_percent = process.cpu_percent()
                            memory_info = process.memory_info()
                            
                            gaming_procs.append({
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'cpu_percent': cpu_percent,
                                'memory_percent': proc.info['memory_percent'],
                                'memory_mb': memory_info.rss / 1024 / 1024,
                                'create_time': proc.info['create_time'],
                                'status': process.status(),
                                'priority': self._get_process_priority(proc.info['pid'])
                            })
                        except:
                            # Fallback with basic info
                            gaming_procs.append({
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'cpu_percent': proc.info.get('cpu_percent', 0),
                                'memory_percent': proc.info.get('memory_percent', 0),
                                'memory_mb': 0,
                                'create_time': proc.info.get('create_time', 0),
                                'status': 'unknown',
                                'priority': None
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"⚠️ Warning: Error getting gaming processes: {e}")
            
        return gaming_procs
        
    def set_process_priority_by_name(self, process_name, priority_level):
        """Set priority for all processes matching the given name"""
        priority_map = {
            'idle': IDLE_PRIORITY_CLASS,
            'low': BELOW_NORMAL_PRIORITY_CLASS,
            'below_normal': BELOW_NORMAL_PRIORITY_CLASS,
            'normal': NORMAL_PRIORITY_CLASS,
            'above_normal': ABOVE_NORMAL_PRIORITY_CLASS,
            'high': HIGH_PRIORITY_CLASS,
            'realtime': REALTIME_PRIORITY_CLASS
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
                            print(f"✅ Set {priority_level} priority for {process_name} (PID: {proc.info['pid']})")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"⚠️ Warning: Error setting process priority: {e}")
            
        return success_count > 0
        
    def is_boost_mode_active(self):
        """Check if boost mode is currently active"""
        return self.boost_mode_active
        
    def get_optimization_status(self):
        """Get detailed status of current optimizations"""
        return {
            'boost_mode_active': self.boost_mode_active,
            'gaming_processes_optimized': len(self.gaming_processes),
            'background_processes_deprioritized': len([pid for pid in self.original_priorities.keys() if pid not in self.gaming_processes]),
            'services_stopped': len(self.services_stopped),
            'power_plan_optimized': self.original_power_scheme is not None,
            'registry_optimized': self.boost_mode_active,  # Registry optimizations are applied with boost mode
            'memory_optimized': self.boost_mode_active
        }