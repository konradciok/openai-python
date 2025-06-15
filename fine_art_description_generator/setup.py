"""
Setup script for Fine Art Description Generator
This script helps set up the environment for the application.
"""

import os
import subprocess
import sys
import shutil

def main():
    """Run the setup process."""
    print("Fine Art Description Generator - Setup")
    print("=====================================")
    
    # Check Python version
    python_version = sys.version.split()[0]
    print(f"Python version: {python_version}")
    
    # Install requirements
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("\nSetting up environment variables...")
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from .env.example")
            print("   Please edit the .env file to add your OpenAI API key")
        else:
            # Create .env file manually
            with open('.env', 'w') as f:
                f.write("# OpenAI API Key - Required for image analysis and description generation\n")
                f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            print("✅ Created .env file")
            print("   Please edit the .env file to add your OpenAI API key")
    else:
        print("\n✅ .env file already exists")
    
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
        print("\n✅ Created data directory")
    
    # Run the setup check
    print("\nRunning setup check...")
    try:
        subprocess.check_call([sys.executable, "setup_check.py"])
    except subprocess.CalledProcessError:
        print("❌ Setup check failed")
        return
    
    print("\n🎉 Setup complete!")
    print("Run 'streamlit run app.py' to start the application")

if __name__ == "__main__":
    main()