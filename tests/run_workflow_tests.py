#!/usr/bin/env python3
"""
Test runner for GitHub Actions workflow validation.
This can be integrated into CI/CD pipelines to validate workflow files.
"""

import sys
import subprocess
import os
from pathlib import Path


def main():
    """Run workflow validation tests."""
    test_dir = Path(__file__).parent
    os.chdir(test_dir.parent)  # Change to project root
    
    # Install test dependencies if needed
    try:
        import pytest  # noqa: F401
        import yaml    # noqa: F401
    except ImportError:
        print("Installing test dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"], 
                      check=True)
    
    # Run the tests
    exit_code = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/test_auto_pr_demo_workflow.py", 
        "-v", 
        "--tb=short"
    ]).returncode
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())