# GameBoost Pro - Advanced System Monitor & Gaming Optimizer

![GameBoost Pro](assets/icon.png)

**GameBoost Pro** is a comprehensive Windows application designed to monitor system performance and optimize your gaming experience. It provides real-time monitoring of CPU, GPU, RAM, disk, and network usage, along with powerful gaming optimization features similar to ExitLag and other gaming boosters.

## 🚀 Features

### System Monitoring
- **Real-time Performance Monitoring**: Track CPU, GPU, RAM, disk, and network usage
- **Interactive Performance Graphs**: Visual representation of system performance over time  
- **Process Management**: Monitor top processes by CPU and memory usage
- **Temperature Monitoring**: Keep track of CPU and GPU temperatures
- **System Information**: Detailed hardware and system information

### Gaming Optimization
- **Gaming Boost Mode**: One-click optimization for gaming performance
- **Process Priority Management**: Automatically prioritize gaming processes
- **CPU Affinity Optimization**: Allocate CPU cores for optimal gaming performance
- **Memory Cleanup**: Free up system memory for better gaming performance
- **Background Process Management**: Pause non-essential processes during gaming

### Network Optimization
- **Latency Reduction**: Optimize network settings to reduce gaming latency
- **DNS Optimization**: Automatically select the fastest DNS servers
- **TCP/IP Stack Optimization**: Fine-tune network stack for gaming
- **Network Throttling Removal**: Disable Windows network throttling
- **Gaming Server Ping Tests**: Test connectivity to popular gaming servers

### User Interface
- **Modern Dark Theme**: Easy on the eyes during long gaming sessions
- **Tabbed Interface**: Organized layout with separate tabs for different functions
- **Real-time Updates**: Live updating of all system metrics
- **Customizable Settings**: Extensive configuration options
- **System Tray Support**: Run minimized in system tray

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11 (64-bit recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100MB free space
- **Administrator Privileges**: Required for system optimizations

### Dependencies
The application will automatically install required dependencies:
- Python 3.8 or higher
- psutil (system monitoring)
- customtkinter (modern UI)
- matplotlib (performance graphs)
- numpy (data processing)
- pywin32 (Windows API access)
- wmi (Windows Management Instrumentation)
- GPUtil (GPU monitoring)

## 🛠️ Installation

### Method 1: Executable (Recommended)
1. Download `GameBoostPro.exe` from the releases page
2. Run the executable as Administrator
3. Follow the installation wizard
4. Launch GameBoost Pro from Start Menu or Desktop

### Method 2: From Source
1. Clone or download this repository
2. Run the launcher: `python launcher.py`
3. The launcher will automatically install dependencies
4. The application will start automatically

### Method 3: Manual Installation
```bash
# Clone the repository
git clone https://github.com/gameboostpro/gameboostpro.git
cd gameboostpro

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 🎮 Usage

### Quick Start
1. **Launch** GameBoost Pro as Administrator
2. **Monitor** your system performance in the "System Monitor" tab
3. **Enable** Gaming Boost Mode in the "Gaming Boost" tab before gaming
4. **Optimize** network settings in the "Network Optimizer" tab
5. **Configure** settings in the "Settings" tab

### Gaming Boost Mode
- Click "Enable Boost Mode" before starting your game
- The application will automatically:
  - Set high-performance power plan
  - Prioritize gaming processes
  - Clean up system memory
  - Optimize CPU core allocation
  - Disable unnecessary background services

### Network Optimization
- Click "Optimize Network Latency" to apply network optimizations
- Test ping to gaming servers to monitor connection quality
- Choose optimal DNS servers for better connectivity

### Monitoring
- View real-time system performance graphs
- Monitor top processes consuming resources
- Track system temperatures and usage over time
- Export performance data for analysis

## ⚙️ Configuration

### Settings Options
- **Theme**: Dark/Light theme selection
- **Startup**: Start with Windows option
- **Monitoring**: Update intervals and monitoring options
- **Gaming**: Auto-detection and priority settings
- **Network**: DNS preferences and optimization settings
- **Alerts**: Performance threshold alerts

### Gaming Process Detection
The application automatically detects popular games including:
- Steam games
- Epic Games Launcher games
- Battle.net games
- Origin/EA games
- Ubisoft Connect games
- And many more...

You can add custom game processes in the settings.

## 🔧 Advanced Features

### Process Priority Management
- Automatically set game processes to high priority
- Reduce priority of background applications
- Custom priority settings per application

### CPU Affinity Optimization
- Reserve CPU cores for gaming
- Limit background processes to specific cores
- Optimize multi-core performance

### Memory Management
- Automatic memory cleanup
- Working set optimization
- Standby memory clearing

### Network Optimizations
- TCP/IP stack tuning
- Nagle's algorithm optimization
- Network buffer optimization
- QoS settings optimization

## 📊 Performance Impact

GameBoost Pro is designed to be lightweight:
- **CPU Usage**: < 2% during normal operation
- **Memory Usage**: ~50MB RAM
- **Disk Usage**: Minimal background activity
- **Network**: No unnecessary network traffic

## 🛡️ Safety & Security

- **No Malware**: Clean, open-source code
- **Reversible Changes**: All optimizations can be undone
- **System Backup**: Automatic backup of changed settings
- **Safe Defaults**: Conservative optimization settings

## 🐛 Troubleshooting

### Common Issues

**Application won't start**
- Ensure you're running as Administrator
- Check if all dependencies are installed
- Try running `launcher.py` to install missing dependencies

**Gaming Boost not working**
- Verify Administrator privileges
- Check if antivirus is blocking the application
- Ensure game processes are detected correctly

**Network optimization fails**
- Run as Administrator
- Check Windows firewall settings
- Verify network adapter compatibility

**Performance monitoring inaccurate**
- Update GPU drivers
- Check Windows Performance Toolkit installation
- Verify WMI service is running

### Getting Help
1. Check the troubleshooting section above
2. Review the logs in `%USERPROFILE%\.gameBoostPro\logs\`
3. Create an issue on GitHub with system details
4. Join our community Discord for support

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/gameboostpro/gameboostpro.git
cd gameboostpro

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run the application
python main.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **psutil** - Cross-platform system monitoring
- **CustomTkinter** - Modern tkinter UI
- **matplotlib** - Performance graphing
- **Windows API** - System optimization capabilities

## 📞 Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/gameboostpro/gameboostpro/issues)
- **Documentation**: [Full documentation](https://docs.gameboostpro.com)
- **Community**: [Discord Server](https://discord.gg/gameboostpro)
- **Email**: support@gameboostpro.com

---

**⚠️ Disclaimer**: This software modifies system settings to optimize performance. While all changes are reversible, use at your own risk. Always create a system restore point before using optimization features.

**🎮 Happy Gaming!** - The GameBoost Pro Team