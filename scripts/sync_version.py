#!/usr/bin/env python3
"""
Script to sync version from _version.py to pyside6_deploy.toml
Run this whenever you update the version.
"""

import re
import sys
from pathlib import Path

def get_version_from_package():
    """Read version from the package _version.py file."""
    version_file = Path("src/focus_backdrop/_version.py")
    if not version_file.exists():
        print(f"Error: Version file not found at {version_file}")
        sys.exit(1)
    
    version_content = version_file.read_text()
    version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', version_content)
    
    if not version_match:
        print("Error: Could not find __version__ in _version.py")
        sys.exit(1)
    
    return version_match.group(1)

def update_pyside6_deploy_toml(version):
    """Update version references in pyside6_deploy.toml."""
    deploy_file = Path("pyside6_deploy.toml")
    if not deploy_file.exists():
        print(f"Error: {deploy_file} not found")
        sys.exit(1)
    
    content = deploy_file.read_text()
    
    # Update version fields
    patterns = [
        (r'version = "[^"]*"', f'version = "{version}"'),
        (r'short_version = "[^"]*"', f'short_version = "{version}"'),
        (r'product_version = "[^"]*"', f'product_version = "{version}"'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    deploy_file.write_text(content)
    print(f"Updated pyside6_deploy.toml with version {version}")

def main():
    """Main function."""
    version = get_version_from_package()
    print(f"Found version: {version}")
    
    update_pyside6_deploy_toml(version)
    print("Version sync complete!")

if __name__ == "__main__":
    main()
