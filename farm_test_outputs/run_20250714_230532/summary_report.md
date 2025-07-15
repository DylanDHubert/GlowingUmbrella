# Farm Knee System Test Report

**Generated:** 2025-07-14T23:05:32.497528
**Test Name:** Farm Knee System Test

## 📊 Executive Summary

- **Total Questions:** 4
- **Success Rate (Simple):** 75.0%
- **Success Rate (LLM Graded):** 75.0%
- **Binary Success Rate (Correct/Wrong):** 75.0%
- **Average Response Time:** 5.20s

## 🔍 RAG Pipeline Diagnostics

- **Discovery Issues:** 0/4 (0.0%)
- **Retrieval Issues:** 0/4 (0.0%)
- **LLM Issues:** 0/4 (0.0%)
- **Useless Page Questions:** 0/4 (0.0%)

## 🏷️ Keyword Enhancement Analysis

- **Enhanced Queries:** 4/4 (100.0%)
- **Sample Keywords:** cause, instrument, percentage, patients, fitted, number, removing, survivorship, used, triathlon

## ⏱️ Performance Metrics

- **Average Response Time:** 5.20s
- **Median Response Time:** 5.02s
- **Min Response Time:** 3.99s
- **Max Response Time:** 6.78s
- **Response Time Std Dev:** 1.18s

## 📈 Difficulty Breakdown

- **Easy:** 3/4 (75.0%)

## 📋 Answer Type Breakdown

- **data_extraction:** 2/3 (66.7%)
- **technical:** 1/1 (100.0%)

## 🔧 System Status

- **llm_configured:** True
- **documents_loaded:** True
- **total_documents:** 3
- **max_context_length:** 4000
- **confidence_threshold:** 0.3

## 📝 All Grading Results

### 1. Correct: True 

**Question:** What is the instrument item number for the Impaction Handle?

**Expected:** 6541-4-810

**Actual:** The instrument item number for the Impaction Handle is **6541-4-810**.

**Justification:** The answer provided matches the expected answer exactly.

**RAG Pipeline Analysis:**
- Expected source: ✅ (rank 8)
- Content retrieved: ✅
- Tools used: find_relevant_tables, get_row_data, get_table_data
- Iterations: 5

---

### 2. Correct: False 

**Question:** What percentage of patients can be fitted using the FlexRod according to the CT scan-based study?

**Expected:** 99.4%

**Actual:** I currently do not have specific data available regarding the percentage of patients that can be fitted using the FlexRod according to a CT scan-based study. If you have any additional information or data on this topic, please provide it, and I can assist you further.

**Justification:** The answer provided does not contain the exact expected value of 99.4% as requested in the question.

**RAG Pipeline Analysis:**
- Expected source: ✅ (rank 1)
- Content retrieved: ✅
- Tools used: find_relevant_tables, get_table_data
- Iterations: 5

**Improvement:** The system should be improved to extract and provide specific data points accurately in response to questions.

---

### 3. Correct: True 

**Question:** Which tool is used for removing posterior osteophytes during the femoral trial assessment?

**Expected:** Posterior Osteophyte Removal Tool

**Actual:** The tool used for removing posterior osteophytes during the femoral trial assessment is the "Posterior Osteophyte Removal Tool." This tool is attached to the Impaction Handle according to the provided information.

**Justification:** The answer provided matches the expected answer by correctly identifying the 'Posterior Osteophyte Removal Tool' as the tool used for removing posterior osteophytes during the femoral trial assessment.

**RAG Pipeline Analysis:**
- Expected source: ✅ (rank 1)
- Content retrieved: ✅
- Tools used: find_relevant_tables, get_page_content, get_table_data
- Iterations: 5

---

### 4. Correct: True 

**Question:** What is the Triathlon All-Cause Survivorship percentage at 10 years according to Mistry et al. 2016?

**Expected:** 99.0%

**Actual:** The Triathlon All-Cause Survivorship percentage at 10 years according to Mistry et al. 2016 is 99.0%.

**Justification:** The answer provided matches the expected answer exactly.

**RAG Pipeline Analysis:**
- Expected source: ✅ (rank 1)
- Content retrieved: ✅
- Tools used: get_row_data, get_table_data, table_summary
- Iterations: 5

---

