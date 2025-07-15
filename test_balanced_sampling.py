#!/usr/bin/env python3
"""
BALANCED SAMPLING TEST SCRIPT
=============================

This script tests the balanced sampling functionality to ensure we get
equal distribution across documents and 50/50 table/text questions.
"""

import json
import random
from typing import Dict, List, Any

def analyze_question_distribution(questions: List[Dict[str, Any]]):
    """ANALYZE THE DISTRIBUTION OF QUESTIONS"""
    
    # GROUP BY DOCUMENT
    doc_counts = {}
    table_count = 0
    text_count = 0
    
    for question in questions:
        doc_file = question.get("doc_file", "unknown")
        doc_counts[doc_file] = doc_counts.get(doc_file, 0) + 1
        
        table_count_in_q = question.get("table_count", 0)
        if table_count_in_q > 0:
            table_count += 1
        else:
            text_count += 1
    
    print("📊 QUESTION DISTRIBUTION ANALYSIS:")
    print(f"   📄 Total questions: {len(questions)}")
    print(f"   📋 Table questions: {table_count}")
    print(f"   📝 Text questions: {text_count}")
    print(f"   📊 Table/Text ratio: {table_count/len(questions)*100:.1f}% / {text_count/len(questions)*100:.1f}%")
    
    print("\n📚 DOCUMENT DISTRIBUTION:")
    for doc_file, count in doc_counts.items():
        percentage = (count / len(questions)) * 100
        print(f"   📄 {doc_file}: {count} questions ({percentage:.1f}%)")
    
    return {
        "total": len(questions),
        "table_count": table_count,
        "text_count": text_count,
        "doc_counts": doc_counts
    }

def test_balanced_sampling():
    """TEST THE BALANCED SAMPLING FUNCTIONALITY"""
    
    print("🧪 TESTING BALANCED SAMPLING")
    print("="*50)
    
    # LOAD QUESTIONS
    try:
        with open("data/questions/knee_test_questions_20250712_160235.json", 'r') as f:
            questions_data = json.load(f)
        
        all_questions = questions_data.get("page_tests", [])
        print(f"✅ Loaded {len(all_questions)} total questions")
        
        # ANALYZE ORIGINAL DISTRIBUTION
        print("\n📊 ORIGINAL DISTRIBUTION:")
        original_analysis = analyze_question_distribution(all_questions)
        
        # TEST DIFFERENT SAMPLE SIZES
        sample_sizes = [30, 60, 90]
        
        for sample_size in sample_sizes:
            print(f"\n🎯 TESTING SAMPLE SIZE: {sample_size}")
            print("-" * 40)
            
            # SIMULATE BALANCED SAMPLING
            balanced_sample = simulate_balanced_sampling(all_questions, sample_size)
            
            # ANALYZE BALANCED SAMPLE
            sample_analysis = analyze_question_distribution(balanced_sample)
            
            # CHECK BALANCE
            check_balance(sample_analysis, sample_size)
    
    except Exception as e:
        print(f"❌ ERROR: {e}")

