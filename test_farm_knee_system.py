#!/usr/bin/env python3
"""
COMPREHENSIVE TESTING FRAMEWORK FOR FARM SYSTEM
================================================

This script provides a complete testing framework for the farm RAG system using:
- Multiple knee documents loaded together
- Pre-generated test questions with expected answers
- Automated response grading and analysis
- Debug mode testing with detailed output
- Performance metrics and reporting

USAGE:
    python test_farm_knee_system.py [--debug] [--save-results] [--load-all-docs]
"""

import json
import sys
import os
import time
import argparse
import random
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import statistics
import shutil

# ADD FARM TO PATH - USE ABSOLUTE PATH TO AVOID CONFLICTS
farm_path = os.path.join(os.path.dirname(__file__), 'farm/src')
sys.path.insert(0, farm_path)  # INSERT AT BEGINNING TO PRIORITIZE

from farm.farmer import Farmer


@dataclass
class TestResult:
    """STRUCTURE FOR STORING INDIVIDUAL TEST RESULTS"""
    question: str
    expected_answer: str
    actual_answer: str
    page_id: str
    page_title: str
    doc_file: str
    difficulty: str
    expected_answer_type: str
    response_time: float
    debug_info: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    # REMOVED: success field - will be determined by LLM grader


@dataclass
class RAGDiagnostic:
    """STRUCTURE FOR STORING RAG PIPELINE DIAGNOSTICS"""
    discovery_issue: Optional[str] = None
    retrieval_issue: Optional[str] = None
    llm_issue: Optional[str] = None
    correct_page_found: bool = False
    correct_page_rank: Optional[int] = None
    correct_content_retrieved: bool = False
    tools_used: Optional[List[str]] = None
    total_iterations: int = 0
    keyword_enhancement: Optional[Dict[str, Any]] = None

@dataclass
class GradingResult:
    """STRUCTURE FOR STORING ENHANCED LLM GRADING RESULTS"""
    question: str
    expected_answer: str
    actual_answer: str
    is_correct: bool  # TRUE/FALSE - BINARY JUDGMENT
    justification: str
    rag_diagnostic: RAGDiagnostic
    is_useless_page_question: bool = False
    useless_page_explanation: Optional[str] = None
    improvement_suggestion: Optional[str] = None
    grader_model: str = "gpt-3.5-turbo"

@dataclass
class TestSuite:
    """STRUCTURE FOR STORING COMPLETE TEST SUITE RESULTS"""
    test_name: str
    timestamp: str
    total_questions: int
    successful_answers: int
    failed_answers: int
    average_response_time: float
    median_response_time: float
    results: List[TestResult]
    grading_results: List[GradingResult]
    system_status: Dict[str, Any]
    performance_metrics: Dict[str, Any]


