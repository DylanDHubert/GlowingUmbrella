#!/usr/bin/env python3
"""
SIMPLE TS KNEE QUESTIONS TEST
=============================

Run the 13 questions from questions.txt through the system
with just the TS knee JSON loaded. Show only the answers.
"""

import sys
import os
import json

# ADD FARM TO PATH
farm_path = os.path.join(os.path.dirname(__file__), 'farm/src')
sys.path.insert(0, farm_path)

from farm.farmer import Farmer

def load_questions():
    """LOAD QUESTIONS FROM questions.txt"""
    questions = []
    with open('questions.txt', 'r') as f:
        content = f.read()
    
    # PARSE QUESTIONS (LOOK FOR "Test X:" PATTERNS)
    lines = content.split('\n')
    current_question = None
    
    for line in lines:
        if line.startswith('Test ') and ':' in line:
            # EXTRACT QUESTION TEXT
            question_text = line.split(':', 1)[1].strip()
            questions.append(question_text)
    
    return questions

def main():
    """MAIN FUNCTION"""
    print("🚀 RUNNING TS KNEE QUESTIONS TEST")
    print("=" * 50)
    
    # LOAD QUESTIONS
    questions = load_questions()
    print(f"📝 Loaded {len(questions)} questions")
    print()
    
    # INITIALIZE FARMER WITH MAX 5 ITERATIONS
    print("🚜 INITIALIZING FARMER...")
    farmer = Farmer(max_agentic_iterations=5)
    
    # LOAD TS KNEE DOCUMENT
    ts_knee_path = "data/jsons/ts_knee_original_20250701_175753.json"
    print(f"📄 Loading TS knee document: {ts_knee_path}")
    success = farmer.load_document("ts_knee", ts_knee_path)
    
    if not success:
        print("❌ Failed to load TS knee document!")
        return
    
    print("✅ TS knee document loaded successfully")
    print()
    
    # RUN QUESTIONS
    print("🧪 RUNNING QUESTIONS...")
    print("=" * 50)
    
    for i, question in enumerate(questions, 1):
        print(f"\n🔍 Question {i}: {question}")
        print("-" * 40)
        
        try:
            # ASK QUESTION (NO DEBUG)
            response = farmer.ask(question, debug=False)
            
            # EXTRACT ANSWER
            if hasattr(response, 'answer'):
                answer = response.answer
            else:
                answer = str(response)
            
            print(f"💬 Answer: {answer}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
    
    print("\n🎉 ALL QUESTIONS COMPLETED!")

if __name__ == "__main__":
    main() 