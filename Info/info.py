import os
import platform
import sys
import pip
from subprocess import check_output

def get_system_info():
    print("=== System Information ===")
    print(f"Operating System: {platform.system()}")
    print(f"OS Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"CPU Count: {os.cpu_count()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print()

def get_python_info():
    print("=== Python Information ===")
    print(f"Python Version: {platform.python_version()}")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Installation Path: {os.path.dirname(sys.executable)}")
    print(f"User Base Path: {sys.base_prefix}")
    print(f"User Site Path: {os.path.join(sys.base_prefix, 'Lib', 'site-packages')}")
    print()

def get_python_paths():
    print("=== Python Paths ===")
    for path in sys.path:
        print(path)
    print()

def get_installed_libraries():
    print("=== Installed Python Libraries ===")
    try:
        # Get the list of installed packages
        installed_packages = check_output([sys.executable, '-m', 'pip', 'list']).decode()
        print(installed_packages)
    except Exception as e:
        print(f"Failed to get installed libraries: {e}")
    print()

if __name__ == "__main__":
    get_system_info()
    get_python_info()
    get_python_paths()
    get_installed_libraries()
