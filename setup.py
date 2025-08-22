#!/usr/bin/env python3
"""
ErlViz Setup Script
Sets up the ErlViz development environment with virtualenv

Copyright (c) 2025 David Leon (leondavi)
Licensed under the MIT License - see LICENSE file for details.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr and check:
        print(f"Error: {result.stderr}")
    
    if check and result.returncode != 0:
        sys.exit(1)
    
    return result

def main():
    """Main setup function"""
    project_root = Path(__file__).parent
    venv_path = project_root / 'venv'
    
    print("="*60)
    print("ErlViz Setup")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"Python version: {sys.version}")
    print(f"Project root: {project_root}")
    
    # Create virtual environment
    if venv_path.exists():
        print(f"Virtual environment already exists at: {venv_path}")
        recreate = input("Recreate virtual environment? (y/N): ").strip().lower()
        if recreate == 'y':
            print("Removing existing virtual environment...")
            import shutil
            shutil.rmtree(venv_path)
        else:
            print("Using existing virtual environment")
    
    if not venv_path.exists():
        print(f"Creating virtual environment at: {venv_path}")
        venv.create(venv_path, with_pip=True)
    
    # Determine activation script
    if os.name == 'nt':  # Windows
        activate_script = venv_path / 'Scripts' / 'activate.bat'
        pip_cmd = str(venv_path / 'Scripts' / 'pip')
    else:  # Unix/Linux/macOS
        activate_script = venv_path / 'bin' / 'activate'
        pip_cmd = str(venv_path / 'bin' / 'pip')
    
    print(f"Activation script: {activate_script}")
    
    # Upgrade pip
    print("Upgrading pip...")
    run_command(f"{pip_cmd} install --upgrade pip")
    
    # Install requirements
    requirements_file = project_root / 'requirements.txt'
    if requirements_file.exists():
        print("Installing requirements...")
        run_command(f"{pip_cmd} install -r {requirements_file}")
    else:
        print("No requirements.txt found, installing basic dependencies...")
        run_command(f"{pip_cmd} install PySide6 gitpython graphviz markdown requests networkx matplotlib pygments")
    
    # Install project in development mode
    print("Installing ErlViz in development mode...")
    run_command(f"{pip_cmd} install -e .", cwd=project_root)
    
    # Check if graphviz system package is installed
    print("Checking for Graphviz system installation...")
    graphviz_check = run_command("dot -V", check=False)
    
    if graphviz_check.returncode != 0:
        print("\nWARNING: Graphviz is not installed on your system!")
        print("Please install Graphviz:")
        print("  macOS: brew install graphviz")
        print("  Ubuntu/Debian: sudo apt-get install graphviz")
        print("  CentOS/RHEL: sudo yum install graphviz")
        print("  Windows: Download from https://graphviz.org/download/")
    else:
        print("Graphviz is installed ✓")
    
    # Create example configuration
    config_dir = project_root / 'config'
    config_dir.mkdir(exist_ok=True)
    
    example_config = config_dir / 'example_config.json'
    if not example_config.exists():
        config_content = {
            "output_format": "png",
            "generate_graphs": True,
            "generate_docs": True,
            "include_submodules": False,
            "cache_dir": "~/.erlviz/cache",
            "example_projects": [
                {
                    "name": "NErlNet",
                    "url": "https://github.com/leondavi/NErlNet",
                    "description": "Distributed machine learning framework"
                },
                {
                    "name": "Cowboy",
                    "url": "https://github.com/ninenines/cowboy", 
                    "description": "HTTP server framework"
                }
            ]
        }
        
        import json
        with open(example_config, 'w') as f:
            json.dump(config_content, f, indent=2)
        
        print(f"Created example configuration: {example_config}")
    
    # Test installation
    print("\nTesting installation...")
    test_result = run_command(f"cd {project_root} && {venv_path / 'bin' / 'python'} -c 'import erlviz; print(\"ErlViz imported successfully\")'", check=False)
    
    if test_result.returncode == 0:
        print("✓ ErlViz installation successful!")
    else:
        print("✗ ErlViz installation test failed")
        print("Please check the error messages above")
        sys.exit(1)
    
    # Final instructions
    print("\n" + "="*60)
    print("SETUP COMPLETE")
    print("="*60)
    print(f"Virtual environment created at: {venv_path}")
    print(f"To activate the environment:")
    
    if os.name == 'nt':
        print(f"  {activate_script}")
    else:
        print(f"  source {activate_script}")
    
    print(f"\nTo run ErlViz:")
    print(f"  python main.py                    # Launch GUI")
    print(f"  python main.py --cli <project>    # CLI analysis")
    print(f"  python main.py --help             # Show all options")
    
    print(f"\nExample projects to try:")
    print(f"  python main.py --cli https://github.com/leondavi/NErlNet")
    print(f"  python main.py --cli https://github.com/ninenines/cowboy")
    
    print(f"\nConfiguration examples: {config_dir}")
    print(f"Documentation will be generated in: ./erlviz_output/")

if __name__ == '__main__':
    main()
