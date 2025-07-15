#!/usr/bin/env python3
"""
SIMPLE RELEVANCE TEST
=====================

Test using only relevance finder to get top 5 pages and tables,
then pass directly to LLM to generate answer (skip full RAG).
"""

import sys
import os
import json

# ADD FARM TO PATH
farm_path = os.path.join(os.path.dirname(__file__), 'farm/src')
sys.path.insert(0, farm_path)

from farm.farmer import Farmer
from farm.toolshed.exploration.relevance_finder import RelevanceFinder
from farm.toolshed.retrieval.table_retriever import TableRetriever
from farm.toolshed.retrieval.page_retriever import PageRetriever
from farm.barn import Barn

def test_simple_relevance():
    """TEST SIMPLE RELEVANCE-BASED ANSWERING"""
    
    print("🚀 SIMPLE RELEVANCE TEST")
    print("=" * 50)
    
    # INITIALIZE FARMER
    print("🚜 INITIALIZING FARMER...")
    farmer = Farmer()
    
    # LOAD TS KNEE DOCUMENT
    print("📄 Loading TS knee document...")
    success = farmer.load_document("ts_knee", "data/jsons/ts_knee_original_20250701_175753.json")
    if not success:
        print("❌ Failed to load TS knee document")
        return
    
    print("✅ TS knee document loaded successfully")
    
    # GET RELEVANCE FINDER
    relevance_finder = RelevanceFinder(farmer.barn.silo)
    
    # TEST QUESTIONS
    test_questions = [
        "What is the thickness of the 32mm patella?",
        "How much more M/L space is there in a size 6 femur vs a size 5?",
        "What are your asymmetric patella options?",
        "What are the TS poly thicknesses?"
    ]
    
    print(f"\n🧪 TESTING {len(test_questions)} QUESTIONS...")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 Question {i}: {question}")
        print("-" * 40)
        
        # FIND RELEVANT CONTENT
        print("🔍 FINDING RELEVANT CONTENT...")
        relevant_tables = relevance_finder.find_relevant_tables(question)
        relevant_pages = relevance_finder.find_relevant_pages(question)
        
        print(f"📊 Found {len(relevant_tables)} relevant tables, {len(relevant_pages)} relevant pages")
        
        # GET TOP 5 TABLES AND PAGES
        top_tables = relevant_tables[:5]
        top_pages = relevant_pages[:5]
        
        # COLLECT TABLE DATA
        table_retriever = TableRetriever(farmer.barn.silo)
        page_retriever = PageRetriever(farmer.barn.silo)
        
        table_data = []
        for table in top_tables:
            try:
                data = table_retriever.get_table_data(table["table_name"])
                if data:
                    table_data.append({
                        "table_name": table["table_name"],
                        "relevance_score": table["relevance_score"],
                        "data": data
                    })
            except Exception as e:
                print(f"⚠️ Error getting table {table['table_name']}: {e}")
        
        # COLLECT PAGE DATA
        page_data = []
        for page in top_pages:
            try:
                content = page_retriever.get_page_content(page["page_title"])
                if content:
                    page_data.append({
                        "page_title": page["page_title"],
                        "relevance_score": page["relevance_score"],
                        "content": content
                    })
            except Exception as e:
                print(f"⚠️ Error getting page {page['page_title']}: {e}")
        
        # SHOW CONTEXT: TABLE AND PAGE TITLES
        if top_tables:
            print("Tables passed to LLM:")
            for t in top_tables:
                print(f"  - {t['table_name']}")
        if top_pages:
            print("Pages passed to LLM:")
            for p in top_pages:
                print(f"  - {p['page_title']}")
        
        # GENERATE ANSWER WITH LLM
        print("🤖 GENERATING ANSWER...")
        try:
            # CREATE CONTEXT FORMAT THAT MATCHES WHAT _format_context_for_llm EXPECTS
            context_data = {
                "retrieval_data": {}
            }
            
            # ADD TABLE DATA IN THE EXPECTED FORMAT
            if table_data:
                context_data["retrieval_data"]["get_table_data"] = []
                for table in table_data:
                    context_data["retrieval_data"]["get_table_data"].append({
                        "table_title": table["table_name"],
                        "row_count": len(table["data"]["rows"]) if table["data"].get("rows") else 0,
                        "column_count": len(table["data"]["rows"][0]) if table["data"].get("rows") and table["data"]["rows"] else 0,
                        "columns": table["data"].get("columns", []),
                        "rows": table["data"].get("rows", [])
                    })
            
            # ADD PAGE DATA IN THE EXPECTED FORMAT
            if page_data:
                context_data["retrieval_data"]["get_page_content"] = []
                for page in page_data:
                    context_data["retrieval_data"]["get_page_content"].append({
                        "page_title": page["page_title"],
                        "content": page["content"],
                        "table_count": 0  # WE DON'T HAVE THIS INFO
                    })
            
            # USE THE BARN'S LLM METHOD
            answer = farmer.barn._generate_llm_response(question, context_data)
            print(f"💬 Answer: {answer}")
        except Exception as e:
            print(f"❌ Error generating answer: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    test_simple_relevance() 