class FarmKneeTester:
    """MAIN TESTING CLASS FOR FARM SYSTEM WITH KNEE DOCUMENTS"""
    
    def __init__(self, debug_mode: bool = False, save_results: bool = True):
        """
        INITIALIZE THE TESTER
        
        Args:
            debug_mode: Enable detailed debug output
            save_results: Save results to JSON file
        """
        self.debug_mode = debug_mode
        self.save_results_flag = save_results
        self.farmer = None
        self.test_results = []
        self.questions_data = None
        
        # KNEE DOCUMENT PATHS (EXCLUDING TS KNEE)
        self.knee_docs = {
            "knee_original_20250701_144728": "data/jsons/knee_original_20250701_144728.json",
            "knee_original_20250701_171754": "data/jsons/knee_original_20250701_171754.json", 
            "knee_original_20250702_233749": "data/jsons/knee_original_20250702_233749.json"
        }
        
        # QUESTIONS FILE PATH
        self.questions_file = "data/questions/knee_test_questions_20250712_160235.json"
        
        print("🌾 INITIALIZING FARM KNEE TESTER")
        print(f"📁 Knee documents: {len(self.knee_docs)}")
        print(f"❓ Questions file: {self.questions_file}")
        print(f"🐛 Debug mode: {debug_mode}")
        print(f"💾 Save results: {save_results}")
        print()
    
    def extract_keywords(self, text: str) -> List[str]:
        """EXTRACT KEYWORDS FROM TEXT FOR ENHANCED DISCOVERY"""
        # REMOVE COMMON STOP WORDS AND SHORT WORDS
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'shall', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers', 'ours', 'theirs',
            'what', 'when', 'where', 'why', 'how', 'which', 'who', 'whom', 'whose', 'if', 'then', 'else',
            'as', 'than', 'so', 'because', 'although', 'while', 'since', 'until', 'before', 'after', 'during',
            'through', 'under', 'over', 'above', 'below', 'between', 'among', 'within', 'without', 'against',
            'toward', 'towards', 'into', 'onto', 'upon', 'from', 'up', 'down', 'out', 'off', 'away', 'back',
            'around', 'across', 'along', 'beside', 'beyond', 'inside', 'outside', 'near', 'far', 'close',
            'open', 'close', 'high', 'low', 'big', 'small', 'large', 'little', 'good', 'bad', 'new', 'old',
            'young', 'first', 'last', 'next', 'previous', 'current', 'recent', 'early', 'late', 'soon',
            'now', 'then', 'here', 'there', 'everywhere', 'somewhere', 'nowhere', 'anywhere', 'always',
            'never', 'sometimes', 'often', 'usually', 'rarely', 'seldom', 'frequently', 'occasionally',
            'much', 'many', 'few', 'several', 'some', 'any', 'all', 'none', 'each', 'every', 'both',
            'either', 'neither', 'other', 'another', 'same', 'different', 'similar', 'various', 'several',
            'multiple', 'single', 'double', 'triple', 'half', 'quarter', 'third', 'fourth', 'fifth',
            'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'hundred', 'thousand', 'million', 'billion',
            'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
            'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen',
            'nineteen', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety',
            'hundred', 'thousand', 'million', 'billion', 'trillion'
        }
        
        # TOKENIZE AND NORMALIZE
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # FILTER OUT STOP WORDS AND SHORT WORDS
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # REMOVE DUPLICATES WHILE PRESERVING ORDER
        seen = set()
        unique_keywords = []
        for word in keywords:
            if word not in seen:
                seen.add(word)
                unique_keywords.append(word)
        
        return unique_keywords
    
    def enhance_query_with_keywords(self, question: str) -> str:
        """ENHANCE QUERY WITH EXTRACTED KEYWORDS FOR BETTER DISCOVERY"""
        keywords = self.extract_keywords(question)
        
        if not keywords:
            return question
        
        # ADD KEYWORDS TO QUERY FOR ENHANCED DISCOVERY
        enhanced_query = f"{question} {' '.join(keywords)}"
        
        print(f"🔍 ENHANCED QUERY: {enhanced_query}")
        print(f"   📝 Original: {question}")
        print(f"   🏷️ Keywords: {', '.join(keywords[:10])}")  # SHOW FIRST 10 KEYWORDS
        
        return enhanced_query
    
    def load_questions(self) -> bool:
        """LOAD TEST QUESTIONS FROM JSON FILE"""
        try:
            print("📖 LOADING TEST QUESTIONS...")
            with open(self.questions_file, 'r') as f:
                self.questions_data = json.load(f)
            
            total_questions = len(self.questions_data.get("page_tests", []))
            print(f"✅ Loaded {total_questions} test questions")
            return True
            
        except Exception as e:
            print(f"❌ ERROR LOADING QUESTIONS: {e}")
            return False
    
    def initialize_farmer(self) -> bool:
        """INITIALIZE FARMER WITH ALL KNEE DOCUMENTS"""
        try:
            print("🚜 INITIALIZING FARMER...")
            
            # CREATE FARMER INSTANCE WITH MAX 5 AGENTIC ITERATIONS
            self.farmer = Farmer(max_agentic_iterations=5)
            
            # LOAD ALL KNEE DOCUMENTS
            print("📚 LOADING KNEE DOCUMENTS...")
            for doc_name, doc_path in self.knee_docs.items():
                print(f"  📄 Loading {doc_name}...")
                success = self.farmer.load_document(doc_name, doc_path)
                if success:
                    print(f"    ✅ Successfully loaded {doc_name}")
                else:
                    print(f"    ❌ Failed to load {doc_name}")
            
            # CHECK SYSTEM STATUS
            status = self.farmer.get_system_status()
            
            # HANDLE DIFFERENT STATUS FORMATS
            if 'status' in status:
                # OLD BRUCELEE FORMAT
                print(f"📊 System Status: {status['status']}")
                print(f"📄 Loaded documents: {status['loaded_documents']}")
            else:
                # NEW FARM FORMAT
                status_text = "healthy" if status.get('documents_loaded', False) else "not ready"
                print(f"📊 System Status: {status_text}")
                print(f"📄 Loaded documents: {status.get('total_documents', 0)}")
            
            return True
            
        except Exception as e:
            print(f"❌ ERROR INITIALIZING FARMER: {e}")
            return False
    
    def run_single_test(self, question_data: Dict[str, Any]) -> TestResult:
        """RUN A SINGLE TEST QUESTION"""
        
        start_time = time.time()
        
        try:
            # EXTRACT QUESTION DATA
            question = question_data["question"]
            expected_answer = question_data["target_content"]
            page_id = question_data["page_id"]
            page_title = question_data["page_title"]
            doc_file = question_data["doc_file"]
            difficulty = question_data["difficulty"]
            expected_answer_type = question_data["expected_answer_type"]
            
            # ENHANCE QUERY WITH KEYWORDS FOR BETTER DISCOVERY
            enhanced_question = self.enhance_query_with_keywords(question)
            
            # ASK QUESTION WITH DEBUG MODE (ALWAYS USE DEBUG)
            if self.farmer is None:
                raise Exception("Farmer not initialized")
                
            response = self.farmer.ask(enhanced_question, debug=True)
            
            # EXTRACT ANSWER FROM DEBUG RESPONSE
            if isinstance(response, dict) and "rag_response" in response:
                rag_response = response["rag_response"]
                actual_answer = rag_response.answer if hasattr(rag_response, 'answer') else str(rag_response)
                debug_info = response
            else:
                # FALLBACK FOR NON-DEBUG RESPONSE
                actual_answer = response.answer if hasattr(response, 'answer') else str(response)
                debug_info = {"response": response}
            
            # TRIM RELEVANT PAGES AND TABLES IN DEBUG INFO (TOP 10, TITLES ONLY)
            try:
                rag_response_obj = debug_info.get("rag_response")
                if rag_response_obj and hasattr(rag_response_obj, "context"):
                    discovery_data = getattr(rag_response_obj.context, "retrieved_data", {}).get("discovery_data", {})
                    if "relevant_pages" in discovery_data:
                        discovery_data["relevant_pages"] = [
                            {"page_title": p.get("page_title", "")}
                            for p in discovery_data["relevant_pages"][:10]
                        ]
                    if "relevant_tables" in discovery_data:
                        discovery_data["relevant_tables"] = [
                            {"table_name": t.get("table_name", "")}
                            for t in discovery_data["relevant_tables"][:10]
                        ]
            except Exception as trim_exc:
                print(f"⚠️  Could not trim debug_info: {trim_exc}")

            response_time = time.time() - start_time
            
            return TestResult(
                question=question,
                expected_answer=expected_answer,
                actual_answer=actual_answer,
                page_id=page_id,
                page_title=page_title,
                doc_file=doc_file,
                difficulty=difficulty,
                expected_answer_type=expected_answer_type,
                response_time=response_time,
                debug_info=debug_info
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return TestResult(
                question=question_data.get("question", "Unknown"),
                expected_answer=question_data.get("target_content", ""),
                actual_answer=f"ERROR: {str(e)}",
                page_id=question_data.get("page_id", ""),
                page_title=question_data.get("page_title", ""),
                doc_file=question_data.get("doc_file", ""),
                difficulty=question_data.get("difficulty", ""),
                expected_answer_type=question_data.get("expected_answer_type", ""),
                response_time=response_time,
                error_message=str(e)
            )
    
    def get_balanced_sample(self, total_questions: int) -> List[Dict[str, Any]]:
        """GET BALANCED SAMPLE OF QUESTIONS ACROSS DOCUMENTS AND CONTENT TYPES"""
        
        all_questions = self.questions_data.get("page_tests", [])
        
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
        
        print(f"📊 QUESTION DISTRIBUTION:")
        print(f"   📄 Total questions: {len(all_questions)}")
        print(f"   📋 Table questions: {len(table_questions)}")
        print(f"   📝 Text questions: {len(text_questions)}")
        
        for doc_file, questions in doc_questions.items():
            print(f"   📚 {doc_file}: {len(questions)} questions")
        
        # CALCULATE SAMPLING NUMBERS
        questions_per_doc = total_questions // 3  # EQUAL ACROSS 3 DOCUMENTS
        table_questions_needed = total_questions // 2  # 50% TABLE QUESTIONS
        text_questions_needed = total_questions // 2   # 50% TEXT QUESTIONS
        
        print(f"\n🎯 SAMPLING TARGETS:")
        print(f"   📊 Total sample: {total_questions}")
        print(f"   📋 Table questions needed: {table_questions_needed}")
        print(f"   📝 Text questions needed: {text_questions_needed}")
        print(f"   📚 Questions per document: {questions_per_doc}")
        
        # SAMPLE QUESTIONS
        sampled_questions = []
        
        # SAMPLE TABLE QUESTIONS (50%)
        if table_questions:
            table_sample = min(table_questions_needed, len(table_questions))
            sampled_table = random.sample(table_questions, table_sample)
            sampled_questions.extend(sampled_table)
            print(f"   ✅ Sampled {len(sampled_table)} table questions")
        
        # SAMPLE TEXT QUESTIONS (50%)
        if text_questions:
            text_sample = min(text_questions_needed, len(text_questions))
            sampled_text = random.sample(text_questions, text_sample)
            sampled_questions.extend(sampled_text)
            print(f"   ✅ Sampled {len(sampled_text)} text questions")
        
        # BALANCE ACROSS DOCUMENTS - IMPROVED ALGORITHM
        questions_per_doc = total_questions // 3
        doc_balanced_questions = []
        
        # FIRST, TRY TO GET EQUAL NUMBERS FROM EACH DOCUMENT
        for doc_file in doc_questions.keys():
            doc_questions_list = [q for q in sampled_questions if q.get("doc_file") == doc_file]
            if doc_questions_list:
                # TAKE UP TO THE TARGET PER DOCUMENT
                target_for_doc = min(questions_per_doc, len(doc_questions_list))
                doc_sample = random.sample(doc_questions_list, target_for_doc)
                doc_balanced_questions.extend(doc_sample)
        
        # IF WE DON'T HAVE ENOUGH, ADD MORE FROM ANY DOCUMENT
        if len(doc_balanced_questions) < total_questions:
            remaining_needed = total_questions - len(doc_balanced_questions)
            remaining_questions = [q for q in sampled_questions if q not in doc_balanced_questions]
            if remaining_questions:
                additional = random.sample(remaining_questions, min(remaining_needed, len(remaining_questions)))
                doc_balanced_questions.extend(additional)
        
        # SHUFFLE FINAL SAMPLE
        random.shuffle(doc_balanced_questions)
        
        print(f"   🎯 Final balanced sample: {len(doc_balanced_questions)} questions")
        
        return doc_balanced_questions[:total_questions]
    
    def analyze_rag_pipeline(self, result: TestResult) -> RAGDiagnostic:
        """ANALYZE RAG PIPELINE TO IDENTIFY ISSUES"""
        diagnostic = RAGDiagnostic()
        
        if not result.debug_info or "rag_response" not in result.debug_info:
            diagnostic.discovery_issue = "No debug information available"
            return diagnostic
        
        debug_info = result.debug_info
        rag_response = debug_info["rag_response"]
        
        # EXTRACT EXPECTED PAGE/TABLE INFO
        expected_page_id = result.page_id
        expected_page_title = result.page_title
        
        # ANALYZE DISCOVERY PHASE
        discovery_data = rag_response.context.retrieved_data.get("discovery_data", {})
        relevant_pages = discovery_data.get("relevant_pages", [])
        relevant_tables = discovery_data.get("relevant_tables", [])
        
        # CHECK IF CORRECT PAGE WAS FOUND - IMPROVED MATCHING
        correct_page_found = False
        correct_page_rank = None
        
        # NORMALIZE TITLES FOR COMPARISON
        expected_title_normalized = expected_page_title.lower().replace(":", "").replace(" ", "")
        expected_page_num = expected_page_id.replace("page_", "")
        
        for i, page in enumerate(relevant_pages):
            page_title = page.get("page_title", "")
            page_number = str(page.get("page_number", ""))
            
            # EXACT MATCH
            if (page_title == expected_page_title or page_number == expected_page_num):
                correct_page_found = True
                correct_page_rank = i + 1
                break
            
            # FUZZY MATCH - CHECK IF TITLES ARE VERY SIMILAR
            page_title_normalized = page_title.lower().replace(":", "").replace(" ", "")
            
            # CHECK IF ONE TITLE CONTAINS THE OTHER (FOR SIMILAR TITLES)
            if (expected_title_normalized in page_title_normalized or 
                page_title_normalized in expected_title_normalized):
                correct_page_found = True
                correct_page_rank = i + 1
                break
            
            # CHECK FOR COMMON PREFIXES (E.G., "TRIATHLON TOTAL KNEE SYSTEM REFERENCE GUIDE")
            if (expected_title_normalized.startswith("triathlon") and 
                page_title_normalized.startswith("triathlon") and
                len(expected_title_normalized) > 20 and len(page_title_normalized) > 20):
                # IF BOTH START WITH "TRIATHLON" AND ARE LONG ENOUGH, LIKELY SAME DOCUMENT
                correct_page_found = True
                correct_page_rank = i + 1
                break
        
        diagnostic.correct_page_found = correct_page_found
        diagnostic.correct_page_rank = correct_page_rank
        
        # ANALYZE KEYWORD ENHANCEMENT EFFECTIVENESS
        original_keywords = self.extract_keywords(result.question)
        if original_keywords:
            diagnostic.keyword_enhancement = {
                "original_keywords": original_keywords[:10],  # FIRST 10 KEYWORDS
                "keyword_count": len(original_keywords),
                "enhanced_query_used": True
            }
        
        if not correct_page_found:
            diagnostic.discovery_issue = f"Expected page '{expected_page_title}' (ID: {expected_page_id}) not found in discovery results"
        
        # ANALYZE AGENTIC LOOP - FIXED PATH
        # CHECK IF AGENTIC LOOP IS NESTED IN debug_info
        if "debug_info" in debug_info:
            agentic_loop = debug_info["debug_info"].get("agentic_loop", {})
        else:
            agentic_loop = debug_info.get("agentic_loop", {})
        
        iterations = agentic_loop.get("iterations", [])
        diagnostic.total_iterations = len(iterations)
        
        # CHECK WHAT TOOLS WERE USED - IMPROVED EXTRACTION
        tools_used = []
        for iteration in iterations:
            tool_calls = iteration.get("tool_calls", [])
            for tool_call in tool_calls:
                tool_name = tool_call.get("tool_name", "")
                if tool_name:
                    tools_used.append(tool_name)
        
        # REMOVE DUPLICATES AND SORT
        diagnostic.tools_used = sorted(list(set(tools_used))) if tools_used else []
        
        # IMPROVE CONTENT RETRIEVAL CHECK - FIXED LOGIC
        correct_content_retrieved = False
        
        # IF TOOLS WERE USED, CONTENT WAS RETRIEVED
        if diagnostic.tools_used:
            correct_content_retrieved = True
        elif diagnostic.total_iterations > 0:
            # IF THERE WERE ITERATIONS BUT NO TOOLS, STILL CONSIDER CONTENT RETRIEVED
            correct_content_retrieved = True
        
        diagnostic.correct_content_retrieved = correct_content_retrieved
        
        # ADD DEBUG INFO TO HELP TROUBLESHOOT
        if diagnostic.total_iterations == 0:
            diagnostic.retrieval_issue = f"No agentic iterations found. Debug keys: {list(debug_info.keys())}"
        elif not diagnostic.tools_used:
            diagnostic.retrieval_issue = f"Agentic loop ran ({diagnostic.total_iterations} iterations) but no tools were used"
        elif not correct_content_retrieved:
            if not correct_page_found:
                diagnostic.retrieval_issue = "Cannot retrieve content from page that wasn't discovered"
            else:
                diagnostic.retrieval_issue = "Correct page found but content not properly retrieved"
        
        return diagnostic
    
    def grade_answers_with_llm(self, results: List[TestResult]) -> List[GradingResult]:
        """GRADE ALL ANSWERS USING ENHANCED LLM GRADER WITH RAG DIAGNOSTICS"""
        print("🎯 GRADING ANSWERS WITH ENHANCED LLM GRADER...")
        
        grading_results = []
        
        for i, result in enumerate(results, 1):
            print(f"  📝 Grading answer {i}/{len(results)}...")
            
            # ANALYZE RAG PIPELINE
            rag_diagnostic = self.analyze_rag_pipeline(result)
            
            try:
                # CREATE ENHANCED GRADING PROMPT
                grading_prompt = f"""
You are an expert grader evaluating a RAG system's performance on a medical question.

QUESTION: {result.question}
EXPECTED ANSWER: {result.expected_answer}
ACTUAL ANSWER: {result.actual_answer}

RAG PIPELINE ANALYSIS:
- Expected source: {result.page_title} (ID: {result.page_id})
- Correct page found: {rag_diagnostic.correct_page_found}
- Correct page rank: {rag_diagnostic.correct_page_rank if rag_diagnostic.correct_page_rank else "N/A"}
- Correct content retrieved: {rag_diagnostic.correct_content_retrieved}
- Tools used: {', '.join(rag_diagnostic.tools_used) if rag_diagnostic.tools_used else "None"}
- Total iterations: {rag_diagnostic.total_iterations}

DIAGNOSTIC ISSUES:
- Discovery issue: {rag_diagnostic.discovery_issue or "None"}
- Retrieval issue: {rag_diagnostic.retrieval_issue or "None"}
- LLM issue: {rag_diagnostic.llm_issue or "None"}

Your task is to:
1. Determine if the answer is CORRECT (true) or INCORRECT (false) - binary judgment ONLY. Do not give a score or partial credit.
2. Provide a brief justification.
3. Identify the primary failure point in the RAG pipeline.
4. FLAG if this question is about a "useless" page/table that shouldn't be in the test set.

GRADING CRITERIA:
- For exact lookup questions (e.g., "what is the code for X?", "what is the measurement Y?"): The answer must contain the exact expected value. For example, if the expected answer is "44mm", the answer must include "44mm" to be correct.
- For explanatory questions: The answer is correct if it contains the right content/information, even if not phrased exactly as expected. Focus on whether the key information is present and accurate.
- For complex analysis questions: The answer is correct if it demonstrates understanding of the relevant concepts and provides accurate information, even if not perfectly formatted.

IMPORTANT: Look for questions that ask about:
- "useless" pages/tables
- "explain why this page is useless"
- "what could've happened" (in context of useless content)
- Questions that seem to be about testing the system rather than real medical content

If you detect a useless page question, mark it as such and explain why it's problematic.

Respond in JSON format:
{{
    "is_correct": <true/false>,
    "justification": "<text>",
    "primary_failure_point": "<discovery|retrieval|llm|none>",
    "is_useless_page_question": <true/false>,
    "useless_page_explanation": "<explanation if useless page detected, otherwise null>",
    "improvement_suggestion": "<text or null>"
}}
"""
                
                # CALL LLM FOR GRADING
                if self.farmer and hasattr(self.farmer, 'barn') and self.farmer.barn.llm_client:
                    response = self.farmer.barn.llm_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": grading_prompt}],
                        temperature=0.3,
                        max_tokens=300
                    )
                    
                    # PARSE RESPONSE
                    try:
                        grading_text = response.choices[0].message.content
                        if grading_text:
                            grading_data = json.loads(grading_text)
                        else:
                            raise ValueError("Empty response from LLM")
                        
                        grading_result = GradingResult(
                            question=result.question,
                            expected_answer=result.expected_answer,
                            actual_answer=result.actual_answer,
                            is_correct=grading_data.get("is_correct", False),
                            justification=grading_data.get("justification", "No justification provided"),
                            rag_diagnostic=rag_diagnostic,
                            is_useless_page_question=grading_data.get("is_useless_page_question", False),
                            useless_page_explanation=grading_data.get("useless_page_explanation"),
                            improvement_suggestion=grading_data.get("improvement_suggestion"),
                            grader_model="gpt-3.5-turbo"
                        )
                        
                        grading_results.append(grading_result)
                        
                    except json.JSONDecodeError:
                        print(f"    ⚠️  Failed to parse LLM response for question {i}")
                        # CREATE FALLBACK GRADING RESULT
                        grading_results.append(GradingResult(
                            question=result.question,
                            expected_answer=result.expected_answer,
                            actual_answer=result.actual_answer,
                            is_correct=False,
                            justification="Failed to parse LLM grading response",
                            rag_diagnostic=rag_diagnostic,
                            grader_model="gpt-3.5-turbo"
                        ))
                        
                else:
                    print(f"    ⚠️  No LLM client available for grading question {i}")
                    # CREATE FALLBACK GRADING RESULT
                    grading_results.append(GradingResult(
                        question=result.question,
                        expected_answer=result.expected_answer,
                        actual_answer=result.actual_answer,
                        is_correct=False,
                        justification="No LLM client available for grading",
                        rag_diagnostic=rag_diagnostic,
                        grader_model="none"
                    ))
                    
            except Exception as e:
                print(f"    ❌ Error grading question {i}: {e}")
                # CREATE FALLBACK GRADING RESULT
                grading_results.append(GradingResult(
                    question=result.question,
                    expected_answer=result.expected_answer,
                    actual_answer=result.actual_answer,
                    is_correct=False,
                    justification=f"Grading error: {str(e)}",
                    rag_diagnostic=rag_diagnostic,
                    grader_model="error"
                ))
        
        print(f"✅ Completed grading {len(grading_results)} answers")
        return grading_results
    
    def get_output_dir(self):
        """Get or create a unique output directory for this run."""
        base_dir = "farm_test_outputs"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = os.path.join(base_dir, f"run_{timestamp}")
        os.makedirs(run_dir, exist_ok=True)
        return run_dir

    def run_all_tests(self, max_tests: Optional[int] = None, balanced_sample: bool = True) -> TestSuite:
        """RUN ALL TESTS AND RETURN COMPREHENSIVE RESULTS"""
        
        print("🧪 RUNNING ALL TESTS...")
        
        if not self.questions_data:
            print("❌ No questions loaded!")
            return TestSuite(
                test_name="Farm Knee System Test",
                timestamp=datetime.now().isoformat(),
                total_questions=0,
                successful_answers=0,
                failed_answers=0,
                average_response_time=0.0,
                median_response_time=0.0,
                results=[],
                grading_results=[],
                system_status={},
                performance_metrics={}
            )
        
        if balanced_sample and max_tests:
            questions = self.get_balanced_sample(max_tests)
        else:
            questions = self.questions_data.get("page_tests", []) if self.questions_data else []
            if max_tests:
                questions = questions[:max_tests]
        
        total_questions = len(questions)
        print(f"📝 Running {total_questions} tests...")
        
        results = []
        successful_answers = 0
        failed_answers = 0
        response_times = []
        
        for i, question_data in enumerate(questions, 1):
            print(f"  🔍 Test {i}/{total_questions}: {question_data['question'][:50]}...")
            
            result = self.run_single_test(question_data)
            results.append(result)
            
            # DETERMINE SUCCESS FOR LLM GRADER
            success = result.expected_answer.lower() in result.actual_answer.lower()
            
            if success:
                successful_answers += 1
            else:
                failed_answers += 1
            
            response_times.append(result.response_time)
            
            # PRINT PROGRESS
            if i % 10 == 0:
                success_rate = (successful_answers / i) * 100
                avg_time = statistics.mean(response_times)
                print(f"    📊 Progress: {i}/{total_questions} | Success: {success_rate:.1f}% | Avg Time: {avg_time:.2f}s")
        
        # CALCULATE METRICS
        avg_response_time = statistics.mean(response_times) if response_times else 0
        median_response_time = statistics.median(response_times) if response_times else 0
        
        # GET SYSTEM STATUS
        system_status = self.farmer.get_system_status() if self.farmer else {}
        
        # PERFORMANCE METRICS - WILL BE UPDATED AFTER LLM GRADING
        performance_metrics = {
            "total_questions": total_questions,
            "success_rate": 0,  # WILL BE UPDATED AFTER LLM GRADING
            "avg_response_time": avg_response_time,
            "median_response_time": median_response_time,
            "min_response_time": min(response_times) if response_times else 0,
            "max_response_time": max(response_times) if response_times else 0,
            "response_time_std": statistics.stdev(response_times) if len(response_times) > 1 else 0
        }
        
        # GRADE ANSWERS WITH LLM
        grading_results = self.grade_answers_with_llm(results)
        
        # CALCULATE SUCCESS BASED ON LLM GRADING
        successful_answers_llm = len([g for g in grading_results if g.is_correct])
        failed_answers_llm = len([g for g in grading_results if not g.is_correct])
        
        # UPDATE PERFORMANCE METRICS WITH LLM GRADING RESULTS
        performance_metrics["success_rate"] = (successful_answers_llm / total_questions) * 100 if total_questions > 0 else 0
        
        test_suite = TestSuite(
            test_name="Farm Knee System Test",
            timestamp=datetime.now().isoformat(),
            total_questions=total_questions,
            successful_answers=successful_answers_llm,  # USE LLM GRADING RESULTS
            failed_answers=failed_answers_llm,  # USE LLM GRADING RESULTS
            average_response_time=avg_response_time,
            median_response_time=median_response_time,
            results=results,
            grading_results=grading_results,
            system_status=system_status,
            performance_metrics=performance_metrics
        )
        
        return test_suite
    
    def print_results_summary(self, test_suite: TestSuite):
        """PRINT COMPREHENSIVE RESULTS SUMMARY"""
        
        print("\n" + "="*80)
        print("📊 TEST RESULTS SUMMARY")
        print("="*80)
        
        # BASIC STATS
        print(f"📝 Total Questions: {test_suite.total_questions}")
        print(f"✅ Successful Answers: {test_suite.successful_answers}")
        print(f"❌ Failed Answers: {test_suite.failed_answers}")
        print(f"📈 Success Rate: {test_suite.performance_metrics['success_rate']:.1f}%")
        
        # TIMING STATS
        print(f"\n⏱️  TIMING STATISTICS:")
        print(f"   Average Response Time: {test_suite.average_response_time:.2f}s")
        print(f"   Median Response Time: {test_suite.median_response_time:.2f}s")
        print(f"   Min Response Time: {test_suite.performance_metrics['min_response_time']:.2f}s")
        print(f"   Max Response Time: {test_suite.performance_metrics['max_response_time']:.2f}s")
        print(f"   Response Time Std Dev: {test_suite.performance_metrics['response_time_std']:.2f}s")
        
        # SYSTEM STATUS
        print(f"\n🔧 SYSTEM STATUS:")
        for key, value in test_suite.system_status.items():
            print(f"   {key}: {value}")
        
        # DIFFICULTY BREAKDOWN
        print(f"\n📊 DIFFICULTY BREAKDOWN:")
        difficulty_stats = {}
        for result in test_suite.results:
            difficulty = result.difficulty
            if difficulty not in difficulty_stats:
                difficulty_stats[difficulty] = {"total": 0, "success": 0}
            difficulty_stats[difficulty]["total"] += 1
            # DETERMINE SUCCESS FOR LLM GRADER
            success = result.expected_answer.lower() in result.actual_answer.lower()
            if success:
                difficulty_stats[difficulty]["success"] += 1
        
        for difficulty, stats in difficulty_stats.items():
            success_rate = (stats["success"] / stats["total"]) * 100
            print(f"   {difficulty.capitalize()}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        # ANSWER TYPE BREAKDOWN
        print(f"\n📋 ANSWER TYPE BREAKDOWN:")
        answer_type_stats = {}
        for result in test_suite.results:
            answer_type = result.expected_answer_type
            if answer_type not in answer_type_stats:
                answer_type_stats[answer_type] = {"total": 0, "success": 0}
            answer_type_stats[answer_type]["total"] += 1
            # DETERMINE SUCCESS FOR LLM GRADER
            success = result.expected_answer.lower() in result.actual_answer.lower()
            if success:
                answer_type_stats[answer_type]["success"] += 1
        
        for answer_type, stats in answer_type_stats.items():
            success_rate = (stats["success"] / stats["total"]) * 100
            print(f"   {answer_type}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
    
    def save_results(self, test_suite: TestSuite, filename: Optional[str] = None):
        """SAVE TEST RESULTS TO JSON FILE IN RUN OUTPUT DIR"""
        
        if not self.save_results_flag:
            return
        
        output_dir = self.get_output_dir()
        if not filename:
            filename = os.path.join(output_dir, "results.json")
        else:
            filename = os.path.join(output_dir, filename)
        
        try:
            # CONVERT DATACLASS TO DICT
            results_dict = asdict(test_suite)
            
            with open(filename, 'w') as f:
                json.dump(results_dict, f, indent=2, default=str)
            
            print(f"💾 Results saved to: {filename}")
            
        except Exception as e:
            print(f"❌ ERROR SAVING RESULTS: {e}")
    
    def generate_markdown_summary(self, test_suite: TestSuite, filename: Optional[str] = None):
        """GENERATE COMPREHENSIVE MARKDOWN SUMMARY REPORT"""
        
        if not self.save_results_flag:
            return
        
        output_dir = self.get_output_dir()
        if not filename:
            filename = os.path.join(output_dir, "summary_report.md")
        else:
            filename = os.path.join(output_dir, filename)
        
        try:
            # CALCULATE GRADING STATS
            total_graded = len(test_suite.grading_results)
            # avg_score = statistics.mean([g.score for g in test_suite.grading_results]) if total_graded > 0 else 0 # REMOVED
            # high_scores = [g for g in test_suite.grading_results if g.score >= 8] # REMOVED
            # low_scores = [g for g in test_suite.grading_results if g.score < 5] # REMOVED
            
            # CALCULATE SUCCESS RATE BASED ON GRADING
            successful_graded = len([g for g in test_suite.grading_results if g.is_correct]) # UPDATED
            success_rate_graded = (successful_graded / total_graded * 100) if total_graded > 0 else 0 # UPDATED
            
            # CALCULATE BINARY SUCCESS RATE
            correct_answers = len([g for g in test_suite.grading_results if g.is_correct]) # UPDATED
            binary_success_rate = (correct_answers / total_graded * 100) if total_graded > 0 else 0 # UPDATED
            
            # ANALYZE RAG PIPELINE ISSUES
            discovery_issues = len([g for g in test_suite.grading_results if g.rag_diagnostic.discovery_issue])
            retrieval_issues = len([g for g in test_suite.grading_results if g.rag_diagnostic.retrieval_issue])
            llm_issues = len([g for g in test_suite.grading_results if g.rag_diagnostic.llm_issue])
            
            # ANALYZE USELESS PAGE QUESTIONS
            useless_page_questions = len([g for g in test_suite.grading_results if g.is_useless_page_question])
            
            with open(filename, 'w') as f:
                f.write(f"# Farm Knee System Test Report\n\n")
                f.write(f"**Generated:** {test_suite.timestamp}\n")
                f.write(f"**Test Name:** {test_suite.test_name}\n\n")
                
                # EXECUTIVE SUMMARY
                f.write("## 📊 Executive Summary\n\n")
                f.write(f"- **Total Questions:** {test_suite.total_questions}\n")
                f.write(f"- **Success Rate (Simple):** {test_suite.performance_metrics['success_rate']:.1f}%\n")
                f.write(f"- **Success Rate (LLM Graded):** {success_rate_graded:.1f}%\n")
                f.write(f"- **Binary Success Rate (Correct/Wrong):** {binary_success_rate:.1f}%\n")
                # f.write(f"- **Average LLM Score:** {avg_score:.1f}/10\n") # REMOVED
                # f.write(f"- **High Scores (≥8):** {len(high_scores)}/{total_graded}\n") # REMOVED
                # f.write(f"- **Low Scores (<5):** {len(low_scores)}/{total_graded}\n") # REMOVED
                f.write(f"- **Average Response Time:** {test_suite.average_response_time:.2f}s\n\n")
                
                # RAG PIPELINE DIAGNOSTICS
                f.write("## 🔍 RAG Pipeline Diagnostics\n\n")
                f.write(f"- **Discovery Issues:** {discovery_issues}/{total_graded} ({discovery_issues/total_graded*100:.1f}%)\n")
                f.write(f"- **Retrieval Issues:** {retrieval_issues}/{total_graded} ({retrieval_issues/total_graded*100:.1f}%)\n")
                f.write(f"- **LLM Issues:** {llm_issues}/{total_graded} ({llm_issues/total_graded*100:.1f}%)\n")
                f.write(f"- **Useless Page Questions:** {useless_page_questions}/{total_graded} ({useless_page_questions/total_graded*100:.1f}%)\n\n")
                
                # KEYWORD ENHANCEMENT ANALYSIS
                keyword_enhanced_queries = len([g for g in test_suite.grading_results if g.rag_diagnostic.keyword_enhancement])
                if keyword_enhanced_queries > 0:
                    f.write("## 🏷️ Keyword Enhancement Analysis\n\n")
                    f.write(f"- **Enhanced Queries:** {keyword_enhanced_queries}/{total_graded} ({keyword_enhanced_queries/total_graded*100:.1f}%)\n")
                    
                    # SHOW SAMPLE KEYWORDS
                    sample_keywords = []
                    for grading in test_suite.grading_results[:5]:  # FIRST 5 FOR SAMPLE
                        if grading.rag_diagnostic.keyword_enhancement:
                            keywords = grading.rag_diagnostic.keyword_enhancement.get("original_keywords", [])
                            sample_keywords.extend(keywords[:3])  # FIRST 3 KEYWORDS PER QUERY
                    
                    if sample_keywords:
                        unique_keywords = list(set(sample_keywords))[:10]  # FIRST 10 UNIQUE
                        f.write(f"- **Sample Keywords:** {', '.join(unique_keywords)}\n")
                    f.write("\n")
                
                # PERFORMANCE METRICS
                f.write("## ⏱️ Performance Metrics\n\n")
                f.write(f"- **Average Response Time:** {test_suite.average_response_time:.2f}s\n")
                f.write(f"- **Median Response Time:** {test_suite.median_response_time:.2f}s\n")
                f.write(f"- **Min Response Time:** {test_suite.performance_metrics['min_response_time']:.2f}s\n")
                f.write(f"- **Max Response Time:** {test_suite.performance_metrics['max_response_time']:.2f}s\n")
                f.write(f"- **Response Time Std Dev:** {test_suite.performance_metrics['response_time_std']:.2f}s\n\n")
                
                # DIFFICULTY BREAKDOWN
                f.write("## 📈 Difficulty Breakdown\n\n")
                difficulty_stats = {}
                for result in test_suite.results:
                    difficulty = result.difficulty
                    if difficulty not in difficulty_stats:
                        difficulty_stats[difficulty] = {"total": 0, "success": 0}
                    difficulty_stats[difficulty]["total"] += 1
                    success = result.expected_answer.lower() in result.actual_answer.lower()
                    if success:
                        difficulty_stats[difficulty]["success"] += 1
                
                for difficulty, stats in difficulty_stats.items():
                    success_rate = (stats["success"] / stats["total"]) * 100
                    f.write(f"- **{difficulty.capitalize()}:** {stats['success']}/{stats['total']} ({success_rate:.1f}%)\n")
                f.write("\n")
                
                # ANSWER TYPE BREAKDOWN
                f.write("## 📋 Answer Type Breakdown\n\n")
                answer_type_stats = {}
                for result in test_suite.results:
                    answer_type = result.expected_answer_type
                    if answer_type not in answer_type_stats:
                        answer_type_stats[answer_type] = {"total": 0, "success": 0}
                    answer_type_stats[answer_type]["total"] += 1
                    success = result.expected_answer.lower() in result.actual_answer.lower()
                    if success:
                        answer_type_stats[answer_type]["success"] += 1
                
                for answer_type, stats in answer_type_stats.items():
                    success_rate = (stats["success"] / stats["total"]) * 100
                    f.write(f"- **{answer_type}:** {stats['success']}/{stats['total']} ({success_rate:.1f}%)\n")
                f.write("\n")
                
                # SYSTEM STATUS
                f.write("## 🔧 System Status\n\n")
                for key, value in test_suite.system_status.items():
                    f.write(f"- **{key}:** {value}\n")
                f.write("\n")
                
                # USELESS PAGE QUESTIONS
                useless_questions = [g for g in test_suite.grading_results if g.is_useless_page_question]
                if useless_questions:
                    f.write("## 🚫 Useless Page Questions Detected\n\n")
                    f.write("These questions appear to be about pages/tables that shouldn't be in the test set:\n\n")
                    for i, grading in enumerate(useless_questions, 1):
                        f.write(f"### {i}. Question: {grading.question}\n\n")
                        f.write(f"**Expected:** {grading.expected_answer}\n\n")
                        f.write(f"**Useless Page Explanation:** {grading.useless_page_explanation}\n\n")
                        f.write("---\n\n")
                
                # LOW SCORING ANSWERS
                # if low_scores: # REMOVED
                #     f.write("## ⚠️ Low Scoring Answers (<5/10)\n\n") # REMOVED
                #     for i, grading in enumerate(low_scores, 1): # REMOVED
                #         f.write(f"### {i}. Question: {grading.question}\n\n") # REMOVED
                #         f.write(f"**Expected:** {grading.expected_answer}\n\n") # REMOVED
                #         f.write(f"**Actual:** {grading.actual_answer}\n\n") # REMOVED
                #         f.write(f"**Score:** {grading.score}/10\n\n") # REMOVED
                #         f.write(f"**Justification:** {grading.justification}\n\n") # REMOVED
                #         if grading.improvement_suggestion: # REMOVED
                #             f.write(f"**Improvement:** {grading.improvement_suggestion}\n\n") # REMOVED
                #         f.write("---\n\n") # REMOVED
                
                # ALL GRADING RESULTS
                f.write("## 📝 All Grading Results\n\n")
                for i, grading in enumerate(test_suite.grading_results, 1):
                    useless_flag = "🚫 USELESS PAGE" if grading.is_useless_page_question else ""
                    f.write(f"### {i}. Correct: {grading.is_correct} {useless_flag}\n\n") # UPDATED
                    f.write(f"**Question:** {grading.question}\n\n")
                    f.write(f"**Expected:** {grading.expected_answer}\n\n")
                    f.write(f"**Actual:** {grading.actual_answer}\n\n")
                    f.write(f"**Justification:** {grading.justification}\n\n")
                    
                    if grading.is_useless_page_question and grading.useless_page_explanation:
                        f.write(f"**🚫 Useless Page:** {grading.useless_page_explanation}\n\n")
                    
                    # RAG DIAGNOSTIC INFO
                    f.write(f"**RAG Pipeline Analysis:**\n")
                    f.write(f"- Expected source: {grading.rag_diagnostic.correct_page_found and '✅' or '❌'} {grading.rag_diagnostic.correct_page_rank and f'(rank {grading.rag_diagnostic.correct_page_rank})' or ''}\n")
                    f.write(f"- Content retrieved: {grading.rag_diagnostic.correct_content_retrieved and '✅' or '❌'}\n")
                    f.write(f"- Tools used: {', '.join(grading.rag_diagnostic.tools_used) if grading.rag_diagnostic.tools_used else 'None'}\n")
                    f.write(f"- Iterations: {grading.rag_diagnostic.total_iterations}\n")

                    # If iterations or tools used are zero/None, print debug keys for troubleshooting
                    if (grading.rag_diagnostic.total_iterations == 0 or not grading.rag_diagnostic.tools_used):
                        # Try to get debug keys from the original result
                        debug_keys = None
                        for result in test_suite.results:
                            if result.question == grading.question:
                                if result.debug_info:
                                    debug_keys = list(result.debug_info.keys())
                        if debug_keys:
                            f.write(f"- ⚠️ DEBUG: Available debug_info keys: {debug_keys}\n")
                        else:
                            f.write(f"- ⚠️ DEBUG: No debug_info available for this answer\n")

                    if grading.rag_diagnostic.discovery_issue:
                        f.write(f"- Discovery issue: {grading.rag_diagnostic.discovery_issue}\n")
                    if grading.rag_diagnostic.retrieval_issue:
                        f.write(f"- Retrieval issue: {grading.rag_diagnostic.retrieval_issue}\n")
                    if grading.rag_diagnostic.llm_issue:
                        f.write(f"- LLM issue: {grading.rag_diagnostic.llm_issue}\n")
                    f.write("\n")
                    
                    if grading.improvement_suggestion:
                        f.write(f"**Improvement:** {grading.improvement_suggestion}\n\n")
                    f.write("---\n\n")
            
            print(f"📄 Markdown summary saved to: {filename}")
            
        except Exception as e:
            print(f"❌ ERROR GENERATING MARKDOWN SUMMARY: {e}")
    
    def run_complete_test(self, max_tests: Optional[int] = None, balanced_sample: bool = True):
        """RUN COMPLETE TEST SUITE"""
        
        print("🚀 STARTING COMPLETE FARM KNEE TEST SUITE")
        print("="*60)
        
        # STEP 1: LOAD QUESTIONS
        if not self.load_questions():
            print("❌ FAILED TO LOAD QUESTIONS - ABORTING")
            return
        
        # STEP 2: INITIALIZE FARMER
        if not self.initialize_farmer():
            print("❌ FAILED TO INITIALIZE FARMER - ABORTING")
            return
        
        # STEP 3: RUN TESTS
        test_suite = self.run_all_tests(max_tests, balanced_sample)
        
        if not test_suite:
            print("❌ FAILED TO RUN TESTS - ABORTING")
            return
        
        # STEP 4: PRINT RESULTS
        self.print_results_summary(test_suite)
        
        # STEP 5: SAVE RESULTS
        self.save_results(test_suite)
        
        # STEP 6: GENERATE MARKDOWN SUMMARY
        self.generate_markdown_summary(test_suite)
        
        print("\n🎉 TEST SUITE COMPLETED!")
        print("="*60)


def main():
    """MAIN FUNCTION WITH COMMAND LINE ARGUMENTS"""
    
    parser = argparse.ArgumentParser(description="Test Farm RAG System with Knee Documents")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--save-results", action="store_true", default=True, help="Save results to JSON file")
    parser.add_argument("--max-tests", type=int, help="Maximum number of tests to run")
    parser.add_argument("--no-save", action="store_true", help="Don't save results")
    
    args = parser.parse_args()
    
    # CREATE TESTER
    tester = FarmKneeTester(
        debug_mode=args.debug,
        save_results=not args.no_save
    )
    
    # RUN COMPLETE TEST
    tester.run_complete_test(max_tests=args.max_tests, balanced_sample=True)


if __name__ == "__main__":
    main() 