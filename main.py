#!/usr/bin/env python3
"""
Requirements Extractor - Main Entry Point
"""

import sys
import os

# Add ui directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

from main_window import main

if __name__ == "__main__":
    main()