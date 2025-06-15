#!/usr/bin/env python3
"""
Run script for Fine Art Description Generator
This script provides a convenient way to start the application.
"""

import os
import sys
import subprocess

def main():
    """Run the Streamlit application."""
    print("Starting Fine Art Description Generator...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Warning: .env file not found. Creating from .env.example...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as example_file:
                with open('.env', 'w') as env_file:
                    env_file.write(example_file.read())
            print("Created .env file. Please edit it to add your OpenAI API key.")
        else:
            print("Error: .env.example file not found. Please create a .env file manually.")
            return
    
    # Run the Streamlit application
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\nApplication stopped.")
    except Exception as e:
        print(f"Error running application: {str(e)}")
        print("Make sure Streamlit is installed: pip install streamlit")

if __name__ == "__main__":
    main()