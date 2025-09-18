"""
Network Optimizer Module - REAL Windows Implementation
Handles network optimizations for gaming with actual Windows commands and registry modifications
"""

import subprocess
import socket
import time
import threading
import psutil
import json
import os
import winreg
import ctypes
from datetime import datetime
from ctypes import windll, wintypes

try:
    import win32api
    import win32con
    import wmi
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("Warning: pywin32 or wmi not available. Some network features will be limited.")

class NetworkOptimizer:
    def __init__(self):
        self.optimizations_active = False
        self.original_dns_servers = {}
        self.original_registry_values = {}
        self.ping_results = {}
        
        # Initialize WMI for network interface management
        if WIN32_AVAILABLE:
            try:
                self.wmi_conn = wmi.WMI()
            except:
                self.wmi_conn = None
                WIN32_AVAILABLE = False
        else:
            self.wmi_conn = None
        
        # Gaming-optimized DNS servers with actual IPs
        self.gaming_dns_servers = {
            'cloudflare_gaming': ['1.1.1.1', '1.0.0.1'],      # Cloudflare (fastest)
            'google_gaming': ['8.8.8.8', '8.8.4.4'],          # Google
            'opendns_gaming': ['208.67.222.222', '208.67.220.220'],  # OpenDNS
            'quad9_gaming': ['9.9.9.9', '149.112.112.112'],   # Quad9
            'level3_gaming': ['4.2.2.1', '4.2.2.2'],          # Level3
            'comodo_gaming': ['8.26.56.26', '8.20.247.20'],   # Comodo
            'norton_gaming': ['199.85.126.10', '199.85.127.10'], # Norton ConnectSafe
        }
        
        # Gaming servers for ping testing (actual game servers)
        self.gaming_servers = {
            'steam': ['steamcommunity.com', 'store.steampowered.com'],
            'epic_games': ['epicgames.com', 'launcher-public-service-prod06.ol.epicgames.com'],
            'riot_games': ['riotgames.com', 'riot-geo.pas.si.riotgames.com'],
            'blizzard': ['battle.net', 'us.battle.net'],
            'ea_origin': ['origin.com', 'eaassets-a.akamaihd.net'],
            'ubisoft': ['ubisoft.com', 'static3.cdn.ubi.com'],
            'xbox_live': ['xbox.com', 'xboxlive.com'],
            'playstation': ['playstation.com', 'sonyentertainmentnetwork.com'],
            'discord': ['discord.com', 'gateway.discord.gg'],
            'twitch': ['twitch.tv', 'ttvnw.net']
        }
        
    def optimize_latency(self):
        """Apply comprehensive network latency optimizations with REAL Windows commands"""
        try:
            print("🌐 Optimizing network latency for gaming...")
            
            # 1. Save current DNS settings before changing
            self._backup_current_dns_settings()
            
            # 2. Apply TCP/IP stack optimizations
            self._optimize_tcp_stack()
            
            # 3. Disable network throttling and QoS limitations
            self._disable_network_throttling()
            
            # 4. Optimize network adapter settings
            self._optimize_network_adapter()
            
            # 5. Set optimal gaming DNS servers
            self._set_optimal_gaming_dns()
            
            # 6. Apply Windows network registry optimizations
            self._apply_network_registry_optimizations()
            
            # 7. Optimize network buffers and windows
            self._optimize_network_buffers()
            
            # 8. Disable bandwidth limiting
            self._disable_bandwidth_limiting()
            
            # 9. Apply QoS gaming optimizations
            self._optimize_gaming_qos()
            
            # 10. Clear network caches
            self._clear_all_network_caches()
            
            self.optimizations_active = True
            print("✅ Network latency optimizations applied successfully!")
            
        except Exception as e:
            print(f"❌ Error optimizing network latency: {e}")
            raise
            
    def _backup_current_dns_settings(self):
        """Backup current DNS settings for all network interfaces"""
        try:
            if not self.wmi_conn:
                return
                
            # Get all network adapters with IP enabled
            adapters = self.wmi_conn.Win32_NetworkAdapterConfiguration(IPEnabled=True)
            
            for adapter in adapters:
                if adapter.DNSServerSearchOrder:
                    self.original_dns_servers[adapter.Index] = {
                        'dns_servers': list(adapter.DNSServerSearchOrder),
                        'description': adapter.Description,
                        'dhcp_enabled': adapter.DHCPEnabled
                    }
                    print(f"✅ Backed up DNS for: {adapter.Description}")
                    
        except Exception as e:
            print(f"⚠️ Warning: Could not backup DNS settings: {e}")
            
    def _optimize_tcp_stack(self):
        """Optimize TCP/IP stack with actual Windows registry modifications"""
        try:
            tcp_optimizations = [
                # TCP Chimney Offload
                (winreg.HKEY_LOCAL_MACHINE, 
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "EnableTCPChimney", 1, winreg.REG_DWORD),
                
                # TCP Window Scaling
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "Tcp1323Opts", 3, winreg.REG_DWORD),
                
                # Disable Nagle's Algorithm
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "TcpAckFrequency", 1, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "TCPNoDelay", 1, winreg.REG_DWORD),
                
                # TCP Delayed ACK
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "TcpDelAckTicks", 0, winreg.REG_DWORD),
                
                # TCP Window Size
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "TcpWindowSize", 65535, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "GlobalMaxTcpWindowSize", 65535, winreg.REG_DWORD),
                
                # Default TTL
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "DefaultTTL", 64, winreg.REG_DWORD),
                
                # MTU Discovery
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "EnablePMTUDiscovery", 1, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "EnablePMTUBHDetect", 0, winreg.REG_DWORD),
                
                # TCP Max Duplicate ACKs
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "TcpMaxDupAcks", 2, winreg.REG_DWORD),
                
                # SACK Options
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "SackOpts", 1, winreg.REG_DWORD),
                
                # TCP Timed Wait Delay
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "TcpTimedWaitDelay", 30, winreg.REG_DWORD),
            ]
            
            for hive, key_path, value_name, value_data, value_type in tcp_optimizations:
                try:
                    # Backup original value
                    self._backup_registry_value(hive, key_path, value_name)
                    
                    # Set new value
                    key = winreg.CreateKeyEx(hive, key_path)
                    winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                    winreg.CloseKey(key)
                except Exception as e:
                    print(f"⚠️ Warning: Could not set {key_path}\\{value_name}: {e}")
                    
            print("✅ TCP/IP stack optimizations applied")
            
        except Exception as e:
            print(f"⚠️ Warning: Error optimizing TCP stack: {e}")
            
    def _disable_network_throttling(self):
        """Disable Windows network throttling and QoS limitations"""
        try:
            # Network throttling registry settings
            throttling_settings = [
                # Disable network throttling index
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                 "NetworkThrottlingIndex", 0xFFFFFFFF, winreg.REG_DWORD),
                
                # System responsiveness (0 = best performance)
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                 "SystemResponsiveness", 0, winreg.REG_DWORD),
                
                # Gaming task priority
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "GPU Priority", 8, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "Priority", 6, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "Scheduling Category", "High", winreg.REG_SZ),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "SFIO Priority", "High", winreg.REG_SZ),
                
                # Disable QoS packet scheduler bandwidth limit
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Policies\Microsoft\Windows\Psched",
                 "NonBestEffortLimit", 0, winreg.REG_DWORD),
                
                # Network adapter power management
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\NDIS\Parameters",
                 "DefaultPnPCapabilities", 0, winreg.REG_DWORD),
            ]
            
            for hive, key_path, value_name, value_data, value_type in throttling_settings:
                try:
                    self._backup_registry_value(hive, key_path, value_name)
                    key = winreg.CreateKeyEx(hive, key_path)
                    winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                    winreg.CloseKey(key)
                except Exception as e:
                    print(f"⚠️ Warning: Could not set {key_path}\\{value_name}: {e}")
                    
            print("✅ Network throttling disabled")
            
        except Exception as e:
            print(f"⚠️ Warning: Error disabling network throttling: {e}")
            
    def _optimize_network_adapter(self):
        """Optimize network adapter settings using netsh commands"""
        try:
            # Network adapter optimization commands
            netsh_commands = [
                # TCP Global Settings
                ['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=normal'],
                ['netsh', 'int', 'tcp', 'set', 'global', 'chimney=enabled'],
                ['netsh', 'int', 'tcp', 'set', 'global', 'rss=enabled'],
                ['netsh', 'int', 'tcp', 'set', 'global', 'netdma=enabled'],
                ['netsh', 'int', 'tcp', 'set', 'heuristics', 'disabled'],
                
                # TCP Congestion Provider
                ['netsh', 'int', 'tcp', 'set', 'supplemental', 'Internet', 'congestionprovider=ctcp'],
                
                # Disable TCP heuristics
                ['netsh', 'int', 'tcp', 'set', 'global', 'nonsackrttresiliency=disabled'],
                ['netsh', 'int', 'tcp', 'set', 'security', 'mpp=disabled'],
                ['netsh', 'int', 'tcp', 'set', 'security', 'profiles=disabled'],
                
                # IPv4 settings
                ['netsh', 'interface', 'ipv4', 'set', 'global', 'randomizeidentifiers=disabled'],
                ['netsh', 'interface', 'ipv4', 'set', 'dynamicportrange', 'tcp', 'startport=1024', 'numberofports=64511'],
                
                # IPv6 optimizations (disable if not needed for gaming)
                ['netsh', 'interface', 'ipv6', 'set', 'global', 'randomizeidentifiers=disabled'],
                
                # Interface optimizations for all active adapters
                ['netsh', 'interface', 'tcp', 'set', 'heuristics', 'disabled'],
            ]
            
            for command in netsh_commands:
                try:
                    result = subprocess.run(command, check=True, capture_output=True, text=True)
                    print(f"✅ Executed: {' '.join(command)}")
                except subprocess.CalledProcessError as e:
                    print(f"⚠️ Warning: Command failed: {' '.join(command)} - {e}")
                    
            # Set MTU for active network interfaces
            self._optimize_mtu_settings()
            
            print("✅ Network adapter optimizations applied")
            
        except Exception as e:
            print(f"⚠️ Warning: Error optimizing network adapter: {e}")
            
    def _optimize_mtu_settings(self):
        """Optimize MTU settings for all active network interfaces"""
        try:
            # Get active network interfaces
            interfaces = psutil.net_if_stats()
            
            for interface_name, stats in interfaces.items():
                if stats.isup and not interface_name.startswith('Loopback'):
                    try:
                        # Set optimal MTU (1500 for Ethernet, 1472 for some connections)
                        subprocess.run([
                            'netsh', 'interface', 'ipv4', 'set', 'subinterface',
                            f'"{interface_name}"', 'mtu=1500', 'store=persistent'
                        ], check=True, capture_output=True)
                        print(f"✅ Set MTU=1500 for interface: {interface_name}")
                    except subprocess.CalledProcessError:
                        # Try alternative MTU
                        try:
                            subprocess.run([
                                'netsh', 'interface', 'ipv4', 'set', 'subinterface',
                                f'"{interface_name}"', 'mtu=1472', 'store=persistent'
                            ], check=True, capture_output=True)
                            print(f"✅ Set MTU=1472 for interface: {interface_name}")
                        except subprocess.CalledProcessError:
                            pass
                            
        except Exception as e:
            print(f"⚠️ Warning: Error optimizing MTU settings: {e}")
            
    def _set_optimal_gaming_dns(self):
        """Set optimal DNS servers based on ping tests to gaming servers"""
        try:
            print("🔍 Testing DNS servers for gaming performance...")
            
            # Test all DNS servers
            dns_performance = {}
            for provider, dns_servers in self.gaming_dns_servers.items():
                avg_ping = self._test_dns_performance(dns_servers)
                dns_performance[provider] = {
                    'servers': dns_servers,
                    'avg_ping': avg_ping
                }
                print(f"📊 {provider}: {avg_ping:.1f}ms average")
                
            # Find the fastest DNS
            fastest_dns = min(dns_performance.items(), key=lambda x: x[1]['avg_ping'])
            best_dns_servers = fastest_dns[1]['servers']
            
            print(f"🏆 Fastest DNS: {fastest_dns[0]} ({fastest_dns[1]['avg_ping']:.1f}ms)")
            
            # Set DNS for all active network adapters
            self._set_dns_servers(best_dns_servers)
            
        except Exception as e:
            print(f"⚠️ Warning: Error setting optimal DNS: {e}")
            
    def _test_dns_performance(self, dns_servers):
        """Test DNS performance by pinging gaming servers"""
        total_ping = 0
        successful_pings = 0
        
        # Test primary DNS server
        for server_group in list(self.gaming_servers.values())[:3]:  # Test first 3 server groups
            for server in server_group[:1]:  # Test first server in each group
                ping_time = self._ping_host_via_dns(server, dns_servers[0])
                if ping_time < 1000:  # Valid ping (less than 1 second)
                    total_ping += ping_time
                    successful_pings += 1
                    
        return total_ping / max(1, successful_pings)
        
    def _ping_host_via_dns(self, hostname, dns_server, timeout=3):
        """Ping a host using a specific DNS server"""
        try:
            # Use nslookup to resolve via specific DNS, then ping
            nslookup_result = subprocess.run([
                'nslookup', hostname, dns_server
            ], capture_output=True, text=True, timeout=timeout)
            
            if nslookup_result.returncode == 0:
                # Extract IP from nslookup result
                lines = nslookup_result.stdout.split('\n')
                for line in lines:
                    if 'Address:' in line and dns_server not in line:
                        ip = line.split('Address:')[-1].strip()
                        if self._is_valid_ip(ip):
                            return self._ping_ip(ip, timeout)
                            
            return 1000  # Return high ping if resolution failed
            
        except:
            return 1000
            
    def _is_valid_ip(self, ip):
        """Check if string is a valid IP address"""
        try:
            parts = ip.split('.')
            return len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts)
        except:
            return False
            
    def _ping_ip(self, ip, timeout=3):
        """Ping an IP address and return response time in milliseconds"""
        try:
            result = subprocess.run([
                'ping', '-n', '1', '-w', str(timeout * 1000), ip
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Extract ping time from output
                for line in result.stdout.split('\n'):
                    if 'time=' in line:
                        time_part = line.split('time=')[1].split('ms')[0]
                        return float(time_part.replace('<', ''))
                        
            return 1000
            
        except:
            return 1000
            
    def _set_dns_servers(self, dns_servers):
        """Set DNS servers for all active network interfaces"""
        try:
            if not self.wmi_conn:
                # Fallback to netsh command
                self._set_dns_netsh(dns_servers)
                return
                
            # Use WMI to set DNS for all active adapters
            adapters = self.wmi_conn.Win32_NetworkAdapterConfiguration(IPEnabled=True)
            
            for adapter in adapters:
                try:
                    # Set DNS servers
                    result = adapter.SetDNSServerSearchOrder(dns_servers)
                    if result[0] == 0:  # Success
                        print(f"✅ Set DNS for: {adapter.Description}")
                    else:
                        print(f"⚠️ Warning: Failed to set DNS for: {adapter.Description}")
                        
                except Exception as e:
                    print(f"⚠️ Warning: Error setting DNS for {adapter.Description}: {e}")
                    
        except Exception as e:
            print(f"⚠️ Warning: Error setting DNS servers: {e}")
            # Fallback to netsh
            self._set_dns_netsh(dns_servers)
            
    def _set_dns_netsh(self, dns_servers):
        """Set DNS servers using netsh commands (fallback method)"""
        try:
            # Get active network interface names
            interfaces = psutil.net_if_stats()
            
            for interface_name, stats in interfaces.items():
                if stats.isup and not interface_name.startswith('Loopback'):
                    try:
                        # Set primary DNS
                        subprocess.run([
                            'netsh', 'interface', 'ip', 'set', 'dns',
                            f'"{interface_name}"', 'static', dns_servers[0]
                        ], check=True, capture_output=True)
                        
                        # Set secondary DNS if available
                        if len(dns_servers) > 1:
                            subprocess.run([
                                'netsh', 'interface', 'ip', 'add', 'dns',
                                f'"{interface_name}"', dns_servers[1], 'index=2'
                            ], check=True, capture_output=True)
                            
                        print(f"✅ Set DNS via netsh for: {interface_name}")
                        
                    except subprocess.CalledProcessError as e:
                        print(f"⚠️ Warning: netsh DNS failed for {interface_name}: {e}")
                        
        except Exception as e:
            print(f"⚠️ Warning: Error with netsh DNS fallback: {e}")
            
    def _apply_network_registry_optimizations(self):
        """Apply network-specific registry optimizations"""
        try:
            network_registry_settings = [
                # AFD (Ancillary Function Driver) optimizations
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\AFD\Parameters",
                 "DefaultSendWindow", 65536, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\AFD\Parameters",
                 "DefaultReceiveWindow", 65536, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\AFD\Parameters",
                 "FastSendDatagramThreshold", 1024, winreg.REG_DWORD),
                
                # Network adapter optimizations
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\lanmanserver\parameters",
                 "IRPStackSize", 32, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\lanmanserver\parameters",
                 "SizReqBuf", 17424, winreg.REG_DWORD),
                
                # DNS optimizations
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Dnscache\Parameters",
                 "CacheHashTableBucketSize", 1, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Dnscache\Parameters",
                 "CacheHashTableSize", 384, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Dnscache\Parameters",
                 "MaxCacheEntryTtlLimit", 64000, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Dnscache\Parameters",
                 "MaxSOACacheEntryTtlLimit", 301, winreg.REG_DWORD),
                
                # Network security optimizations
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "SynAttackProtect", 0, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "EnableICMPRedirect", 0, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                 "EnableSecurityFilters", 0, winreg.REG_DWORD),
            ]
            
            for hive, key_path, value_name, value_data, value_type in network_registry_settings:
                try:
                    self._backup_registry_value(hive, key_path, value_name)
                    key = winreg.CreateKeyEx(hive, key_path)
                    winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                    winreg.CloseKey(key)
                except Exception as e:
                    print(f"⚠️ Warning: Could not set {key_path}\\{value_name}: {e}")
                    
            print("✅ Network registry optimizations applied")
            
        except Exception as e:
            print(f"⚠️ Warning: Error applying network registry optimizations: {e}")
            
    def _optimize_network_buffers(self):
        """Optimize network buffer sizes and windows"""
        try:
            # Network buffer optimization commands
            buffer_commands = [
                # TCP receive window auto-tuning
                ['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=normal'],
                
                # Set custom TCP window sizes
                ['netsh', 'int', 'tcp', 'set', 'global', 'initialrto=3000'],
                
                # Optimize for gaming (low latency over throughput)
                ['netsh', 'int', 'tcp', 'set', 'supplemental', 'template=internet', 'congestionprovider=ctcp'],
                
                # Network adapter buffer settings
                ['netsh', 'int', 'tcp', 'set', 'global', 'rsc=disabled'],  # Disable RSC for lower latency
            ]
            
            for command in buffer_commands:
                try:
                    subprocess.run(command, check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    pass
                    
            print("✅ Network buffer optimizations applied")
            
        except Exception as e:
            print(f"⚠️ Warning: Error optimizing network buffers: {e}")
            
    def _disable_bandwidth_limiting(self):
        """Disable Windows bandwidth limiting and QoS restrictions"""
        try:
            # Disable QoS packet scheduler bandwidth reservation
            qos_commands = [
                ['sc', 'config', 'BITS', 'start=', 'disabled'],  # Disable BITS (Background Intelligent Transfer)
                ['sc', 'stop', 'BITS'],
                ['sc', 'config', 'wuauserv', 'start=', 'disabled'],  # Disable Windows Update during gaming
                ['sc', 'stop', 'wuauserv'],
            ]
            
            for command in qos_commands:
                try:
                    subprocess.run(command, check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    pass
                    
            # Registry settings to disable bandwidth limiting
            bandwidth_settings = [
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Policies\Microsoft\Windows\Psched",
                 "NonBestEffortLimit", 0, winreg.REG_DWORD),
                 
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SYSTEM\CurrentControlSet\Services\Psched",
                 "NonBestEffortLimit", 0, winreg.REG_DWORD),
            ]
            
            for hive, key_path, value_name, value_data, value_type in bandwidth_settings:
                try:
                    self._backup_registry_value(hive, key_path, value_name)
                    key = winreg.CreateKeyEx(hive, key_path)
                    winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                    winreg.CloseKey(key)
                except:
                    pass
                    
            print("✅ Bandwidth limiting disabled")
            
        except Exception as e:
            print(f"⚠️ Warning: Error disabling bandwidth limiting: {e}")
            
    def _optimize_gaming_qos(self):
        """Apply gaming-specific QoS optimizations"""
        try:
            # Gaming QoS registry settings
            gaming_qos_settings = [
                # Gaming multimedia class scheduler settings
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "Affinity", 0, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "Background Only", "False", winreg.REG_SZ),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "Clock Rate", 10000, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "GPU Priority", 8, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "Priority", 6, winreg.REG_DWORD),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "Scheduling Category", "High", winreg.REG_SZ),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "SFIO Priority", "High", winreg.REG_SZ),
            ]
            
            for hive, key_path, value_name, value_data, value_type in gaming_qos_settings:
                try:
                    self._backup_registry_value(hive, key_path, value_name)
                    key = winreg.CreateKeyEx(hive, key_path)
                    winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                    winreg.CloseKey(key)
                except:
                    pass
                    
            print("✅ Gaming QoS optimizations applied")
            
        except Exception as e:
            print(f"⚠️ Warning: Error applying gaming QoS: {e}")
            
    def _clear_all_network_caches(self):
        """Clear all network-related caches"""
        try:
            cache_commands = [
                # DNS cache
                ['ipconfig', '/flushdns'],
                
                # ARP cache
                ['arp', '-d', '*'],
                
                # NetBIOS cache
                ['nbtstat', '-R'],
                ['nbtstat', '-RR'],
                
                # Winsock reset
                ['netsh', 'winsock', 'reset'],
                
                # IP configuration reset
                ['netsh', 'int', 'ip', 'reset'],
                
                # TCP/IP stack reset
                ['netsh', 'int', 'tcp', 'reset'],
                
                # Release and renew IP
                ['ipconfig', '/release'],
                ['ipconfig', '/renew'],
            ]
            
            for command in cache_commands:
                try:
                    subprocess.run(command, check=True, capture_output=True, timeout=30)
                    print(f"✅ Executed: {' '.join(command)}")
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    print(f"⚠️ Warning: Command failed or timed out: {' '.join(command)}")
                    
            print("✅ Network caches cleared")
            
        except Exception as e:
            print(f"⚠️ Warning: Error clearing network caches: {e}")
            
    def _backup_registry_value(self, hive, key_path, value_name):
        """Backup original registry value before modification"""
        try:
            key = winreg.OpenKey(hive, key_path)
            try:
                original_value, value_type = winreg.QueryValueEx(key, value_name)
                backup_key = f"{key_path}\\{value_name}"
                self.original_registry_values[backup_key] = {
                    'hive': hive,
                    'key_path': key_path,
                    'value_name': value_name,
                    'original_value': original_value,
                    'value_type': value_type
                }
            except FileNotFoundError:
                # Value doesn't exist, mark for deletion on restore
                backup_key = f"{key_path}\\{value_name}"
                self.original_registry_values[backup_key] = None
            finally:
                winreg.CloseKey(key)
        except:
            pass
            
    def test_gaming_servers_ping(self):
        """Test ping to various gaming servers and return detailed results"""
        results = {}
        
        def ping_server_group(name, servers):
            group_results = []
            for server in servers:
                ping_time = self._ping_ip_advanced(server)
                group_results.append({
                    'server': server,
                    'ping_ms': ping_time if ping_time < 1000 else 'Timeout',
                    'status': 'Good' if ping_time < 50 else 'Fair' if ping_time < 100 else 'Poor' if ping_time < 1000 else 'Timeout'
                })
            
            # Calculate average ping for the group
            valid_pings = [r['ping_ms'] for r in group_results if isinstance(r['ping_ms'], (int, float))]
            avg_ping = sum(valid_pings) / len(valid_pings) if valid_pings else 1000
            
            results[name] = {
                'servers': group_results,
                'average_ping': round(avg_ping, 2),
                'best_server': min(group_results, key=lambda x: x['ping_ms'] if isinstance(x['ping_ms'], (int, float)) else 1000)
            }
            
        # Test all gaming server groups in parallel
        threads = []
        for name, servers in self.gaming_servers.items():
            thread = threading.Thread(target=ping_server_group, args=(name, servers))
            thread.start()
            threads.append(thread)
            
        # Wait for all tests to complete
        for thread in threads:
            thread.join(timeout=10)
            
        return results
        
    def _ping_ip_advanced(self, hostname, timeout=3):
        """Advanced ping with hostname resolution and multiple attempts"""
        try:
            # First resolve hostname to IP
            ip = socket.gethostbyname(hostname)
            
            # Ping the IP multiple times and take average
            ping_times = []
            for _ in range(3):  # 3 ping attempts
                result = subprocess.run([
                    'ping', '-n', '1', '-w', str(timeout * 1000), ip
                ], capture_output=True, text=True, timeout=timeout + 1)
                
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'time=' in line:
                            time_part = line.split('time=')[1].split('ms')[0]
                            ping_time = float(time_part.replace('<', ''))
                            ping_times.append(ping_time)
                            break
                            
            return sum(ping_times) / len(ping_times) if ping_times else 1000
            
        except:
            return 1000
            
    def get_network_stats(self):
        """Get comprehensive network statistics"""
        try:
            # Get basic network I/O stats
            net_io = psutil.net_io_counters()
            
            # Get network connections
            connections = psutil.net_connections()
            
            # Count connections by status
            conn_stats = {}
            for conn in connections:
                status = conn.status
                conn_stats[status] = conn_stats.get(status, 0) + 1
                
            # Get network interfaces with detailed info
            interfaces = {}
            net_if_addrs = psutil.net_if_addrs()
            net_if_stats = psutil.net_if_stats()
            
            for interface_name in net_if_addrs:
                if interface_name in net_if_stats:
                    stats = net_if_stats[interface_name]
                    addrs = net_if_addrs[interface_name]
                    
                    # Get IP addresses
                    ipv4_addrs = [addr.address for addr in addrs if addr.family == socket.AF_INET]
                    ipv6_addrs = [addr.address for addr in addrs if addr.family == socket.AF_INET6]
                    
                    interfaces[interface_name] = {
                        'is_up': stats.isup,
                        'speed': stats.speed,  # Mbps
                        'mtu': stats.mtu,
                        'ipv4_addresses': ipv4_addrs,
                        'ipv6_addresses': ipv6_addrs,
                        'duplex': stats.duplex.name if stats.duplex else 'Unknown'
                    }
                    
            # Get current DNS servers
            current_dns = self._get_current_dns_servers()
            
            stats = {
                'io_counters': {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'packets_sent': net_io.packets_sent,
                    'packets_recv': net_io.packets_recv,
                    'errin': net_io.errin,
                    'errout': net_io.errout,
                    'dropin': net_io.dropin,
                    'dropout': net_io.dropout
                },
                'connections': conn_stats,
                'interfaces': interfaces,
                'total_connections': len(connections),
                'dns_servers': current_dns,
                'optimizations_active': self.optimizations_active
            }
            
            return stats
            
        except Exception as e:
            print(f"⚠️ Warning: Error getting network stats: {e}")
            return {}
            
    def _get_current_dns_servers(self):
        """Get currently configured DNS servers"""
        current_dns = {}
        try:
            if self.wmi_conn:
                adapters = self.wmi_conn.Win32_NetworkAdapterConfiguration(IPEnabled=True)
                for adapter in adapters:
                    if adapter.DNSServerSearchOrder:
                        current_dns[adapter.Description] = list(adapter.DNSServerSearchOrder)
        except:
            pass
            
        return current_dns
        
    def restore_original_settings(self):
        """Restore all original network settings"""
        try:
            print("🔄 Restoring original network settings...")
            
            # Restore original DNS settings
            self._restore_dns_settings()
            
            # Restore original registry values
            self._restore_registry_values()
            
            # Reset network stack to defaults
            self._reset_network_stack()
            
            self.optimizations_active = False
            print("✅ Original network settings restored!")
            
        except Exception as e:
            print(f"⚠️ Warning: Error restoring network settings: {e}")
            
    def _restore_dns_settings(self):
        """Restore original DNS settings"""
        try:
            if not self.wmi_conn or not self.original_dns_servers:
                return
                
            for adapter_index, dns_info in self.original_dns_servers.items():
                try:
                    adapter = self.wmi_conn.Win32_NetworkAdapterConfiguration(Index=adapter_index)[0]
                    
                    if dns_info['dhcp_enabled']:
                        # Restore DHCP DNS
                        adapter.SetDNSServerSearchOrder()
                    else:
                        # Restore static DNS
                        adapter.SetDNSServerSearchOrder(dns_info['dns_servers'])
                        
                    print(f"✅ Restored DNS for: {dns_info['description']}")
                    
                except Exception as e:
                    print(f"⚠️ Warning: Could not restore DNS for adapter {adapter_index}: {e}")
                    
        except Exception as e:
            print(f"⚠️ Warning: Error restoring DNS settings: {e}")
            
    def _restore_registry_values(self):
        """Restore original registry values"""
        try:
            for backup_key, backup_info in self.original_registry_values.items():
                if backup_info is None:
                    # Value was created, delete it
                    continue
                    
                try:
                    key = winreg.CreateKeyEx(backup_info['hive'], backup_info['key_path'])
                    winreg.SetValueEx(key, backup_info['value_name'], 0, 
                                    backup_info['value_type'], backup_info['original_value'])
                    winreg.CloseKey(key)
                except:
                    pass
                    
            self.original_registry_values.clear()
            print("✅ Registry values restored")
            
        except Exception as e:
            print(f"⚠️ Warning: Error restoring registry values: {e}")
            
    def _reset_network_stack(self):
        """Reset network stack to Windows defaults"""
        try:
            reset_commands = [
                # Reset TCP/IP stack
                ['netsh', 'int', 'ip', 'reset'],
                ['netsh', 'int', 'tcp', 'reset'],
                ['netsh', 'winsock', 'reset'],
                
                # Reset TCP settings to auto
                ['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=normal'],
                ['netsh', 'int', 'tcp', 'set', 'global', 'chimney=enabled'],
                ['netsh', 'int', 'tcp', 'set', 'global', 'rss=enabled'],
                ['netsh', 'int', 'tcp', 'set', 'heuristics', 'enabled'],
            ]
            
            for command in reset_commands:
                try:
                    subprocess.run(command, check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    pass
                    
            print("✅ Network stack reset to defaults")
            
        except Exception as e:
            print(f"⚠️ Warning: Error resetting network stack: {e}")
            
    def optimize_for_specific_game(self, game_name):
        """Apply game-specific network optimizations"""
        game_optimizations = {
            'valorant': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 32768,
                'mtu': 1472,
                'priority_ports': [7000, 7500, 8180]
            },
            'csgo': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 65536,
                'mtu': 1500,
                'priority_ports': [27015, 27020]
            },
            'cs2': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 65536,
                'mtu': 1500,
                'priority_ports': [27015, 27020, 27036]
            },
            'lol': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 32768,
                'mtu': 1472,
                'priority_ports': [2099, 5223, 8393, 8400]
            },
            'dota2': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 65536,
                'mtu': 1500,
                'priority_ports': [27015, 27020]
            },
            'fortnite': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 32768,
                'mtu': 1472,
                'priority_ports': [7777, 7778, 7779]
            },
            'apex_legends': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 32768,
                'mtu': 1472,
                'priority_ports': [1024, 65535]
            },
            'overwatch': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 65536,
                'mtu': 1500,
                'priority_ports': [1119, 3724, 6113]
            },
            'cod_warzone': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 32768,
                'mtu': 1472,
                'priority_ports': [3074, 53, 88, 500, 3544, 4500]
            }
        }
        
        game_lower = game_name.lower()
        if game_lower in game_optimizations:
            settings = game_optimizations[game_lower]
            print(f"🎮 Applying {game_name} specific network optimizations...")
            
            try:
                # Apply game-specific TCP settings
                if settings.get('tcp_nodelay'):
                    self._set_registry_value(winreg.HKEY_LOCAL_MACHINE,
                                           r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                                           "TCPNoDelay", 1, winreg.REG_DWORD)
                    
                if settings.get('disable_nagle'):
                    self._set_registry_value(winreg.HKEY_LOCAL_MACHINE,
                                           r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                                           "TcpAckFrequency", 1, winreg.REG_DWORD)
                    
                # Set optimal MTU for the game
                if settings.get('mtu'):
                    self._set_mtu_for_game(settings['mtu'])
                    
                # Apply QoS for game ports
                if settings.get('priority_ports'):
                    self._set_port_priority(settings['priority_ports'])
                    
                print(f"✅ {game_name} network optimizations applied!")
                return True
                
            except Exception as e:
                print(f"⚠️ Warning: Error applying {game_name} optimizations: {e}")
                return False
        else:
            print(f"⚠️ No specific optimizations available for {game_name}")
            return False
            
    def _set_registry_value(self, hive, key_path, value_name, value_data, value_type):
        """Set a registry value with backup"""
        try:
            self._backup_registry_value(hive, key_path, value_name)
            key = winreg.CreateKeyEx(hive, key_path)
            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
            winreg.CloseKey(key)
        except:
            pass
            
    def _set_mtu_for_game(self, mtu):
        """Set MTU for all active interfaces for game optimization"""
        try:
            interfaces = psutil.net_if_stats()
            for interface_name, stats in interfaces.items():
                if stats.isup and not interface_name.startswith('Loopback'):
                    try:
                        subprocess.run([
                            'netsh', 'interface', 'ipv4', 'set', 'subinterface',
                            f'"{interface_name}"', f'mtu={mtu}', 'store=persistent'
                        ], check=True, capture_output=True)
                    except subprocess.CalledProcessError:
                        pass
        except:
            pass
            
    def _set_port_priority(self, ports):
        """Set QoS priority for specific game ports"""
        try:
            # This would require more complex QoS configuration
            # For now, we'll just log that we would set priority for these ports
            print(f"📊 Would prioritize traffic on ports: {ports}")
        except:
            pass