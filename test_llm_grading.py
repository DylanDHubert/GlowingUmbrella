#!/usr/bin/env python3
"""
SIMPLE TEST SCRIPT TO VERIFY LLM GRADING AND MARKDOWN SUMMARY FUNCTIONALITY
"""

import sys
import os

# ADD FARM TO PATH - USE ABSOLUTE PATH TO AVOID CONFLICTS
farm_path = os.path.join(os.path.dirname(__file__), 'farm/src')
sys.path.insert(0, farm_path)  # INSERT AT BEGINNING TO PRIORITIZE

from test_farm_knee_system import FarmKneeTester

def main():
    """TEST THE NEW LLM GRADING AND MARKDOWN SUMMARY FEATURES"""
    
    print("🧪 TESTING LLM GRADING AND MARKDOWN SUMMARY FEATURES")
    print("="*60)
    
    # CREATE TESTER WITH DEBUG MODE AND SAVE RESULTS
    tester = FarmKneeTester(
        debug_mode=True,  # ALWAYS USE DEBUG MODE
        save_results=True
    )
    
    # RUN A SMALL TEST WITH 3 QUESTIONS
    print("📝 Running test with 3 questions...")
    tester.run_complete_test(max_tests=3, balanced_sample=True)
    
    print("\n✅ TEST COMPLETED!")
    print("📁 Check the farm_test_outputs directory for results and markdown summary")

if __name__ == "__main__":
    main() 