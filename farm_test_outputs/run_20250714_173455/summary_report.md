# Farm Knee System Test Report

**Generated:** 2025-07-14T17:34:55.866581
**Test Name:** Farm Knee System Test

## 📊 Executive Summary

- **Total Questions:** 2
- **Success Rate (Simple):** 50.0%
- **Success Rate (LLM Graded):** 50.0%
- **Binary Success Rate (Correct/Wrong):** 50.0%
- **Average Response Time:** 8.82s

## 🔍 RAG Pipeline Diagnostics

- **Discovery Issues:** 0/2 (0.0%)
- **Retrieval Issues:** 0/2 (0.0%)
- **LLM Issues:** 0/2 (0.0%)
- **Useless Page Questions:** 0/2 (0.0%)

## 🏷️ Keyword Enhancement Analysis

- **Enhanced Queries:** 2/2 (100.0%)
- **Sample Keywords:** patients, fitted, complete, recommended, tool, percentage

## ⏱️ Performance Metrics

- **Average Response Time:** 8.82s
- **Median Response Time:** 8.82s
- **Min Response Time:** 4.68s
- **Max Response Time:** 12.96s
- **Response Time Std Dev:** 5.86s

## 📈 Difficulty Breakdown

- **Easy:** 1/2 (50.0%)

## 📋 Answer Type Breakdown

- **data_extraction:** 0/1 (0.0%)
- **instruction:** 1/1 (100.0%)

## 🔧 System Status

- **llm_configured:** True
- **documents_loaded:** True
- **total_documents:** 3
- **max_context_length:** 4000
- **confidence_threshold:** 0.3

## 📝 All Grading Results

### 1. Correct: False 

**Question:** What percentage of patients can be fitted using the FlexRod according to the CT scan-based study?

**Expected:** 99.4%

**Actual:** Based on the available data, there is no specific information regarding the percentage of patients that can be fitted using the FlexRod according to the CT scan-based study. As such, I do not have the data to provide the exact percentage of patients fitted using the FlexRod based on the scan-based study. If this information is crucial, additional data or sources related to the study would be needed to determine the percentage accurately.

**Justification:** The answer is incorrect as it states that there is no specific information regarding the percentage of patients that can be fitted using the FlexRod according to the CT scan-based study, while the expected answer is 99.4%.

**RAG Pipeline Analysis:**
- Expected source: ✅ (rank 1)
- Content retrieved: ✅
- Tools used: get_page_content, table_summary
- Iterations: 5

---

### 2. Correct: True 

**Question:** What is the recommended tool to complete the preparation of the box after using the Saw Only option?

**Expected:** Triathlon PS Femoral Finishing Punch

**Actual:** The recommended tool to complete the preparation of the box after using the "Saw Only" option is the "Triathlon PS Femoral Finishing Punch." This tool is optional but recommended for completing the box preparation. After using either option A or option B (Saw Only), the surgeon may choose to use the Triathlon PS Femoral Finishing Punch to finalize the preparation of the box.

Make sure that after using the Saw Only option, the prepared box is properly completed and all remaining bone is removed before trialing with a PS Femoral Trial.

**Justification:** The answer provides the correct tool, the Triathlon PS Femoral Finishing Punch, for completing the preparation of the box after using the Saw Only option.

**RAG Pipeline Analysis:**
- Expected source: ✅ (rank 1)
- Content retrieved: ✅
- Tools used: get_page_content, get_table_data
- Iterations: 5

---

