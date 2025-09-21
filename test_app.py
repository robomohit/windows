"""
Test script for GameBoost Pro
This script tests the core functionality without requiring the full GUI
"""

import sys
import os
import time

def test_imports():
    """Test if all modules can be imported"""
    print("Testing module imports...")
    
    try:
        # Test core modules
        from src.system_monitor import SystemMonitor
        print("✓ SystemMonitor imported successfully")
        
        from src.gaming_optimizer import GamingOptimizer
        print("✓ GamingOptimizer imported successfully")
        
        from src.network_optimizer import NetworkOptimizer
        print("✓ NetworkOptimizer imported successfully")
        
        from src.config_manager import ConfigManager
        print("✓ ConfigManager imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_system_monitor():
    """Test system monitoring functionality"""
    print("\nTesting system monitoring...")
    
    try:
        monitor = SystemMonitor()
        
        # Update stats
        monitor.update_stats()
        stats = monitor.get_stats()
        
        # Check if we got valid data
        assert stats['cpu']['usage_percent'] >= 0
        assert stats['memory']['total'] > 0
        assert stats['memory']['percent'] >= 0
        
        print("✓ System monitoring working correctly")
        print(f"  - CPU Usage: {stats['cpu']['usage_percent']:.1f}%")
        print(f"  - Memory Usage: {stats['memory']['percent']:.1f}%")
        print(f"  - Total Memory: {monitor.format_bytes(stats['memory']['total'])}")
        
        return True
        
    except Exception as e:
        print(f"✗ System monitor error: {e}")
        return False

def test_config_manager():
    """Test configuration management"""
    print("\nTesting configuration manager...")
    
    try:
        config = ConfigManager()
        
        # Test getting/setting values
        config.set("test", "test_key", "test_value")
        value = config.get("test", "test_key")
        assert value == "test_value"
        
        # Test saving/loading
        config.save_config()
        
        print("✓ Configuration manager working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Config manager error: {e}")
        return False

def test_gaming_optimizer():
    """Test gaming optimizer (limited test)"""
    print("\nTesting gaming optimizer...")
    
    try:
        optimizer = GamingOptimizer()
        
        # Test getting gaming processes (shouldn't crash)
        processes = optimizer.get_gaming_processes()
        print(f"✓ Gaming optimizer initialized (found {len(processes)} gaming processes)")
        
        return True
        
    except Exception as e:
        print(f"✗ Gaming optimizer error: {e}")
        return False

def test_network_optimizer():
    """Test network optimizer (limited test)"""
    print("\nTesting network optimizer...")
    
    try:
        optimizer = NetworkOptimizer()
        
        # Test getting network stats
        stats = optimizer.get_network_stats()
        print("✓ Network optimizer initialized")
        
        return True
        
    except Exception as e:
        print(f"✗ Network optimizer error: {e}")
        return False

def main():
    """Run all tests"""
    print("GameBoost Pro - System Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_system_monitor,
        test_config_manager,
        test_gaming_optimizer,
        test_network_optimizer
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! GameBoost Pro is ready to use.")
        return True
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)