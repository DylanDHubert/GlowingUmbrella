#!/usr/bin/env python3
"""
DEBUG SCRIPT TO CHECK WHICH FARMER WE'RE IMPORTING
"""

import sys
import os

# ADD FARM TO PATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'farm/src'))

try:
    from farm.farmer import Farmer
    print("✅ Successfully imported Farmer from farm.farmer")
    
    # CHECK THE FARMER'S ASK METHOD
    farmer = Farmer()
    print(f"Farmer ask method signature: {farmer.ask.__code__.co_varnames}")
    print(f"Farmer ask method defaults: {farmer.ask.__defaults__}")
    
except Exception as e:
    print(f"❌ Error importing Farmer: {e}")

# ALSO TRY DIFFERENT PATHS
print("\n🔍 Checking other possible import paths...")

# TRY FARM ROOT
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'farm'))
try:
    from farm.farmer import Farmer as Farmer2
    print("✅ Found Farmer in farm/ (root)")
except Exception as e:
    print(f"❌ No Farmer in farm/ (root): {e}")

# TRY BRUCE LEE
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'BruceLee'))
try:
    from farm.farmer import Farmer as Farmer3
    print("✅ Found Farmer in BruceLee/")
except Exception as e:
    print(f"❌ No Farmer in BruceLee/: {e}") 