def simulate_balanced_sampling(all_questions: List[Dict[str, Any]], total_questions: int) -> List[Dict[str, Any]]:
    """SIMULATE THE BALANCED SAMPLING LOGIC"""
    
    # GROUP QUESTIONS BY DOCUMENT
    doc_questions = {}
    for question in all_questions:
        doc_file = question.get("doc_file", "")
        if doc_file not in doc_questions:
            doc_questions[doc_file] = []
        doc_questions[doc_file].append(question)
    
    # SEPARATE TABLE AND TEXT QUESTIONS
    table_questions = []
    text_questions = []
    
    for question in all_questions:
        table_count = question.get("table_count", 0)
        if table_count > 0:
            table_questions.append(question)
        else:
            text_questions.append(question)
    
    # CALCULATE SAMPLING NUMBERS
    questions_per_doc = total_questions // 3  # EQUAL ACROSS 3 DOCUMENTS
    table_questions_needed = total_questions // 2  # 50% TABLE QUESTIONS
    text_questions_needed = total_questions // 2   # 50% TEXT QUESTIONS
    
    # SAMPLE QUESTIONS
    sampled_questions = []
    
    # SAMPLE TABLE QUESTIONS (50%)
    if table_questions:
        table_sample = min(table_questions_needed, len(table_questions))
        sampled_table = random.sample(table_questions, table_sample)
        sampled_questions.extend(sampled_table)
    
    # SAMPLE TEXT QUESTIONS (50%)
    if text_questions:
        text_sample = min(text_questions_needed, len(text_questions))
        sampled_text = random.sample(text_questions, text_sample)
        sampled_questions.extend(sampled_text)
    
    # BALANCE ACROSS DOCUMENTS
    doc_balanced_questions = []
    questions_per_doc_actual = total_questions // 3
    
    for doc_file in doc_questions.keys():
        doc_questions_list = [q for q in sampled_questions if q.get("doc_file") == doc_file]
        if len(doc_questions_list) > questions_per_doc_actual:
            # TAKE RANDOM SAMPLE TO BALANCE
            doc_balanced_questions.extend(random.sample(doc_questions_list, questions_per_doc_actual))
        else:
            # TAKE ALL AVAILABLE
            doc_balanced_questions.extend(doc_questions_list)
    
    # IF WE DON'T HAVE ENOUGH FROM BALANCED SAMPLING, ADD MORE
    if len(doc_balanced_questions) < total_questions:
        remaining_needed = total_questions - len(doc_balanced_questions)
        remaining_questions = [q for q in sampled_questions if q not in doc_balanced_questions]
        if remaining_questions:
            additional = random.sample(remaining_questions, min(remaining_needed, len(remaining_questions)))
            doc_balanced_questions.extend(additional)
    
    # SHUFFLE FINAL SAMPLE
    random.shuffle(doc_balanced_questions)
    
    return doc_balanced_questions[:total_questions]

def check_balance(analysis: Dict[str, Any], target_size: int):
    """CHECK IF THE SAMPLE IS PROPERLY BALANCED"""
    
    total = analysis["total"]
    table_count = analysis["table_count"]
    text_count = analysis["text_count"]
    doc_counts = analysis["doc_counts"]
    
    print(f"\n✅ BALANCE CHECK:")
    
    # CHECK TOTAL SIZE
    if total == target_size:
        print(f"   ✅ Sample size correct: {total}/{target_size}")
    else:
        print(f"   ⚠️  Sample size mismatch: {total}/{target_size}")
    
    # CHECK TABLE/TEXT BALANCE
    table_percentage = (table_count / total) * 100
    text_percentage = (text_count / total) * 100
    
    if 45 <= table_percentage <= 55:
        print(f"   ✅ Table/Text balance good: {table_percentage:.1f}% / {text_percentage:.1f}%")
    else:
        print(f"   ⚠️  Table/Text balance off: {table_percentage:.1f}% / {text_percentage:.1f}%")
    
    # CHECK DOCUMENT BALANCE
    expected_per_doc = target_size // 3
    balanced_docs = 0
    
    for doc_file, count in doc_counts.items():
        if abs(count - expected_per_doc) <= 2:  # Allow small variance
            balanced_docs += 1
            print(f"   ✅ {doc_file}: {count} (target: ~{expected_per_doc})")
        else:
            print(f"   ⚠️  {doc_file}: {count} (target: ~{expected_per_doc})")
    
    if balanced_docs >= len(doc_counts) - 1:  # Allow one doc to be off
        print(f"   ✅ Document balance: Good ({balanced_docs}/{len(doc_counts)} docs balanced)")
    else:
        print(f"   ⚠️  Document balance: Needs improvement ({balanced_docs}/{len(doc_counts)} docs balanced)")

if __name__ == "__main__":
    test_balanced_sampling() 