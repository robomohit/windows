"""
UI Components Module
Contains custom UI components for the system monitor and gaming optimizer
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np
import threading
import time

class MonitoringDashboard:
    def __init__(self, parent, system_monitor):
        self.parent = parent
        self.system_monitor = system_monitor
        self.setup_dashboard()
        
    def setup_dashboard(self):
        """Setup the monitoring dashboard UI"""
        # Create main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # System overview section
        self.setup_system_overview()
        
        # Performance graphs section
        self.setup_performance_graphs()
        
        # Process monitor section
        self.setup_process_monitor()
        
        # System information section
        self.setup_system_info()
        
    def setup_system_overview(self):
        """Setup system overview cards"""
        overview_frame = ctk.CTkFrame(self.main_frame)
        overview_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(overview_frame, text="System Overview", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Create grid for overview cards
        cards_frame = ctk.CTkFrame(overview_frame)
        cards_frame.pack(fill="x", padx=10, pady=10)
        
        # CPU Card
        self.cpu_card = self.create_overview_card(cards_frame, "CPU", "0%", "blue")
        self.cpu_card.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Memory Card
        self.memory_card = self.create_overview_card(cards_frame, "Memory", "0%", "green")
        self.memory_card.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # GPU Card
        self.gpu_card = self.create_overview_card(cards_frame, "GPU", "N/A", "orange")
        self.gpu_card.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        # Disk Card
        self.disk_card = self.create_overview_card(cards_frame, "Disk", "0%", "red")
        self.disk_card.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        # Network Card
        self.network_card = self.create_overview_card(cards_frame, "Network", "0 KB/s", "purple")
        self.network_card.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Temperature Card
        self.temp_card = self.create_overview_card(cards_frame, "Temperature", "N/A", "cyan")
        self.temp_card.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        
        # Configure grid weights
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)
        
    def create_overview_card(self, parent, title, value, color):
        """Create an overview card widget"""
        card = ctk.CTkFrame(parent, fg_color=color, corner_radius=10)
        
        title_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(pady=(10, 5))
        
        value_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"))
        value_label.pack(pady=(0, 10))
        
        # Store reference to value label for updates
        card.value_label = value_label
        
        return card
        
    def setup_performance_graphs(self):
        """Setup performance graphs section"""
        graphs_frame = ctk.CTkFrame(self.main_frame)
        graphs_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(graphs_frame, text="Performance Graphs", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(12, 8), dpi=100, facecolor='#2b2b2b')
        self.fig.patch.set_facecolor('#2b2b2b')
        
        # Create subplots
        self.cpu_ax = self.fig.add_subplot(2, 2, 1, facecolor='#2b2b2b')
        self.memory_ax = self.fig.add_subplot(2, 2, 2, facecolor='#2b2b2b')
        self.gpu_ax = self.fig.add_subplot(2, 2, 3, facecolor='#2b2b2b')
        self.network_ax = self.fig.add_subplot(2, 2, 4, facecolor='#2b2b2b')
        
        # Style the plots
        for ax in [self.cpu_ax, self.memory_ax, self.gpu_ax, self.network_ax]:
            ax.set_facecolor('#2b2b2b')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            
        # Initialize plot data
        self.time_data = list(range(60))
        self.cpu_data = [0] * 60
        self.memory_data = [0] * 60
        self.gpu_data = [0] * 60
        self.network_upload_data = [0] * 60
        self.network_download_data = [0] * 60
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, graphs_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Update graphs
        self.update_graphs()
        
    def update_graphs(self):
        """Update performance graphs"""
        try:
            # Get current stats
            stats = self.system_monitor.get_stats()
            
            # Update data arrays
            self.cpu_data.append(stats['cpu']['usage_percent'])
            self.memory_data.append(stats['memory']['percent'])
            self.gpu_data.append(stats['gpu']['usage_percent'])
            self.network_upload_data.append(stats['network']['upload_speed'])
            self.network_download_data.append(stats['network']['download_speed'])
            
            # Keep only last 60 points
            if len(self.cpu_data) > 60:
                self.cpu_data.pop(0)
                self.memory_data.pop(0)
                self.gpu_data.pop(0)
                self.network_upload_data.pop(0)
                self.network_download_data.pop(0)
                
            # Clear and redraw plots
            self.cpu_ax.clear()
            self.memory_ax.clear()
            self.gpu_ax.clear()
            self.network_ax.clear()
            
            # CPU plot
            self.cpu_ax.plot(self.time_data[-len(self.cpu_data):], self.cpu_data, 'cyan', linewidth=2)
            self.cpu_ax.set_title('CPU Usage (%)', color='white', fontsize=12)
            self.cpu_ax.set_ylim(0, 100)
            self.cpu_ax.grid(True, alpha=0.3)
            
            # Memory plot
            self.memory_ax.plot(self.time_data[-len(self.memory_data):], self.memory_data, 'lime', linewidth=2)
            self.memory_ax.set_title('Memory Usage (%)', color='white', fontsize=12)
            self.memory_ax.set_ylim(0, 100)
            self.memory_ax.grid(True, alpha=0.3)
            
            # GPU plot
            self.gpu_ax.plot(self.time_data[-len(self.gpu_data):], self.gpu_data, 'orange', linewidth=2)
            self.gpu_ax.set_title('GPU Usage (%)', color='white', fontsize=12)
            self.gpu_ax.set_ylim(0, 100)
            self.gpu_ax.grid(True, alpha=0.3)
            
            # Network plot
            self.network_ax.plot(self.time_data[-len(self.network_upload_data):], self.network_upload_data, 'red', linewidth=2, label='Upload')
            self.network_ax.plot(self.time_data[-len(self.network_download_data):], self.network_download_data, 'blue', linewidth=2, label='Download')
            self.network_ax.set_title('Network Usage (KB/s)', color='white', fontsize=12)
            self.network_ax.legend()
            self.network_ax.grid(True, alpha=0.3)
            
            # Style all axes
            for ax in [self.cpu_ax, self.memory_ax, self.gpu_ax, self.network_ax]:
                ax.set_facecolor('#2b2b2b')
                ax.tick_params(colors='white')
                for spine in ax.spines.values():
                    spine.set_color('white')
                    
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error updating graphs: {e}")
            
    def setup_process_monitor(self):
        """Setup process monitor section"""
        process_frame = ctk.CTkFrame(self.main_frame)
        process_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(process_frame, text="Top Processes", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Create treeview for processes
        columns = ('PID', 'Name', 'CPU %', 'Memory %')
        self.process_tree = ttk.Treeview(process_frame, columns=columns, show='headings', height=10)
        
        # Configure columns
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=120, anchor='center')
            
        # Add scrollbar
        process_scrollbar = ttk.Scrollbar(process_frame, orient='vertical', command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=process_scrollbar.set)
        
        # Pack treeview and scrollbar
        tree_frame = ctk.CTkFrame(process_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.process_tree.pack(side='left', fill='both', expand=True)
        process_scrollbar.pack(side='right', fill='y')
        
    def setup_system_info(self):
        """Setup system information section"""
        info_frame = ctk.CTkFrame(self.main_frame)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(info_frame, text="System Information", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Create info text widget
        self.info_text = ctk.CTkTextbox(info_frame, height=150, font=ctk.CTkFont(family="Courier", size=11))
        self.info_text.pack(fill="x", padx=10, pady=10)
        
    def update_display(self):
        """Update all dashboard displays"""
        try:
            stats = self.system_monitor.get_stats()
            
            # Update overview cards
            self.cpu_card.value_label.configure(text=f"{stats['cpu']['usage_percent']:.1f}%")
            self.memory_card.value_label.configure(text=f"{stats['memory']['percent']:.1f}%")
            
            if stats['gpu']['available']:
                self.gpu_card.value_label.configure(text=f"{stats['gpu']['usage_percent']:.1f}%")
            else:
                self.gpu_card.value_label.configure(text="N/A")
                
            self.disk_card.value_label.configure(text=f"{stats['disk']['percent']:.1f}%")
            
            network_speed = max(stats['network']['upload_speed'], stats['network']['download_speed'])
            if network_speed > 1024:
                self.network_card.value_label.configure(text=f"{network_speed/1024:.1f} MB/s")
            else:
                self.network_card.value_label.configure(text=f"{network_speed:.1f} KB/s")
                
            if stats['cpu']['temperature'] > 0:
                self.temp_card.value_label.configure(text=f"{stats['cpu']['temperature']:.1f}°C")
            else:
                self.temp_card.value_label.configure(text="N/A")
                
            # Update process list
            self.update_process_list(stats['processes'])
            
            # Update system info
            self.update_system_info(stats)
            
            # Update graphs
            self.update_graphs()
            
        except Exception as e:
            print(f"Error updating display: {e}")
            
    def update_process_list(self, processes):
        """Update the process list"""
        try:
            # Clear existing items
            for item in self.process_tree.get_children():
                self.process_tree.delete(item)
                
            # Add new items
            for proc in processes[:10]:  # Show top 10
                self.process_tree.insert('', 'end', values=(
                    proc['pid'],
                    proc['name'][:20],  # Truncate long names
                    f"{proc['cpu_percent']:.1f}",
                    f"{proc['memory_percent']:.1f}"
                ))
                
        except Exception as e:
            print(f"Error updating process list: {e}")
            
    def update_system_info(self, stats):
        """Update system information display"""
        try:
            info_text = f"""System Information:

