"""
GameBoost Pro - Advanced System Monitor and Gaming Optimizer
A comprehensive Windows application for monitoring system performance and optimizing gaming experience.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
import os
import sys
from datetime import datetime
import configparser

# Try to import optional dependencies
try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False
    print("CustomTkinter not available, falling back to standard tkinter")

# Import custom modules
try:
    from src.system_monitor import SystemMonitor
    from src.gaming_optimizer import GamingOptimizer
    from src.network_optimizer import NetworkOptimizer
    from src.ui_components import MonitoringDashboard, SettingsPanel
    from src.config_manager import ConfigManager
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all required modules are in the src/ directory")
    sys.exit(1)

# Set appearance mode and color theme
if CTK_AVAILABLE:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

class GameBoostPro:
    def __init__(self):
        if CTK_AVAILABLE:
            self.root = ctk.CTk()
        else:
            self.root = tk.Tk()
            self.root.configure(bg='#2b2b2b')
            
        self.root.title("GameBoost Pro - System Monitor & Gaming Optimizer")
        self.root.geometry("1200x800")
        
        # Try to set icon if available
        try:
            if os.path.exists("assets/icon.ico"):
                self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # Initialize components
        self.config_manager = ConfigManager()
        self.system_monitor = SystemMonitor()
        self.gaming_optimizer = GamingOptimizer()
        self.network_optimizer = NetworkOptimizer()
        
        # Application state
        self.monitoring_active = False
        self.boost_mode_active = False
        self.monitoring_thread = None
        
        # Initialize UI
        self.setup_ui()
        self.start_monitoring()
        
    def setup_ui(self):
        """Setup the main user interface"""
        if CTK_AVAILABLE:
            # Create main container
            self.main_container = ctk.CTkFrame(self.root)
            self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create tabview
            self.tabview = ctk.CTkTabview(self.main_container)
            self.tabview.pack(fill="both", expand=True)
        else:
            # Fallback to standard tkinter
            self.main_container = tk.Frame(self.root, bg='#2b2b2b')
            self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create notebook for tabs
            self.tabview = ttk.Notebook(self.main_container)
            self.tabview.pack(fill="both", expand=True)
        
        # Add tabs
        if CTK_AVAILABLE:
            self.monitoring_tab = self.tabview.add("System Monitor")
            self.gaming_tab = self.tabview.add("Gaming Boost")
            self.network_tab = self.tabview.add("Network Optimizer")
            self.settings_tab = self.tabview.add("Settings")
        else:
            self.monitoring_tab = tk.Frame(self.tabview, bg='#2b2b2b')
            self.gaming_tab = tk.Frame(self.tabview, bg='#2b2b2b')
            self.network_tab = tk.Frame(self.tabview, bg='#2b2b2b')
            self.settings_tab = tk.Frame(self.tabview, bg='#2b2b2b')
            
            self.tabview.add(self.monitoring_tab, text="System Monitor")
            self.tabview.add(self.gaming_tab, text="Gaming Boost")
            self.tabview.add(self.network_tab, text="Network Optimizer")
            self.tabview.add(self.settings_tab, text="Settings")
        
        # Setup tab contents
        self.setup_monitoring_tab()
        self.setup_gaming_tab()
        self.setup_network_tab()
        self.setup_settings_tab()
        
        # Setup status bar
        self.setup_status_bar()
        
    def setup_monitoring_tab(self):
        """Setup system monitoring dashboard"""
        self.monitoring_dashboard = MonitoringDashboard(self.monitoring_tab, self.system_monitor)
        
    def setup_gaming_tab(self):
        """Setup gaming optimization controls"""
        # Gaming boost controls
        boost_frame = ctk.CTkFrame(self.gaming_tab)
        boost_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(boost_frame, text="Gaming Boost Mode", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        self.boost_button = ctk.CTkButton(
            boost_frame, 
            text="Enable Boost Mode", 
            command=self.toggle_boost_mode,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.boost_button.pack(pady=10)
        
        # Boost status
        self.boost_status_label = ctk.CTkLabel(boost_frame, text="Boost Mode: Disabled", font=ctk.CTkFont(size=12))
        self.boost_status_label.pack(pady=5)
        
        # Gaming optimizations frame
        optimizations_frame = ctk.CTkFrame(self.gaming_tab)
        optimizations_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(optimizations_frame, text="Gaming Optimizations", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Process priority controls
        priority_frame = ctk.CTkFrame(optimizations_frame)
        priority_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(priority_frame, text="Game Process Priority:").pack(side="left", padx=10)
        self.priority_var = ctk.StringVar(value="High")
        priority_menu = ctk.CTkOptionMenu(priority_frame, variable=self.priority_var, 
                                        values=["Low", "Below Normal", "Normal", "Above Normal", "High", "Realtime"])
        priority_menu.pack(side="right", padx=10)
        
        # CPU affinity controls
        affinity_frame = ctk.CTkFrame(optimizations_frame)
        affinity_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(affinity_frame, text="CPU Core Allocation:").pack(side="left", padx=10)
        self.affinity_button = ctk.CTkButton(affinity_frame, text="Configure CPU Cores", 
                                           command=self.configure_cpu_affinity)
        self.affinity_button.pack(side="right", padx=10)
        
        # Memory optimization
        memory_frame = ctk.CTkFrame(optimizations_frame)
        memory_frame.pack(fill="x", padx=10, pady=5)
        
        self.memory_cleanup_button = ctk.CTkButton(memory_frame, text="Clean System Memory", 
                                                 command=self.cleanup_memory)
        self.memory_cleanup_button.pack(pady=10)
        
    def setup_network_tab(self):
        """Setup network optimization controls"""
        # Network optimization frame
        network_frame = ctk.CTkFrame(self.network_tab)
        network_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(network_frame, text="Network Optimization", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        # Ping optimization
        ping_frame = ctk.CTkFrame(network_frame)
        ping_frame.pack(fill="x", padx=10, pady=5)
        
        self.ping_optimize_button = ctk.CTkButton(ping_frame, text="Optimize Network Latency", 
                                                command=self.optimize_network_latency)
        self.ping_optimize_button.pack(pady=10)
        
        # DNS optimization
        dns_frame = ctk.CTkFrame(network_frame)
        dns_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(dns_frame, text="DNS Server:").pack(side="left", padx=10)
        self.dns_var = ctk.StringVar(value="Auto")
        dns_menu = ctk.CTkOptionMenu(dns_frame, variable=self.dns_var, 
                                   values=["Auto", "Google (8.8.8.8)", "Cloudflare (1.1.1.1)", "OpenDNS"])
        dns_menu.pack(side="right", padx=10)
        
        # Network statistics
        stats_frame = ctk.CTkFrame(network_frame)
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(stats_frame, text="Network Statistics", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.network_stats_text = ctk.CTkTextbox(stats_frame, height=200)
        self.network_stats_text.pack(fill="both", expand=True, padx=10, pady=10)
        
    def setup_settings_tab(self):
        """Setup settings and configuration"""
        self.settings_panel = SettingsPanel(self.settings_tab, self.config_manager)
        
    def setup_status_bar(self):
        """Setup status bar at bottom of window"""
        self.status_frame = ctk.CTkFrame(self.root, height=30)
        self.status_frame.pack(fill="x", side="bottom", padx=10, pady=5)
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="Ready")
        self.status_label.pack(side="left", padx=10)
        
        self.time_label = ctk.CTkLabel(self.status_frame, text="")
        self.time_label.pack(side="right", padx=10)
        
    def start_monitoring(self):
        """Start system monitoring in background thread"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            
    def monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Update system statistics
                self.system_monitor.update_stats()
                
                # Update UI in main thread
                self.root.after(0, self.update_monitoring_ui)
                
                # Update time display
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.root.after(0, lambda: self.time_label.configure(text=current_time))
                
                time.sleep(1)  # Update every second
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)  # Wait longer on error
                
    def update_monitoring_ui(self):
        """Update monitoring dashboard UI"""
        if hasattr(self, 'monitoring_dashboard'):
            self.monitoring_dashboard.update_display()
            
    def toggle_boost_mode(self):
        """Toggle gaming boost mode"""
        if not self.boost_mode_active:
            self.enable_boost_mode()
        else:
            self.disable_boost_mode()
            
    def enable_boost_mode(self):
        """Enable gaming boost mode"""
        try:
            self.gaming_optimizer.enable_boost_mode()
            self.boost_mode_active = True
            self.boost_button.configure(text="Disable Boost Mode", fg_color="red")
            self.boost_status_label.configure(text="Boost Mode: Enabled")
            self.status_label.configure(text="Gaming Boost Mode Enabled")
            messagebox.showinfo("Boost Mode", "Gaming boost mode enabled successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enable boost mode: {e}")
            
    def disable_boost_mode(self):
        """Disable gaming boost mode"""
        try:
            self.gaming_optimizer.disable_boost_mode()
            self.boost_mode_active = False
            self.boost_button.configure(text="Enable Boost Mode", fg_color=None)
            self.boost_status_label.configure(text="Boost Mode: Disabled")
            self.status_label.configure(text="Gaming Boost Mode Disabled")
            messagebox.showinfo("Boost Mode", "Gaming boost mode disabled successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to disable boost mode: {e}")
            
    def configure_cpu_affinity(self):
        """Configure CPU core affinity for games"""
        # This would open a dialog to select CPU cores
        messagebox.showinfo("CPU Affinity", "CPU affinity configuration will be implemented in the full version.")
        
    def cleanup_memory(self):
        """Clean up system memory"""
        try:
            freed_memory = self.gaming_optimizer.cleanup_memory()
            messagebox.showinfo("Memory Cleanup", f"Successfully freed {freed_memory:.1f} MB of memory!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cleanup memory: {e}")
            
    def optimize_network_latency(self):
        """Optimize network latency"""
        try:
            self.network_optimizer.optimize_latency()
            messagebox.showinfo("Network Optimization", "Network latency optimization applied!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to optimize network: {e}")
            
    def on_closing(self):
        """Handle application closing"""
        if self.boost_mode_active:
            self.disable_boost_mode()
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        self.root.destroy()
        
    def run(self):
        """Run the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = GameBoostPro()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start: {e}")
        sys.exit(1)