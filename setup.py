import sys
import subprocess
import platform
import ensurepip

def check_python_version():
    required_version = "3.12.3"
    current_version = sys.version.split()[0]
    if current_version != required_version or platform.architecture()[0] != "64bit":
        print(f"Python {required_version} (64-bit) is required.")
        print("Please update Python manually and run this script again.")
        sys.exit(1)

def ensure_pip():
    try:
        import pip
    except ImportError:
        print("pip is not installed. Installing pip...")
        ensurepip.bootstrap()
    
    print("Upgrading pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

def install_pygame():
    print("Installing Pygame...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])

if __name__ == "__main__":
    check_python_version()
    ensure_pip()
    install_pygame()
    print("Setup complete!")