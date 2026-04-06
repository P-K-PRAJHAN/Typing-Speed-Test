#!/usr/bin/env python3
"""
Script to fix numpy/pandas compatibility issues
"""
import subprocess
import sys

def fix_dependencies():
    print("Fixing numpy/pandas compatibility issues...")
    
    # Uninstall problematic packages
    packages_to_uninstall = ['numpy', 'pandas', 'matplotlib']
    for package in packages_to_uninstall:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', package, '-y'])
            print(f"Uninstalled {package}")
        except subprocess.CalledProcessError:
            print(f"Failed to uninstall {package}, continuing...")
    
    # Install compatible versions in correct order
    packages_to_install = [
        'numpy==1.24.3',
        'pandas==2.0.3',
        'matplotlib==3.7.2'
    ]
    
    for package in packages_to_install:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"Installed {package}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")
            return False
    
    print("Dependency fix completed successfully!")
    return True

if __name__ == "__main__":
    fix_dependencies()