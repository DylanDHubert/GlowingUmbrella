#!/usr/bin/env python3
"""
ENHANCED OKS TEST WITH KEYWORD EXTRACTION
=========================================

Uses keyword extraction to improve search terms before running the 3-phase RAG system.
"""

import json
import sys
import os
from datetime import datetime

# ADD FARM TO PATH
farm_path = os.path.join(os.path.dirname(__file__), 'farm/src')
sys.path.insert(0, farm_path)

from farm.farmer import Farmer
from keyword_extractor import KeywordExtractor

def load_oks_questions():
    """LOAD ONLY OKS QUESTIONS FROM THE QUESTIONS FILE"""
    questions_file = "data/questions/knee_test_questions_20250712_160235.json"
    
    with open(questions_file, 'r') as f:
        all_questions = json.load(f)
    
    # FILTER FOR OKS QUESTIONS
    oks_questions = []
    for question in all_questions.get("page_tests", []):
        if "OKS" in question.get("question", "") or "Oxford Knee Score" in question.get("question", ""):
            oks_questions.append(question)
    
    print(f"📊 Found {len(oks_questions)} OKS questions")
    for i, q in enumerate(oks_questions, 1):
        print(f"  {i}. {q['question']}")
    
    return oks_questions

def run_enhanced_oks_test():
    """RUN THE OKS QUESTIONS TEST WITH KEYWORD EXTRACTION"""
    
    print("🚀 RUNNING ENHANCED OKS QUESTIONS TEST")
    print("="*60)
    
    # INITIALIZE KEYWORD EXTRACTOR
    extractor = KeywordExtractor()
    
    # LOAD OKS QUESTIONS
    oks_questions = load_oks_questions()
    if not oks_questions:
        print("❌ No OKS questions found!")
        return
    
    # INITIALIZE FARMER WITH 10 ITERATIONS
    print("\n🚜 INITIALIZING FARMER...")
    farmer = Farmer(max_agentic_iterations=10)
    
    # LOAD KNEE DOCUMENTS
    knee_docs = {
        "knee_original_20250701_144728": "data/jsons/knee_original_20250701_144728.json",
        "knee_original_20250701_171754": "data/jsons/knee_original_20250701_171754.json", 
        "knee_original_20250702_233749": "data/jsons/knee_original_20250702_233749.json"
    }
    
    for doc_name, doc_path in knee_docs.items():
        print(f"  📄 Loading {doc_name}...")
        success = farmer.load_document(doc_name, doc_path)
        if success:
            print(f"    ✅ Successfully loaded {doc_name}")
        else:
            print(f"    ❌ Failed to load {doc_name}")
    
    # CHECK SYSTEM STATUS
    status = farmer.get_system_status()
    print(f"📊 System Status: {status}")
    
    # RUN OKS QUESTIONS WITH KEYWORD ENHANCEMENT
    print(f"\n🧪 RUNNING {len(oks_questions)} OKS QUESTIONS WITH KEYWORD EXTRACTION...")
    print("="*60)
    
    results = []
    for i, question_data in enumerate(oks_questions, 1):
        question = question_data["question"]
        expected = question_data["target_content"]
        
        print(f"\n{i}. Question: {question}")
        print(f"   Expected: {expected}")
        
        # EXTRACT KEYWORDS
        keywords = extractor.extract_keywords(question)
        search_terms = extractor.generate_search_terms(keywords)
        
        print(f"   🔍 Extracted keywords: {search_terms[:5]}...")  # SHOW FIRST 5
        
        try:
            # ASK QUESTION WITH DEBUG MODE
            response = farmer.ask(question, debug=True)
            
            if response and 'answer' in response:
                actual_answer = response['answer']
                print(f"   Actual: {actual_answer}")
                
                # SIMPLE SUCCESS CHECK
                success = expected.lower() in actual_answer.lower()
                print(f"   Success: {'✅' if success else '❌'}")
                
                results.append({
                    "question": question,
                    "expected": expected,
                    "actual": actual_answer,
                    "success": success,
                    "keywords": search_terms,
                    "debug_info": response.get('debug_info', {})
                })
            else:
                print(f"   ❌ No answer received")
                results.append({
                    "question": question,
                    "expected": expected,
                    "actual": "No answer",
                    "success": False,
                    "keywords": search_terms,
                    "debug_info": {}
                })
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "question": question,
                "expected": expected,
                "actual": f"Error: {e}",
                "success": False,
                "keywords": search_terms,
                "debug_info": {}
            })
    
    # PRINT SUMMARY
    print(f"\n📊 ENHANCED OKS TEST SUMMARY")
    print("="*60)
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    success_rate = (successful / total) * 100 if total > 0 else 0
    
    print(f"Total Questions: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    # SHOW KEYWORD ANALYSIS
    print(f"\n🔍 KEYWORD ANALYSIS:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Keywords: {result['keywords']}")
    
    # SAVE RESULTS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"farm_test_outputs/oks_enhanced_run_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    results_file = f"{output_dir}/oks_enhanced_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "test_name": "Enhanced OKS Questions Test",
            "timestamp": datetime.now().isoformat(),
            "total_questions": total,
            "successful_answers": successful,
            "failed_answers": total - successful,
            "success_rate": success_rate,
            "enhancement": "keyword_extraction",
            "results": results
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")

if __name__ == "__main__":
    run_enhanced_oks_test() 