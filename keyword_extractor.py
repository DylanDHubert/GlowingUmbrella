#!/usr/bin/env python3
"""
KEYWORD EXTRACTION FOR FARM RAG SYSTEM
======================================

Extracts relevant keywords from questions to improve search term generation
for the 3-phase RAG system (Discovery, Exploration, Retrieval).
"""

import re
import json
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ExtractedKeywords:
    """STRUCTURE FOR EXTRACTED KEYWORDS"""
    primary_terms: List[str]  # MAIN SEARCH TERMS
    secondary_terms: List[str]  # SUPPORTING TERMS
    data_terms: List[str]  # NUMBERS, DATES, MEASUREMENTS
    context_terms: List[str]  # CONTEXT WORDS
    original_query: str  # ORIGINAL QUESTION


class KeywordExtractor:
    """KEYWORD EXTRACTION FOR IMPROVING RAG SEARCH TERMS"""
    
    def __init__(self):
        """INITIALIZE KEYWORD EXTRACTOR"""
        
        # COMMON MEDICAL/CLINICAL TERMS
        self.medical_terms = {
            "score", "scores", "measurement", "measurements", "outcome", "outcomes",
            "clinical", "patient", "patients", "study", "studies", "trial", "trials",
            "procedure", "procedures", "surgery", "surgical", "treatment", "treatments",
            "component", "components", "implant", "implants", "device", "devices",
            "system", "systems", "protocol", "protocols", "guideline", "guidelines",
            "follow-up", "followup", "preoperative", "postoperative", "post-op",
            "year", "years", "month", "months", "week", "weeks", "day", "days",
            "percentage", "percent", "%", "rate", "rates", "survival", "survivorship",
            "complication", "complications", "revision", "revisions", "failure", "failures"
        }
        
        # KNEE-SPECIFIC TERMS
        self.knee_terms = {
            "knee", "knees", "arthroplasty", "arthroplasties", "TKA", "TKR",
            "femoral", "tibial", "patellar", "patella", "femur", "tibia",
            "anterior", "posterior", "medial", "lateral", "cruciate", "ligament",
            "cartilage", "meniscus", "osteotomy", "resection", "implantation",
            "triathlon", "tritanium", "cementless", "cemented", "beaded", "peri-apatite"
        }
        
        # DATA/MEASUREMENT TERMS
        self.data_terms = {
            "mean", "average", "median", "mode", "standard deviation", "std",
            "range", "minimum", "maximum", "total", "count", "number", "amount",
            "percentage", "percent", "rate", "ratio", "proportion", "frequency"
        }
        
        # COMPARISON TERMS
        self.comparison_terms = {
            "compare", "comparison", "versus", "vs", "against", "between",
            "difference", "differences", "similar", "different", "same",
            "higher", "lower", "greater", "less", "more", "fewer",
            "increase", "decrease", "improve", "worse", "better"
        }
    
    def extract_keywords(self, query: str) -> ExtractedKeywords:
        """EXTRACT KEYWORDS FROM QUERY"""
        
        # NORMALIZE QUERY
        query_lower = query.lower()
        
        # EXTRACT PRIMARY TERMS (MOST IMPORTANT FOR SEARCH)
        primary_terms = []
        
        # LOOK FOR SPECIFIC ENTITIES (LIKE "Oxford Knee Score")
        specific_entities = self._extract_specific_entities(query)
        primary_terms.extend(specific_entities)
        
        # LOOK FOR MEDICAL/KNEE TERMS
        medical_found = [term for term in self.medical_terms if term in query_lower]
        knee_found = [term for term in self.knee_terms if term in query_lower]
        primary_terms.extend(medical_found)
        primary_terms.extend(knee_found)
        
        # EXTRACT SECONDARY TERMS (SUPPORTING CONTEXT)
        secondary_terms = []
        
        # LOOK FOR DATA/MEASUREMENT TERMS
        data_found = [term for term in self.data_terms if term in query_lower]
        secondary_terms.extend(data_found)
        
        # LOOK FOR COMPARISON TERMS
        comparison_found = [term for term in self.comparison_terms if term in query_lower]
        secondary_terms.extend(comparison_found)
        
        # EXTRACT DATA TERMS (NUMBERS, DATES, ETC.)
        data_terms = self._extract_data_terms(query)
        
        # EXTRACT CONTEXT TERMS (GENERAL CONTEXT WORDS)
        context_terms = self._extract_context_terms(query)
        
        # REMOVE DUPLICATES AND CLEAN
        primary_terms = list(set(primary_terms))
        secondary_terms = list(set(secondary_terms))
        data_terms = list(set(data_terms))
        context_terms = list(set(context_terms))
        
        return ExtractedKeywords(
            primary_terms=primary_terms,
            secondary_terms=secondary_terms,
            data_terms=data_terms,
            context_terms=context_terms,
            original_query=query
        )
    
    def _extract_specific_entities(self, query: str) -> List[str]:
        """EXTRACT SPECIFIC ENTITIES LIKE 'Oxford Knee Score'"""
        entities = []
        
        # LOOK FOR COMMON PATTERNS
        patterns = [
            r"Oxford Knee Score\s*\(OKS\)",
            r"Oxford Knee Score",
            r"OKS",
            r"Triathlon\s+Total\s+Knee\s+System",
            r"Triathlon\s+TKA",
            r"Triathlon\s+TKR",
            r"Tritanium",
            r"Peri-Apatite",
            r"FlexRod",
            r"X3\s+Polyethylene"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            entities.extend(matches)
        
        return entities
    
    def _extract_data_terms(self, query: str) -> List[str]:
        """EXTRACT NUMBERS, DATES, MEASUREMENTS"""
        data_terms = []
        
        # NUMBERS
        numbers = re.findall(r'\d+(?:\.\d+)?', query)
        data_terms.extend(numbers)
        
        # PERCENTAGES
        percentages = re.findall(r'\d+(?:\.\d+)?%', query)
        data_terms.extend(percentages)
        
        # YEARS
        years = re.findall(r'\d+\s*year', query)
        data_terms.extend(years)
        
        # MEASUREMENTS
        measurements = re.findall(r'\d+(?:\.\d+)?\s*(?:mm|cm|inches?)', query)
        data_terms.extend(measurements)
        
        return data_terms
    
    def _extract_context_terms(self, query: str) -> List[str]:
        """EXTRACT GENERAL CONTEXT WORDS"""
        # REMOVE COMMON STOP WORDS
        stop_words = {
            "what", "when", "where", "who", "why", "how", "is", "are", "was", "were",
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "up", "about", "into", "through", "during",
            "before", "after", "above", "below", "between", "among", "within",
            "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they"
        }
        
        words = re.findall(r'\b\w+\b', query.lower())
        context_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        return context_words[:10]  # LIMIT TO TOP 10 CONTEXT WORDS
    
    def generate_search_terms(self, keywords: ExtractedKeywords) -> List[str]:
        """GENERATE OPTIMIZED SEARCH TERMS FOR RAG SYSTEM"""
        search_terms = []
        
        # ADD PRIMARY TERMS (HIGHEST PRIORITY)
        search_terms.extend(keywords.primary_terms)
        
        # ADD SECONDARY TERMS
        search_terms.extend(keywords.secondary_terms)
        
        # ADD DATA TERMS (IF RELEVANT)
        if keywords.data_terms:
            search_terms.extend(keywords.data_terms[:3])  # LIMIT DATA TERMS
        
        # ADD CONTEXT TERMS (LOWER PRIORITY)
        search_terms.extend(keywords.context_terms[:5])  # LIMIT CONTEXT TERMS
        
        # REMOVE DUPLICATES AND CLEAN
        search_terms = list(set(search_terms))
        
        # REMOVE EMPTY STRINGS
        search_terms = [term for term in search_terms if term.strip()]
        
        return search_terms


# TEST FUNCTION
def test_keyword_extraction():
    """TEST THE KEYWORD EXTRACTOR WITH OKS QUESTIONS"""
    
    extractor = KeywordExtractor()
    
    test_questions = [
        "What was the mean Oxford Knee Score (OKS) for patients with Triathlon TKA at the preoperative stage?",
        "Compare the mean OKS at the 1-year follow-up to the mean OKS at the 10-year follow-up for patients with Triathlon TKA.",
        "What trend can be observed in the mean OKS scores from preoperative to 10 years post-operation?",
        "What is the mean OKS at 5 years post-operation for patients with Triathlon TKA?",
        "What clinical significance does the Oxford Knee Score (OKS) have for patients undergoing Triathlon Total Knee Arthroplasty?"
    ]
    
    print("🧪 TESTING KEYWORD EXTRACTION")
    print("="*50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        
        keywords = extractor.extract_keywords(question)
        search_terms = extractor.generate_search_terms(keywords)
        
        print(f"   Primary terms: {keywords.primary_terms}")
        print(f"   Secondary terms: {keywords.secondary_terms}")
        print(f"   Data terms: {keywords.data_terms}")
        print(f"   Search terms: {search_terms}")
        print()


if __name__ == "__main__":
    test_keyword_extraction() 