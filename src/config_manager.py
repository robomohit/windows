"""
Configuration Manager Module
Handles loading, saving, and managing application configuration
"""

import json
import os
import configparser
from datetime import datetime

class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.join(os.path.expanduser("~"), ".gameBoostPro")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.backup_dir = os.path.join(self.config_dir, "backups")
        
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Default configuration
        self.default_config = {
            "general": {
                "theme": "dark",
                "start_with_windows": False,
                "minimize_to_tray": True,
                "check_for_updates": True,
                "language": "en"
            },
            "monitoring": {
                "update_interval": 1.0,
                "enable_temperature_monitoring": True,
                "enable_gpu_monitoring": True,
                "enable_network_monitoring": True,
                "history_size": 60,
                "auto_export_stats": False,
                "export_interval": 300  # 5 minutes
            },
            "gaming": {
                "auto_detect_games": True,
                "default_game_priority": "High",
                "auto_memory_cleanup": True,
                "auto_boost_mode": False,
                "cpu_affinity_optimization": True,
                "disable_windows_game_bar": True,
                "gaming_process_names": [
                    "steam.exe", "steamwebhelper.exe",
                    "origin.exe", "originwebhelperservice.exe",
                    "epicgameslauncher.exe", "unrealcefsubprocess.exe",
                    "battle.net.exe", "agent.exe",
                    "uplay.exe", "uplayservice.exe",
                    "gog.com.exe", "goggalaxy.exe",
                    "csgo.exe", "dota2.exe", "pubg.exe", "fortnite.exe",
                    "apex_legends.exe", "valorant.exe", "overwatch.exe",
                    "minecraft.exe", "wow.exe", "lol.exe"
                ]
            },
            "network": {
                "auto_network_optimization": True,
                "preferred_dns": "Auto",
                "enable_tcp_optimization": True,
                "enable_gaming_mode_network": True,
                "ping_test_servers": [
                    "google.com",
                    "cloudflare.com",
                    "steam.com",
                    "riot.com"
                ],
                "custom_dns_servers": {
                    "primary": "",
                    "secondary": ""
                }
            },
            "alerts": {
                "enable_high_cpu_alert": True,
                "cpu_alert_threshold": 90.0,
                "enable_high_memory_alert": True,
                "memory_alert_threshold": 85.0,
                "enable_high_temperature_alert": True,
                "temperature_alert_threshold": 80.0,
                "enable_low_disk_alert": True,
                "disk_alert_threshold": 10.0
            },
            "ui": {
                "window_width": 1200,
                "window_height": 800,
                "window_x": -1,  # -1 means center
                "window_y": -1,  # -1 means center
                "always_on_top": False,
                "show_splash_screen": True,
                "graph_colors": {
                    "cpu": "#00FFFF",
                    "memory": "#00FF00",
                    "gpu": "#FFA500",
                    "network_up": "#FF0000",
                    "network_down": "#0000FF"
                }
            },
            "advanced": {
                "debug_mode": False,
                "log_level": "INFO",
                "max_log_files": 5,
                "enable_crash_reporting": True,
                "performance_mode": "Balanced"  # Balanced, Performance, Power Saver
            }
        }
        
        # Load configuration
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    
                # Merge with defaults to ensure all keys exist
                config = self.merge_config(self.default_config, loaded_config)
                return config
            else:
                # Create default config file
                self.save_config(self.default_config)
                return self.default_config.copy()
                
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()
            
    def save_config(self, config=None):
        """Save configuration to file"""
        try:
            if config is None:
                config = self.config
                
            # Create backup before saving
            self.create_backup()
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
            
    def merge_config(self, default, loaded):
        """Merge loaded config with default config to ensure all keys exist"""
        merged = default.copy()
        
        for key, value in loaded.items():
            if key in merged:
                if isinstance(value, dict) and isinstance(merged[key], dict):
                    merged[key] = self.merge_config(merged[key], value)
                else:
                    merged[key] = value
                    
        return merged
        
    def get(self, section, key=None, default=None):
        """Get configuration value"""
        try:
            if key is None:
                return self.config.get(section, default)
            else:
                return self.config.get(section, {}).get(key, default)
        except:
            return default
            
    def set(self, section, key, value):
        """Set configuration value"""
        try:
            if section not in self.config:
                self.config[section] = {}
            self.config[section][key] = value
            return True
        except:
            return False
            
    def get_section(self, section):
        """Get entire configuration section"""
        return self.config.get(section, {})
        
    def set_section(self, section, values):
        """Set entire configuration section"""
        self.config[section] = values
        
    def create_backup(self):
        """Create backup of current configuration"""
        try:
            if os.path.exists(self.config_file):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(self.backup_dir, f"config_backup_{timestamp}.json")
                
                with open(self.config_file, 'r') as src:
                    with open(backup_file, 'w') as dst:
                        dst.write(src.read())
                        
                # Clean old backups (keep only last 10)
                self.cleanup_backups()
                
                return backup_file
                
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None
            
    def cleanup_backups(self, max_backups=10):
        """Clean up old backup files"""
        try:
            backup_files = []
            for file in os.listdir(self.backup_dir):
                if file.startswith("config_backup_") and file.endswith(".json"):
                    file_path = os.path.join(self.backup_dir, file)
                    backup_files.append((file_path, os.path.getctime(file_path)))
                    
            # Sort by creation time (newest first)
            backup_files.sort(key=lambda x: x[1], reverse=True)
            
            # Remove old backups
            for file_path, _ in backup_files[max_backups:]:
                os.remove(file_path)
                
        except Exception as e:
            print(f"Error cleaning up backups: {e}")
            
    def restore_backup(self, backup_file):
        """Restore configuration from backup"""
        try:
            if os.path.exists(backup_file):
                with open(backup_file, 'r') as f:
                    backup_config = json.load(f)
                    
                # Validate backup config
                if self.validate_config(backup_config):
                    self.config = backup_config
                    self.save_config()
                    return True
                    
        except Exception as e:
            print(f"Error restoring backup: {e}")
            
        return False
        
    def validate_config(self, config):
        """Validate configuration structure"""
        try:
            required_sections = ["general", "monitoring", "gaming", "network"]
            for section in required_sections:
                if section not in config:
                    return False
            return True
        except:
            return False
            
    def reset_to_defaults(self):
        """Reset configuration to default values"""
        self.config = self.default_config.copy()
        return self.save_config()
        
    def export_config(self, file_path):
        """Export configuration to specified file"""
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "config": self.config
            }
            
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False
            
    def import_config(self, file_path):
        """Import configuration from specified file"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    import_data = json.load(f)
                    
                if "config" in import_data:
                    imported_config = import_data["config"]
                    
                    if self.validate_config(imported_config):
                        # Create backup before importing
                        self.create_backup()
                        
                        # Merge imported config with defaults
                        self.config = self.merge_config(self.default_config, imported_config)
                        self.save_config()
                        return True
                        
        except Exception as e:
            print(f"Error importing config: {e}")
            
        return False
        
    def get_gaming_processes(self):
        """Get list of gaming process names"""
        return self.get("gaming", "gaming_process_names", [])
        
    def add_gaming_process(self, process_name):
        """Add a gaming process name to the list"""
        processes = self.get_gaming_processes()
        if process_name.lower() not in [p.lower() for p in processes]:
            processes.append(process_name)
            self.set("gaming", "gaming_process_names", processes)
            return True
        return False
        
    def remove_gaming_process(self, process_name):
        """Remove a gaming process name from the list"""
        processes = self.get_gaming_processes()
        processes = [p for p in processes if p.lower() != process_name.lower()]
        self.set("gaming", "gaming_process_names", processes)
        return True
        
    def get_alert_settings(self):
        """Get alert configuration"""
        return self.get_section("alerts")
        
    def should_show_alert(self, alert_type, current_value):
        """Check if an alert should be shown based on current value"""
        alerts = self.get_alert_settings()
        
        alert_map = {
            "cpu": ("enable_high_cpu_alert", "cpu_alert_threshold"),
            "memory": ("enable_high_memory_alert", "memory_alert_threshold"),
            "temperature": ("enable_high_temperature_alert", "temperature_alert_threshold"),
            "disk": ("enable_low_disk_alert", "disk_alert_threshold")
        }
        
        if alert_type in alert_map:
            enable_key, threshold_key = alert_map[alert_type]
            
            if alerts.get(enable_key, False):
                threshold = alerts.get(threshold_key, 0)
                
                if alert_type == "disk":
                    # For disk, alert when free space is below threshold
                    return current_value <= threshold
                else:
                    # For others, alert when value exceeds threshold
                    return current_value >= threshold
                    
        return False
        
    def get_ui_settings(self):
        """Get UI configuration"""
        return self.get_section("ui")
        
    def get_window_geometry(self):
        """Get window geometry settings"""
        ui = self.get_ui_settings()
        return {
            "width": ui.get("window_width", 1200),
            "height": ui.get("window_height", 800),
            "x": ui.get("window_x", -1),
            "y": ui.get("window_y", -1)
        }
        
    def save_window_geometry(self, width, height, x, y):
        """Save window geometry settings"""
        self.set("ui", "window_width", width)
        self.set("ui", "window_height", height)
        self.set("ui", "window_x", x)
        self.set("ui", "window_y", y)
        
    def get_graph_colors(self):
        """Get graph color settings"""
        ui = self.get_ui_settings()
        return ui.get("graph_colors", {
            "cpu": "#00FFFF",
            "memory": "#00FF00", 
            "gpu": "#FFA500",
            "network_up": "#FF0000",
            "network_down": "#0000FF"
        })