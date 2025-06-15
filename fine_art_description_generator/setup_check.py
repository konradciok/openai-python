"""
Setup check script for Fine Art Description Generator
This script verifies that all required dependencies are installed correctly.
"""

import sys
import importlib.util
import subprocess
import os

def check_dependency(package_name):
    """Check if a package is installed and return its version."""
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            return False, None
        
        # Try to get the version
        try:
            package = importlib.import_module(package_name)
            version = getattr(package, '__version__', 'unknown')
        except:
            version = 'installed (version unknown)'
        
        return True, version
    except ImportError:
        return False, None

def main():
    """Check all dependencies and print status."""
    print("Fine Art Description Generator - Setup Check")
    print("===========================================")
    
    # List of required packages
    required_packages = [
        'streamlit',
        'openai',
        'dotenv',
        'PIL',  # Pillow
        'requests',
        'numpy'
    ]
    
    all_installed = True
    
    for package in required_packages:
        installed, version = check_dependency(package)
        if installed:
            print(f"✅ {package}: {version}")
        else:
            print(f"❌ {package}: Not installed")
            all_installed = False
    
    print("\nEnvironment Variables:")
    if os.path.exists('.env'):
        print("✅ .env file exists")
        # Check if OPENAI_API_KEY is in the .env file
        with open('.env', 'r') as f:
            if 'OPENAI_API_KEY' in f.read():
                print("✅ OPENAI_API_KEY found in .env file")
            else:
                print("❌ OPENAI_API_KEY not found in .env file")
    else:
        print("❌ .env file not found")
        print("   Create a .env file with your OpenAI API key (see .env.example)")
    
    print("\nSummary:")
    if all_installed:
        print("✅ All required packages are installed")
        print("🚀 You're ready to run the application!")
        print("   Run 'streamlit run app.py' to start")
    else:
        print("❌ Some packages are missing")
        print("   Run 'pip install -r requirements.txt' to install all dependencies")

if __name__ == "__main__":
    main()