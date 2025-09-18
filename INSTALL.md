# GameBoost Pro Installation Guide

This guide provides detailed instructions for installing and setting up GameBoost Pro on your Windows system.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10 (version 1903 or later)
- **Processor**: Intel Core i3 / AMD Ryzen 3 or equivalent
- **Memory**: 4 GB RAM
- **Storage**: 100 MB available space
- **Graphics**: DirectX 11 compatible
- **Network**: Internet connection for initial setup

### Recommended Requirements
- **Operating System**: Windows 11
- **Processor**: Intel Core i5 / AMD Ryzen 5 or better
- **Memory**: 8 GB RAM or more
- **Storage**: 500 MB available space (for logs and data)
- **Graphics**: Dedicated GPU for GPU monitoring features
- **Network**: Broadband internet connection

## Installation Methods

### Method 1: Executable Installer (Recommended)

1. **Download the Installer**
   - Visit the [GameBoost Pro Releases](https://github.com/gameboostpro/gameboostpro/releases) page
   - Download the latest `GameBoostPro_Setup.exe`
   - Verify the file signature (optional but recommended)

2. **Run the Installer**
   - Right-click on `GameBoostPro_Setup.exe`
   - Select "Run as administrator"
   - If Windows SmartScreen appears, click "More info" then "Run anyway"

3. **Installation Process**
   - Choose installation directory (default: `C:\Program Files\GameBoost Pro Team\GameBoost Pro`)
   - Select components to install
   - Choose Start Menu folder
   - Select additional tasks (desktop shortcut, start with Windows)
   - Click "Install" to begin installation

4. **First Launch**
   - Launch GameBoost Pro from Start Menu or Desktop
   - Grant Administrator privileges when prompted
   - Complete the initial setup wizard

### Method 2: Portable Version

1. **Download Portable Version**
   - Download `GameBoostPro_Portable.zip` from releases
   - Extract to your preferred location
   - No installation required

2. **Run the Application**
   - Navigate to extracted folder
   - Right-click on `GameBoostPro.exe`
   - Select "Run as administrator"

### Method 3: From Source Code

1. **Prerequisites**
   - Install Python 3.8 or later from [python.org](https://python.org)
   - Ensure Python is added to PATH
   - Install Git (optional)

2. **Download Source Code**
   ```bash
   # Option A: Using Git
   git clone https://github.com/gameboostpro/gameboostpro.git
   cd gameboostpro
   
   # Option B: Download ZIP
   # Download and extract the ZIP file from GitHub
   ```

3. **Install Dependencies**
   ```bash
   # Using the launcher (recommended)
   python launcher.py
   
   # Or manually install dependencies
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   # Using launcher
   python launcher.py
   
   # Or run directly
   python main.py
   ```

## Post-Installation Setup

### 1. Administrator Privileges
GameBoost Pro requires Administrator privileges for system optimizations:
- Always run as Administrator for full functionality
- Set up permanent Administrator execution:
  1. Right-click on GameBoost Pro shortcut
  2. Select "Properties"
  3. Go to "Compatibility" tab
  4. Check "Run this program as an administrator"
  5. Click "OK"

### 2. Windows Defender / Antivirus
Some antivirus software may flag system optimization tools:
1. Add GameBoost Pro to your antivirus whitelist
2. Add the installation directory to exclusions
3. If using Windows Defender:
   - Open Windows Security
   - Go to Virus & threat protection
   - Add exclusions for GameBoost Pro folder

### 3. Firewall Configuration
Configure Windows Firewall (if needed):
1. Open Windows Defender Firewall
2. Click "Allow an app or feature through Windows Defender Firewall"
3. Click "Change settings" then "Allow another app"
4. Browse and select GameBoost Pro executable
5. Check both "Private" and "Public" networks

### 4. Initial Configuration
1. Launch GameBoost Pro
2. Go to Settings tab
3. Configure your preferences:
   - Enable/disable startup with Windows
   - Set monitoring intervals
   - Configure gaming process detection
   - Set up network optimization preferences

## Verification

### Check Installation
1. Launch GameBoost Pro
2. Verify all tabs are accessible:
   - System Monitor
   - Gaming Boost
   - Network Optimizer
   - Settings
3. Check that system monitoring data appears
4. Test Gaming Boost mode toggle

### Performance Test
1. Enable Gaming Boost mode
2. Monitor system performance changes
3. Run a game or benchmark tool
4. Verify performance improvements

## Troubleshooting Installation Issues

### Common Installation Problems

**Error: "Windows protected your PC"**
- Click "More info"
- Click "Run anyway"
- This is normal for new software

**Error: "This app can't run on your PC"**
- Ensure you have 64-bit Windows
- Download the correct version for your system

**Error: "Access is denied"**
- Run installer as Administrator
- Disable antivirus temporarily during installation
- Check file permissions

**Error: "Installation failed"**
- Free up disk space
- Close other programs
- Run Windows Update
- Try installing to a different directory

### Dependency Issues

**Missing Python Dependencies**
```bash
# Reinstall all dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Or use the launcher
python launcher.py
```

**Missing System Components**
- Install Visual C++ Redistributable 2019 or later
- Install .NET Framework 4.8 or later
- Update Windows to latest version

**GPU Monitoring Not Working**
- Update GPU drivers
- Install GPU vendor software (NVIDIA GeForce Experience, AMD Adrenalin)
- Check if GPU supports monitoring APIs

### Performance Issues

**High CPU Usage**
- Adjust monitoring interval in settings
- Disable unnecessary monitoring features
- Close other resource-intensive applications

**Slow Startup**
- Add to antivirus exclusions
- Disable startup programs
- Run disk cleanup
- Check for Windows updates

## Uninstallation

### Using Control Panel
1. Open "Apps & Features" in Windows Settings
2. Find "GameBoost Pro"
3. Click "Uninstall"
4. Follow the uninstall wizard

### Manual Removal
1. Delete installation directory
2. Remove shortcuts from Desktop and Start Menu
3. Delete configuration files from `%USERPROFILE%\.gameBoostPro`
4. Remove from Windows startup (if enabled)

### Registry Cleanup (Advanced)
If needed, remove registry entries:
```
HKEY_CURRENT_USER\Software\GameBoost Pro
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GameBoost Pro
```

## Advanced Installation Options

### Silent Installation
For system administrators:
```bash
GameBoostPro_Setup.exe /S /D=C:\Program Files\GameBoost Pro
```

### Custom Installation Directory
```bash
GameBoostPro_Setup.exe /D=C:\Custom\Path\GameBoost Pro
```

### Network Installation
For enterprise deployment:
1. Extract installer to network share
2. Create deployment script
3. Use Group Policy for deployment

## Getting Help

If you encounter issues during installation:

1. **Check System Requirements**: Ensure your system meets minimum requirements
2. **Review Logs**: Check installation logs in `%TEMP%\GameBoostPro_Install.log`
3. **Community Support**: Visit our [Discord server](https://discord.gg/gameboostpro)
4. **GitHub Issues**: Report bugs at [GitHub Issues](https://github.com/gameboostpro/gameboostpro/issues)
5. **Email Support**: Contact support@gameboostpro.com

---

**Note**: Always create a system restore point before installing system optimization software. This allows you to revert changes if needed.