CPU:
  Usage: {stats['cpu']['usage_percent']:.1f}%
  Frequency: {stats['cpu']['frequency']:.0f} MHz
  Cores: {stats['cpu']['cores']} physical, {stats['cpu']['threads']} logical
  Temperature: {stats['cpu']['temperature']:.1f}°C

Memory:
  Total: {self.system_monitor.format_bytes(stats['memory']['total'])}
  Used: {self.system_monitor.format_bytes(stats['memory']['used'])} ({stats['memory']['percent']:.1f}%)
  Available: {self.system_monitor.format_bytes(stats['memory']['available'])}
  Swap: {self.system_monitor.format_bytes(stats['memory']['swap_used'])}/{self.system_monitor.format_bytes(stats['memory']['swap_total'])}

Disk:
  Total: {self.system_monitor.format_bytes(stats['disk']['total'])}
  Used: {self.system_monitor.format_bytes(stats['disk']['used'])} ({stats['disk']['percent']:.1f}%)
  Free: {self.system_monitor.format_bytes(stats['disk']['free'])}
  Read Speed: {stats['disk']['read_speed']:.1f} MB/s
  Write Speed: {stats['disk']['write_speed']:.1f} MB/s

Network:
  Upload: {stats['network']['upload_speed']:.1f} KB/s
  Download: {stats['network']['download_speed']:.1f} KB/s
  Bytes Sent: {self.system_monitor.format_bytes(stats['network']['bytes_sent'])}
  Bytes Received: {self.system_monitor.format_bytes(stats['network']['bytes_recv'])}

