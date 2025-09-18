"""
Network Optimizer Module
Handles network optimizations for gaming including latency reduction, DNS optimization, and traffic shaping
"""

import subprocess
import socket
import time
import threading
import psutil
import json
import os
from datetime import datetime

try:
    import win32api
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

class NetworkOptimizer:
    def __init__(self):
        self.optimizations_active = False
        self.original_dns_servers = []
        self.ping_results = {}
        
        # Gaming-optimized DNS servers
        self.gaming_dns_servers = {
            'cloudflare': ['1.1.1.1', '1.0.0.1'],
            'google': ['8.8.8.8', '8.8.4.4'],
            'opendns': ['208.67.222.222', '208.67.220.220'],
            'quad9': ['9.9.9.9', '149.112.112.112'],
            'level3': ['4.2.2.1', '4.2.2.2']
        }
        
        # Common gaming servers for ping testing
        self.gaming_servers = {
            'steam': 'steamcommunity.com',
            'epic': 'epicgames.com',
            'riot': 'riotgames.com',
            'blizzard': 'battle.net',
            'origin': 'origin.com',
            'uplay': 'ubisoft.com',
            'google': 'google.com',
            'cloudflare': '1.1.1.1'
        }
        
    def optimize_latency(self):
        """Apply comprehensive network latency optimizations"""
        try:
            print("Optimizing network latency...")
            
            # 1. Optimize TCP/IP stack
            self._optimize_tcp_stack()
            
            # 2. Disable network throttling
            self._disable_network_throttling()
            
            # 3. Optimize network adapter settings
            self._optimize_network_adapter()
            
            # 4. Set optimal DNS servers
            self._set_optimal_dns()
            
            # 5. Optimize Windows network settings
            self._optimize_windows_network()
            
            # 6. Clear network caches
            self._clear_network_caches()
            
            # 7. Optimize QoS settings
            self._optimize_qos()
            
            self.optimizations_active = True
            print("Network latency optimizations applied successfully!")
            
        except Exception as e:
            print(f"Error optimizing network latency: {e}")
            raise
            
    def _optimize_tcp_stack(self):
        """Optimize TCP/IP stack for gaming"""
        try:
            # Registry settings for TCP optimization
            tcp_settings = [
                ("TcpAckFrequency", "1"),
                ("TCPNoDelay", "1"),
                ("TcpDelAckTicks", "0"),
                ("TcpWindowSize", "65535"),
                ("DefaultTTL", "64"),
                ("EnablePMTUBHDetect", "0"),
                ("EnablePMTUDiscovery", "1"),
                ("GlobalMaxTcpWindowSize", "65535"),
                ("TcpMaxDupAcks", "2"),
                ("SackOpts", "1"),
                ("Tcp1323Opts", "3"),
                ("TcpTimedWaitDelay", "30")
            ]
            
            base_key = "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters"
            
            for setting, value in tcp_settings:
                try:
                    subprocess.run([
                        "reg", "add", base_key,
                        "/v", setting, "/t", "REG_DWORD", "/d", value, "/f"
                    ], check=True, capture_output=True)
                except:
                    pass
                    
        except Exception as e:
            print(f"Error optimizing TCP stack: {e}")
            
    def _disable_network_throttling(self):
        """Disable Windows network throttling"""
        try:
            # Disable network throttling
            subprocess.run([
                "reg", "add", "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile",
                "/v", "NetworkThrottlingIndex", "/t", "REG_DWORD", "/d", "4294967295", "/f"
            ], check=True, capture_output=True)
            
            # Disable system responsiveness
            subprocess.run([
                "reg", "add", "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile",
                "/v", "SystemResponsiveness", "/t", "REG_DWORD", "/d", "0", "/f"
            ], check=True, capture_output=True)
            
            # Gaming profile optimizations
            subprocess.run([
                "reg", "add", "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games",
                "/v", "GPU Priority", "/t", "REG_DWORD", "/d", "8", "/f"
            ], check=True, capture_output=True)
            
            subprocess.run([
                "reg", "add", "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games",
                "/v", "Priority", "/t", "REG_DWORD", "/d", "6", "/f"
            ], check=True, capture_output=True)
            
        except Exception as e:
            print(f"Error disabling network throttling: {e}")
            
    def _optimize_network_adapter(self):
        """Optimize network adapter settings"""
        try:
            # Netsh commands for network optimization
            netsh_commands = [
                ["netsh", "int", "tcp", "set", "global", "autotuninglevel=normal"],
                ["netsh", "int", "tcp", "set", "global", "chimney=enabled"],
                ["netsh", "int", "tcp", "set", "global", "rss=enabled"],
                ["netsh", "int", "tcp", "set", "global", "netdma=enabled"],
                ["netsh", "int", "tcp", "set", "heuristics", "disabled"],
                ["netsh", "int", "tcp", "set", "supplemental", "Internet", "congestionprovider=ctcp"],
                ["netsh", "interface", "ipv4", "set", "subinterface", "Local Area Connection", "mtu=1500", "store=persistent"]
            ]
            
            for command in netsh_commands:
                try:
                    subprocess.run(command, check=True, capture_output=True)
                except:
                    pass  # Some commands might fail on different systems
                    
        except Exception as e:
            print(f"Error optimizing network adapter: {e}")
            
    def _set_optimal_dns(self):
        """Set optimal DNS servers based on ping tests"""
        try:
            # Test DNS servers to find the fastest
            best_dns = self._find_fastest_dns()
            
            if best_dns:
                # Set DNS servers using netsh
                subprocess.run([
                    "netsh", "interface", "ip", "set", "dns", "Local Area Connection", "static", best_dns[0]
                ], check=True, capture_output=True)
                
                if len(best_dns) > 1:
                    subprocess.run([
                        "netsh", "interface", "ip", "add", "dns", "Local Area Connection", best_dns[1], "index=2"
                    ], check=True, capture_output=True)
                    
                print(f"Set DNS servers to: {', '.join(best_dns)}")
                
        except Exception as e:
            print(f"Error setting optimal DNS: {e}")
            
    def _find_fastest_dns(self):
        """Find the fastest DNS server by testing ping times"""
        best_dns = None
        best_time = float('inf')
        
        for provider, dns_servers in self.gaming_dns_servers.items():
            try:
                # Test primary DNS server
                ping_time = self._ping_host(dns_servers[0])
                if ping_time < best_time:
                    best_time = ping_time
                    best_dns = dns_servers
                    
            except:
                continue
                
        return best_dns
        
    def _ping_host(self, host, timeout=3):
        """Ping a host and return the response time in milliseconds"""
        try:
            start_time = time.time()
            
            # Use socket for cross-platform ping alternative
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, 53))  # DNS port
            sock.close()
            
            end_time = time.time()
            
            if result == 0:
                return (end_time - start_time) * 1000  # Convert to milliseconds
            else:
                return float('inf')
                
        except:
            return float('inf')
            
    def _optimize_windows_network(self):
        """Optimize Windows-specific network settings"""
        try:
            # Disable Large Send Offload
            subprocess.run([
                "reg", "add", "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters",
                "/v", "DisableLargeSendOffload", "/t", "REG_DWORD", "/d", "1", "/f"
            ], check=True, capture_output=True)
            
            # Enable TCP Chimney Offload
            subprocess.run([
                "reg", "add", "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters",
                "/v", "EnableTCPChimney", "/t", "REG_DWORD", "/d", "1", "/f"
            ], check=True, capture_output=True)
            
            # Optimize network buffer sizes
            subprocess.run([
                "reg", "add", "HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters",
                "/v", "DefaultSendWindow", "/t", "REG_DWORD", "/d", "65536", "/f"
            ], check=True, capture_output=True)
            
            subprocess.run([
                "reg", "add", "HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters",
                "/v", "DefaultReceiveWindow", "/t", "REG_DWORD", "/d", "65536", "/f"
            ], check=True, capture_output=True)
            
        except Exception as e:
            print(f"Error optimizing Windows network settings: {e}")
            
    def _clear_network_caches(self):
        """Clear various network caches"""
        try:
            # Clear DNS cache
            subprocess.run(["ipconfig", "/flushdns"], check=True, capture_output=True)
            
            # Clear ARP cache
            subprocess.run(["arp", "-d", "*"], check=True, capture_output=True)
            
            # Clear NetBIOS cache
            subprocess.run(["nbtstat", "-R"], check=True, capture_output=True)
            
            # Reset Winsock
            subprocess.run(["netsh", "winsock", "reset"], check=True, capture_output=True)
            
            print("Network caches cleared successfully!")
            
        except Exception as e:
            print(f"Error clearing network caches: {e}")
            
    def _optimize_qos(self):
        """Optimize Quality of Service settings"""
        try:
            # Disable QoS packet scheduler bandwidth limit
            subprocess.run([
                "reg", "add", "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Psched",
                "/v", "NonBestEffortLimit", "/t", "REG_DWORD", "/d", "0", "/f"
            ], check=True, capture_output=True)
            
            # Gaming traffic prioritization
            subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule",
                "name=Gaming Priority", "dir=out", "action=allow",
                "protocol=any", "profile=any", "interfacetype=any"
            ], check=True, capture_output=True)
            
        except Exception as e:
            print(f"Error optimizing QoS: {e}")
            
    def test_gaming_servers_ping(self):
        """Test ping to various gaming servers"""
        results = {}
        
        def ping_server(name, host):
            ping_time = self._ping_host(host)
            results[name] = {
                'host': host,
                'ping_ms': round(ping_time, 2) if ping_time != float('inf') else 'Timeout'
            }
            
        threads = []
        for name, host in self.gaming_servers.items():
            thread = threading.Thread(target=ping_server, args=(name, host))
            thread.start()
            threads.append(thread)
            
        # Wait for all ping tests to complete
        for thread in threads:
            thread.join(timeout=5)
            
        return results
        
    def get_network_stats(self):
        """Get current network statistics"""
        try:
            # Get network interface statistics
            net_io = psutil.net_io_counters()
            
            # Get network connections
            connections = psutil.net_connections()
            
            # Count connections by status
            conn_stats = {}
            for conn in connections:
                status = conn.status
                conn_stats[status] = conn_stats.get(status, 0) + 1
                
            # Get network interfaces
            interfaces = psutil.net_if_addrs()
            
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
                'interfaces': list(interfaces.keys()),
                'total_connections': len(connections)
            }
            
            return stats
            
        except Exception as e:
            print(f"Error getting network stats: {e}")
            return {}
            
    def monitor_network_latency(self, duration=60):
        """Monitor network latency over time"""
        results = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            timestamp = datetime.now().isoformat()
            
            # Test ping to multiple servers
            ping_results = {}
            for name, host in list(self.gaming_servers.items())[:3]:  # Test first 3 servers
                ping_time = self._ping_host(host, timeout=2)
                ping_results[name] = ping_time if ping_time != float('inf') else None
                
            results.append({
                'timestamp': timestamp,
                'ping_results': ping_results
            })
            
            time.sleep(5)  # Test every 5 seconds
            
        return results
        
    def optimize_for_specific_game(self, game_name):
        """Apply game-specific network optimizations"""
        game_optimizations = {
            'valorant': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 32768
            },
            'csgo': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 65536
            },
            'lol': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 32768
            },
            'dota2': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 65536
            },
            'fortnite': {
                'tcp_nodelay': True,
                'disable_nagle': True,
                'buffer_size': 32768
            }
        }
        
        game_lower = game_name.lower()
        if game_lower in game_optimizations:
            settings = game_optimizations[game_lower]
            print(f"Applying {game_name} specific optimizations...")
            
            # Apply game-specific settings
            try:
                if settings.get('tcp_nodelay'):
                    subprocess.run([
                        "reg", "add", "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters",
                        "/v", "TCPNoDelay", "/t", "REG_DWORD", "/d", "1", "/f"
                    ], check=True, capture_output=True)
                    
                if settings.get('disable_nagle'):
                    subprocess.run([
                        "reg", "add", "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters",
                        "/v", "TcpAckFrequency", "/t", "REG_DWORD", "/d", "1", "/f"
                    ], check=True, capture_output=True)
                    
                print(f"{game_name} network optimizations applied!")
                return True
                
            except Exception as e:
                print(f"Error applying {game_name} optimizations: {e}")
                return False
        else:
            print(f"No specific optimizations available for {game_name}")
            return False
            
    def restore_default_settings(self):
        """Restore default network settings"""
        try:
            # Reset network settings to defaults
            subprocess.run(["netsh", "int", "ip", "reset"], check=True, capture_output=True)
            subprocess.run(["netsh", "winsock", "reset"], check=True, capture_output=True)
            
            # Restore DNS to automatic
            subprocess.run([
                "netsh", "interface", "ip", "set", "dns", "Local Area Connection", "dhcp"
            ], check=True, capture_output=True)
            
            self.optimizations_active = False
            print("Network settings restored to defaults!")
            return True
            
        except Exception as e:
            print(f"Error restoring network settings: {e}")
            return False