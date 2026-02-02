#!/usr/bin/env python3
"""
Campus AI Chat Platform - Automated Setup
One-command installation for the entire platform
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def print_step(step_num, total, text):
    """Print step information"""
    print(f"[{step_num}/{total}] {text}...")


def check_python_version():
    """Check if Python version is 3.8+"""
    print_step(1, 6, "Checking Python version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"✗ Python 3.8+ required. You have Python {version.major}.{version.minor}")
        return False
    
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    print_step(2, 6, "Setting up virtual environment")
    
    venv_path = Path(".env")
    
    if venv_path.exists():
        print(f"✓ Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", ".env"], check=True)
        print(f"✓ Virtual environment created at .env/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create virtual environment: {e}")
        return False


def get_pip_command():
    """Get the appropriate pip command for the platform"""
    if platform.system() == "Windows":
        return [".env\\Scripts\\python.exe", "-m", "pip"]
    else:
        return [".env/bin/python", "-m", "pip"]


def install_dependencies():
    """Install Python dependencies"""
    print_step(3, 6, "Installing dependencies")
    
    pip_cmd = get_pip_command()
    
    try:
        # Upgrade pip first
        print("  Upgrading pip...")
        subprocess.run(pip_cmd + ["install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        print("  Installing packages from requirements.txt...")
        subprocess.run(pip_cmd + ["install", "-r", "requirements.txt"],
                      check=True)
        
        print(f"✓ All dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False


def download_model():
    """Download AI model"""
    print_step(4, 6, "Downloading AI model")
    
    python_cmd = get_pip_command()[0]
    
    try:
        # Run the download script
        subprocess.run([python_cmd, "scripts/download_model.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Model download failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n✗ Setup cancelled by user")
        return False


def configure_environment():
    """Configure config.env file"""
    print_step(5, 6, "Configuring environment")
    
    config_file = Path("config.env")  # Using config.env to avoid conflict with .env venv
    env_example = Path(".env.example")
    
    if config_file.exists():
        print(f"✓ config.env already configured")
        return True
    
    if not env_example.exists():
        print(f"✗ .env.example not found")
        return False
    
    try:
        import shutil
        shutil.copy(env_example, config_file)
        print(f"✓ Created config.env from template")
        print(f"  You can edit config.env to customize settings")
        return True
    except Exception as e:
        print(f"✗ Failed to create config.env: {e}")
        return False


def verify_installation():
    """Verify the installation"""
    print_step(6, 6, "Verifying installation")
    
    checks = []
    
    # Check virtual environment
    venv_path = Path(".env")
    checks.append(("Virtual environment", venv_path.exists()))
    
    # Check config.env file
    config_path = Path("config.env")
    checks.append(("config.env configuration", config_path.exists()))
    
    # Check models directory
    models_dir = Path("models")
    has_model = models_dir.exists() and any(models_dir.glob("*.gguf"))
    checks.append(("AI model", has_model))
    
    # Check frontend
    frontend_dir = Path("frontend")
    has_frontend = (frontend_dir / "index.html").exists()
    checks.append(("Web frontend", has_frontend))
    
    # Print results
    all_passed = True
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"  {status} {check_name}")
        if not passed:
            all_passed = False
    
    return all_passed


def print_success_message():
    """Print success message with next steps"""
    print_header("SETUP COMPLETE!")
    
    print("✓ Campus AI Chat Platform is ready to use!\n")
    print("Next steps:\n")
    
    if platform.system() == "Windows":
        print("  1. Activate virtual environment:")
        print("     .env\\Scripts\\activate\n")
        print("  2. Start the server:")
        print("     python server.py\n")
    else:
        print("  1. Activate virtual environment:")
        print("     source .env/bin/activate\n")
        print("  2. Start the server:")
        print("     python server.py\n")
    
    print("  3. Open your browser:")
    print("     http://localhost:8080\n")
    
    print("Enjoy your local AI chat platform! 🚀\n")


def main():
    """Main setup function"""
    print_header("CAMPUS AI CHAT PLATFORM - SETUP")
    
    print("This script will:")
    print("  • Check system requirements")
    print("  • Create virtual environment")
    print("  • Install dependencies")
    print("  • Download AI model")
    print("  • Configure environment")
    print()
    
    # Run setup steps
    steps = [
        check_python_version,
        create_virtual_environment,
        install_dependencies,
        download_model,
        configure_environment,
        verify_installation
    ]
    
    for step_func in steps:
        if not step_func():
            print("\n✗ Setup failed. Please fix the errors and try again.")
            return 1
    
    # Success!
    print_success_message()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