GPU:
  Available: {stats['gpu']['available']}"""

            if stats['gpu']['available']:
                info_text += f"""
  Name: {stats['gpu']['name']}
  Usage: {stats['gpu']['usage_percent']:.1f}%
  Memory: {stats['gpu']['memory_used']} MB / {stats['gpu']['memory_total']} MB ({stats['gpu']['memory_percent']:.1f}%)
  Temperature: {stats['gpu']['temperature']:.1f}°C"""

            info_text += f"""

System:
  Uptime: {self.system_monitor.format_uptime(stats['system']['uptime'])}
  Active Users: {stats['system']['users']}
  Running Processes: {len(stats['processes'])}"""

            self.info_text.delete("1.0", "end")
            self.info_text.insert("1.0", info_text)
            
        except Exception as e:
            print(f"Error updating system info: {e}")


class SettingsPanel:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager
        self.setup_settings()
        
    def setup_settings(self):
        """Setup the settings panel"""
        # Create main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # General settings
        self.setup_general_settings()
        
        # Monitoring settings
        self.setup_monitoring_settings()
        
        # Gaming settings
        self.setup_gaming_settings()
        
        # Network settings
        self.setup_network_settings()
        
        # Export/Import settings
        self.setup_export_import()
        
    def setup_general_settings(self):
        """Setup general application settings"""
        general_frame = ctk.CTkFrame(self.main_frame)
        general_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(general_frame, text="General Settings", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Theme selection
        theme_frame = ctk.CTkFrame(general_frame)
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(theme_frame, text="Theme:").pack(side="left", padx=10)
        self.theme_var = ctk.StringVar(value="dark")
        theme_menu = ctk.CTkOptionMenu(theme_frame, variable=self.theme_var, 
                                     values=["dark", "light", "system"],
                                     command=self.change_theme)
        theme_menu.pack(side="right", padx=10)
        
        # Start with Windows
        startup_frame = ctk.CTkFrame(general_frame)
        startup_frame.pack(fill="x", padx=10, pady=5)
        
        self.startup_var = ctk.BooleanVar()
        startup_check = ctk.CTkCheckBox(startup_frame, text="Start with Windows", 
                                      variable=self.startup_var,
                                      command=self.toggle_startup)
        startup_check.pack(padx=10, pady=10)
        
        # Minimize to system tray
        tray_frame = ctk.CTkFrame(general_frame)
        tray_frame.pack(fill="x", padx=10, pady=5)
        
        self.tray_var = ctk.BooleanVar(value=True)
        tray_check = ctk.CTkCheckBox(tray_frame, text="Minimize to system tray", 
                                   variable=self.tray_var)
        tray_check.pack(padx=10, pady=10)
        
    def setup_monitoring_settings(self):
        """Setup monitoring-specific settings"""
        monitoring_frame = ctk.CTkFrame(self.main_frame)
        monitoring_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(monitoring_frame, text="Monitoring Settings", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Update interval
        interval_frame = ctk.CTkFrame(monitoring_frame)
        interval_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(interval_frame, text="Update Interval (seconds):").pack(side="left", padx=10)
        self.interval_var = ctk.StringVar(value="1")
        interval_entry = ctk.CTkEntry(interval_frame, textvariable=self.interval_var, width=100)
        interval_entry.pack(side="right", padx=10)
        
        # Temperature monitoring
        temp_frame = ctk.CTkFrame(monitoring_frame)
        temp_frame.pack(fill="x", padx=10, pady=5)
        
        self.temp_monitoring_var = ctk.BooleanVar(value=True)
        temp_check = ctk.CTkCheckBox(temp_frame, text="Enable temperature monitoring", 
                                   variable=self.temp_monitoring_var)
        temp_check.pack(padx=10, pady=10)
        
        # GPU monitoring
        gpu_frame = ctk.CTkFrame(monitoring_frame)
        gpu_frame.pack(fill="x", padx=10, pady=5)
        
        self.gpu_monitoring_var = ctk.BooleanVar(value=True)
        gpu_check = ctk.CTkCheckBox(gpu_frame, text="Enable GPU monitoring", 
                                  variable=self.gpu_monitoring_var)
        gpu_check.pack(padx=10, pady=10)
        
    def setup_gaming_settings(self):
        """Setup gaming optimization settings"""
        gaming_frame = ctk.CTkFrame(self.main_frame)
        gaming_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(gaming_frame, text="Gaming Settings", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Auto-detect games
        autodetect_frame = ctk.CTkFrame(gaming_frame)
        autodetect_frame.pack(fill="x", padx=10, pady=5)
        
        self.autodetect_var = ctk.BooleanVar(value=True)
        autodetect_check = ctk.CTkCheckBox(autodetect_frame, text="Auto-detect gaming processes", 
                                         variable=self.autodetect_var)
        autodetect_check.pack(padx=10, pady=10)
        
        # Gaming priority
        priority_frame = ctk.CTkFrame(gaming_frame)
        priority_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(priority_frame, text="Default Game Priority:").pack(side="left", padx=10)
        self.game_priority_var = ctk.StringVar(value="High")
        priority_menu = ctk.CTkOptionMenu(priority_frame, variable=self.game_priority_var, 
                                        values=["Normal", "Above Normal", "High", "Realtime"])
        priority_menu.pack(side="right", padx=10)
        
        # Memory cleanup
        memory_frame = ctk.CTkFrame(gaming_frame)
        memory_frame.pack(fill="x", padx=10, pady=5)
        
        self.auto_memory_cleanup_var = ctk.BooleanVar(value=True)
        memory_check = ctk.CTkCheckBox(memory_frame, text="Auto memory cleanup when gaming", 
                                     variable=self.auto_memory_cleanup_var)
        memory_check.pack(padx=10, pady=10)
        
    def setup_network_settings(self):
        """Setup network optimization settings"""
        network_frame = ctk.CTkFrame(self.main_frame)
        network_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(network_frame, text="Network Settings", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Auto network optimization
        auto_net_frame = ctk.CTkFrame(network_frame)
        auto_net_frame.pack(fill="x", padx=10, pady=5)
        
        self.auto_network_var = ctk.BooleanVar(value=True)
        auto_net_check = ctk.CTkCheckBox(auto_net_frame, text="Auto network optimization", 
                                       variable=self.auto_network_var)
        auto_net_check.pack(padx=10, pady=10)
        
        # Preferred DNS
        dns_frame = ctk.CTkFrame(network_frame)
        dns_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(dns_frame, text="Preferred DNS:").pack(side="left", padx=10)
        self.dns_preference_var = ctk.StringVar(value="Auto")
        dns_menu = ctk.CTkOptionMenu(dns_frame, variable=self.dns_preference_var, 
                                   values=["Auto", "Cloudflare", "Google", "OpenDNS", "Quad9"])
        dns_menu.pack(side="right", padx=10)
        
    def setup_export_import(self):
        """Setup export/import settings"""
        export_frame = ctk.CTkFrame(self.main_frame)
        export_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(export_frame, text="Backup & Restore", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(export_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        export_button = ctk.CTkButton(buttons_frame, text="Export Settings", 
                                    command=self.export_settings)
        export_button.pack(side="left", padx=10)
        
        import_button = ctk.CTkButton(buttons_frame, text="Import Settings", 
                                    command=self.import_settings)
        import_button.pack(side="right", padx=10)
        
        # Reset button
        reset_button = ctk.CTkButton(buttons_frame, text="Reset to Defaults", 
                                   command=self.reset_settings,
                                   fg_color="red")
        reset_button.pack(pady=10)
        
    def change_theme(self, theme):
        """Change application theme"""
        ctk.set_appearance_mode(theme)
        
    def toggle_startup(self):
        """Toggle startup with Windows"""
        # This would implement Windows registry changes for startup
        pass
        
    def export_settings(self):
        """Export current settings to file"""
        # This would implement settings export
        pass
        
    def import_settings(self):
        """Import settings from file"""
        # This would implement settings import
        pass
        
    def reset_settings(self):
        """Reset all settings to defaults"""
        # This would reset all settings
        pass


class SystemTrayIcon:
    """System tray icon for the application"""
    def __init__(self, app):
        self.app = app
        # This would implement system tray functionality
        pass