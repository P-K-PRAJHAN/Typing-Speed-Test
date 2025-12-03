#!/usr/bin/env python3
"""
Script to package the Typing Speed Test application as a standalone executable
"""

import subprocess
import sys
import os

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], 
                      check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_pyinstaller():
    """Install PyInstaller if not present"""
    print("Installing PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install PyInstaller")
        return False

def package_application():
    """Package the application as a standalone executable"""
    print("Packaging Typing Speed Test Application...")
    
    # Check if PyInstaller is installed
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("Cannot proceed without PyInstaller")
            return False
    
    # Package the application
    try:
        # Using --windowed to create a GUI application without console window
        # Using --onefile to create a single executable
        # Using --name to specify the executable name
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--windowed",
            "--onefile",
            "--name", "TypingSpeedTest",
            "main.py"
        ]
        
        print("Running PyInstaller...")
        subprocess.run(cmd, check=True)
        print("Application packaged successfully!")
        print("Executable created in the 'dist' folder")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to package application: {e}")
        return False

if __name__ == "__main__":
    if package_application():
        print("\n🎉 Packaging completed successfully!")
        print("You can find the executable in the 'dist' folder")
    else:
        print("\n❌ Packaging failed!")
        sys.exit(1)