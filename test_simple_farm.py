#!/usr/bin/env python3
"""
SIMPLE TEST SCRIPT FOR FARM SYSTEM
==================================

This script provides a quick test to verify the farm system is working
with basic functionality before running the full test suite.
"""

import sys
import os

# ADD FARM TO PATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'farm/src'))

def test_farm_import():
    """TEST THAT FARM CAN BE IMPORTED"""
    try:
        from farm.farmer import Farmer
        print("✅ SUCCESS: Farm module imported successfully")
        return True
    except Exception as e:
        print(f"❌ ERROR: Failed to import farm module: {e}")
        return False

def test_farmer_creation():
    """TEST FARMER CREATION"""
    try:
        from farm.farmer import Farmer
        farmer = Farmer()
        print("✅ SUCCESS: Farmer created successfully")
        return True
    except Exception as e:
        print(f"❌ ERROR: Failed to create Farmer: {e}")
        return False

def test_document_loading():
    """TEST DOCUMENT LOADING"""
    try:
        from farm.farmer import Farmer
        farmer = Farmer()
        
        # TRY TO LOAD ONE KNEE DOCUMENT
        doc_path = "data/jsons/knee_original_20250701_144728.json"
        success = farmer.load_document("test_doc", doc_path)
        
        if success:
            print("✅ SUCCESS: Document loaded successfully")
            return True
        else:
            print("❌ ERROR: Document loading failed")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: Failed to load document: {e}")
        return False

def test_simple_query():
    """TEST SIMPLE QUERY"""
    try:
        from farm.farmer import Farmer
        farmer = Farmer()
        
        # LOAD DOCUMENT
        doc_path = "data/jsons/knee_original_20250701_144728.json"
        farmer.load_document("test_doc", doc_path)
        
        # ASK SIMPLE QUESTION
        response = farmer.ask("What is the Triathlon Total Knee System?")
        print(f"✅ SUCCESS: Query executed successfully")
        print(f"📝 Response: {response.answer[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to execute query: {e}")
        return False

def main():
    """RUN ALL BASIC TESTS"""
    print("🧪 RUNNING BASIC FARM TESTS")
    print("="*40)
    
    tests = [
        ("Import Test", test_farm_import),
        ("Farmer Creation Test", test_farmer_creation),
        ("Document Loading Test", test_document_loading),
        ("Simple Query Test", test_simple_query)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Farm system is ready!")
        return True
    else:
        print("❌ SOME TESTS FAILED - Check system setup")
        return False

if __name__ == "__main__":
    main() 