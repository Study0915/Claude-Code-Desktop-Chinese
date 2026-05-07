#!/usr/bin/env python3
"""Test script to verify tray module imports correctly."""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from tray import __init__
    from tray import config_manager

    print("✓ Successfully imported tray module")
    print(f"  - __init__.py loaded: {__init__}")
    print(f"  - config_manager loaded: {config_manager}")

    # Test config manager functions
    config = config_manager.load_config()
    print(f"\n✓ Successfully loaded default config:")
    print(f"  - installed: {config['installed']}")
    print(f"  - language: {config['language']}")
    print(f"  - auto_start: {config['auto_start']}")

    print("\n✅ All tests passed!")

except ImportError as e:
    print(f"✗ Failed to import: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    sys.exit(1)