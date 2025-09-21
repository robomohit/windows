"""
GameBoost Pro Launcher
This script handles dependency checking and installation before launching the main application
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time

class DependencyInstaller:
    def __init__(self):
        self.required_packages = [
            ('psutil', 'psutil>=5.9.0'),
            ('customtkinter', 'customtkinter>=5.2.0'),
            ('matplotlib', 'matplotlib>=3.7.0'),
            ('numpy', 'numpy>=1.24.0'),
            ('Pillow', 'Pillow>=10.0.0'),
            ('requests', 'requests>=2.31.0')
        ]
        
        # Windows-specific packages
        if os.name == 'nt':
            self.required_packages.extend([
                ('win32api', 'pywin32'),
                ('wmi', 'wmi>=1.5.1'),
                ('GPUtil', 'GPUtil>=1.4.0')
            ])
        
        self.missing_packages = []
        self.root = None
        
    def check_dependencies(self):
        """Check which dependencies are missing"""
        self.missing_packages = []
        
        for package_name, pip_name in self.required_packages:
            try:
                __import__(package_name)
            except ImportError:
                self.missing_packages.append((package_name, pip_name))
                
        return len(self.missing_packages) == 0
        
    def create_installer_gui(self):
        """Create GUI for dependency installation"""
        self.root = tk.Tk()
        self.root.title("GameBoost Pro - Setup")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="GameBoost Pro Setup", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Message
        if self.missing_packages:
            message = f"Missing {len(self.missing_packages)} required dependencies.\nWould you like to install them automatically?"
        else:
            message = "All dependencies are installed!\nReady to launch GameBoost Pro."
            
        message_label = tk.Label(main_frame, text=message, 
                                font=("Arial", 10), justify="center")
        message_label.pack(pady=(0, 20))
        
        # Package list
        if self.missing_packages:
            list_frame = tk.LabelFrame(main_frame, text="Missing Packages", padx=10, pady=10)
            list_frame.pack(fill="both", expand=True, pady=(0, 20))
            
            # Create listbox with scrollbar
            list_container = tk.Frame(list_frame)
            list_container.pack(fill="both", expand=True)
            
            scrollbar = tk.Scrollbar(list_container)
            scrollbar.pack(side="right", fill="y")
            
            self.package_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set)
            self.package_listbox.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=self.package_listbox.yview)
            
            for package_name, pip_name in self.missing_packages:
                self.package_listbox.insert(tk.END, f"• {package_name} ({pip_name})")
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        progress_label = tk.Label(main_frame, textvariable=self.progress_var)
        progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.pack(fill="x", pady=(5, 20))
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x")
        
        if self.missing_packages:
            install_button = tk.Button(button_frame, text="Install Dependencies", 
                                     command=self.start_installation, 
                                     bg="#4CAF50", fg="white", padx=20)
            install_button.pack(side="left", padx=(0, 10))
            
            skip_button = tk.Button(button_frame, text="Skip & Launch Anyway", 
                                  command=self.launch_app,
                                  bg="#FF9800", fg="white", padx=20)
            skip_button.pack(side="left")
        else:
            launch_button = tk.Button(button_frame, text="Launch GameBoost Pro", 
                                    command=self.launch_app,
                                    bg="#2196F3", fg="white", padx=20)
            launch_button.pack(side="left")
            
        quit_button = tk.Button(button_frame, text="Quit", 
                              command=self.root.quit,
                              padx=20)
        quit_button.pack(side="right")
        
    def start_installation(self):
        """Start dependency installation in background thread"""
        install_thread = threading.Thread(target=self.install_dependencies, daemon=True)
        install_thread.start()
        
    def install_dependencies(self):
        """Install missing dependencies"""
        self.progress_bar.start()
        self.progress_var.set("Installing dependencies...")
        
        try:
            for i, (package_name, pip_name) in enumerate(self.missing_packages):
                self.progress_var.set(f"Installing {package_name}... ({i+1}/{len(self.missing_packages)})")
                
                # Try different installation methods
                success = False
                
                # Method 1: pip install
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", pip_name], 
                                 check=True, capture_output=True)
                    success = True
                except subprocess.CalledProcessError:
                    pass
                
                # Method 2: pip install with --user
                if not success:
                    try:
                        subprocess.run([sys.executable, "-m", "pip", "install", "--user", pip_name], 
                                     check=True, capture_output=True)
                        success = True
                    except subprocess.CalledProcessError:
                        pass
                
                # Method 3: pip install with --break-system-packages (for externally managed environments)
                if not success:
                    try:
                        subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", pip_name], 
                                     check=True, capture_output=True)
                        success = True
                    except subprocess.CalledProcessError:
                        pass
                
                if not success:
                    self.progress_var.set(f"Failed to install {package_name}")
                    messagebox.showerror("Installation Error", 
                                       f"Failed to install {package_name}.\nPlease install manually:\npip install {pip_name}")
                    self.progress_bar.stop()
                    return
                    
            self.progress_var.set("Installation completed successfully!")
            self.progress_bar.stop()
            
            # Update UI
            self.root.after(1000, self.installation_complete)
            
        except Exception as e:
            self.progress_var.set(f"Installation failed: {str(e)}")
            self.progress_bar.stop()
            messagebox.showerror("Installation Error", f"Installation failed: {str(e)}")
            
    def installation_complete(self):
        """Handle installation completion"""
        messagebox.showinfo("Success", "Dependencies installed successfully!\nLaunching GameBoost Pro...")
        self.launch_app()
        
    def launch_app(self):
        """Launch the main application"""
        self.root.destroy()
        
        try:
            # Import and run the main application
            import main
            app = main.GameBoostPro()
            app.run()
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch GameBoost Pro:\n{str(e)}")
            
    def run(self):
        """Run the installer"""
        if self.check_dependencies():
            # All dependencies available, launch directly
            try:
                import main
                app = main.GameBoostPro()
                app.run()
            except Exception as e:
                # Show GUI even if launch fails
                self.create_installer_gui()
                self.root.mainloop()
        else:
            # Show installation GUI
            self.create_installer_gui()
            self.root.mainloop()

class SimpleLauncher:
    """Simple launcher without GUI for command line use"""
    
    def __init__(self):
        self.installer = DependencyInstaller()
        
    def run(self):
        """Run simple command line launcher"""
        print("GameBoost Pro Launcher")
        print("=" * 40)
        
        print("Checking dependencies...")
        if self.installer.check_dependencies():
            print("✓ All dependencies satisfied")
            print("Launching GameBoost Pro...")
            try:
                import main
                app = main.GameBoostPro()
                app.run()
            except Exception as e:
                print(f"✗ Failed to launch: {e}")
                return False
        else:
            print(f"✗ Missing {len(self.installer.missing_packages)} dependencies:")
            for package_name, pip_name in self.installer.missing_packages:
                print(f"  - {package_name} ({pip_name})")
                
            response = input("\nInstall missing dependencies? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                print("Installing dependencies...")
                self.install_dependencies_cli()
            else:
                print("Launching anyway (some features may not work)...")
                try:
                    import main
                    app = main.GameBoostPro()
                    app.run()
                except Exception as e:
                    print(f"✗ Failed to launch: {e}")
                    return False
                    
        return True
        
    def install_dependencies_cli(self):
        """Install dependencies via command line"""
        for package_name, pip_name in self.installer.missing_packages:
            print(f"Installing {package_name}...")
            
            # Try different installation methods
            success = False
            
            for method in [
                [sys.executable, "-m", "pip", "install", pip_name],
                [sys.executable, "-m", "pip", "install", "--user", pip_name],
                [sys.executable, "-m", "pip", "install", "--break-system-packages", pip_name]
            ]:
                try:
                    subprocess.run(method, check=True, capture_output=True)
                    success = True
                    print(f"✓ {package_name} installed successfully")
                    break
                except subprocess.CalledProcessError:
                    continue
                    
            if not success:
                print(f"✗ Failed to install {package_name}")
                print(f"  Please install manually: pip install {pip_name}")
                
        print("\nLaunching GameBoost Pro...")
        try:
            import main
            app = main.GameBoostPro()
            app.run()
        except Exception as e:
            print(f"✗ Failed to launch: {e}")

def main():
    """Main launcher function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Command line mode
        launcher = SimpleLauncher()
        launcher.run()
    else:
        # GUI mode
        installer = DependencyInstaller()
        installer.run()

if __name__ == "__main__":
    main()