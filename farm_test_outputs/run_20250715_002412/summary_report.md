# Farm Knee System Test Report

**Generated:** 2025-07-15T00:24:12.720670
**Test Name:** Farm Knee System Test

## 📊 Executive Summary

- **Total Questions:** 4
- **Success Rate (Simple):** 50.0%
- **Success Rate (LLM Graded):** 50.0%
- **Binary Success Rate (Correct/Wrong):** 50.0%
- **Average Response Time:** 8.51s

## 🔍 RAG Pipeline Diagnostics

- **Discovery Issues:** 0/4 (0.0%)
- **Retrieval Issues:** 0/4 (0.0%)
- **LLM Issues:** 0/4 (0.0%)
- **Useless Page Questions:** 0/4 (0.0%)

## 🏷️ Keyword Enhancement Analysis

- **Enhanced Queries:** 4/4 (100.0%)
- **Sample Keywords:** reasons, done, used, flexion, using, materials, possible, maximum, page, degrees

## ⏱️ Performance Metrics

- **Average Response Time:** 8.51s
- **Median Response Time:** 7.56s
- **Min Response Time:** 6.65s
- **Max Response Time:** 12.29s
- **Response Time Std Dev:** 2.64s

## 📈 Difficulty Breakdown

- **Easy:** 0/3 (0.0%)
- **Medium:** 0/1 (0.0%)

## 📋 Answer Type Breakdown

- **instruction:** 0/1 (0.0%)
- **data_extraction:** 0/2 (0.0%)
- **technical:** 0/1 (0.0%)

## 🔧 System Status

- **llm_configured:** True
- **documents_loaded:** True
- **total_documents:** 3
- **max_context_length:** 4000
- **confidence_threshold:** 0.3

## 📝 All Grading Results

### 1. Correct: True 

**Question:** What should be done with the chisel before using the Triathlon PS Femoral Box Finishing Punch?

**Expected:** The chisel should be fully removed from the PS Box Cutting Guide prior to using the Triathlon PS Femoral Box Finishing Punch.

**Actual:** Before using the Triathlon PS Femoral Box Finishing Punch, the chisel should be fully removed from the PS Box Cutting Guide. This information is provided in the content related to the optional PS Box Preparation Finishing Punch, which specifies that the chisel should be removed prior to using the Triathlon PS Femoral Box Finishing Punch to ensure proper preparation.

**Justification:** The answer provided contains the correct information about removing the chisel before using the Triathlon PS Femoral Box Finishing Punch.

**RAG Pipeline Analysis:**
- Expected source: ✅ (rank 1)
- Content retrieved: ✅
- Tools used: get_page_content, get_row_data, get_table_data
- Iterations: 5

---

### 2. Correct: False 

**Question:** What is the maximum flexion in degrees for the Posterior Stabilized Bearing (PS)?

**Expected:** 150°

**Actual:** The maximum flexion in degrees for the Posterior Stabilized (PS) bearing is not directly provided in the available data. If there are specific details regarding the maximum flexion for the Posterior Stabilized bearing in the user notes or any additional information, please provide that so I can assist you further.

**Justification:** The actual answer does not provide the specific maximum flexion in degrees for the Posterior Stabilized Bearing (PS) as expected.

**RAG Pipeline Analysis:**
- Expected source: ✅ (rank 1)
- Content retrieved: ✅
- Tools used: get_table_data
- Iterations: 5

---

### 3. Correct: False 

**Question:** What types of materials are used in the Triathlon Tritanium Metal-Backed Patella?

**Expected:** Conventional polyethylene, Tritanium 3D porous metal

**Actual:** The types of materials used in the Triathlon Tritanium Metal-Backed Patella are as follows:
- The main component material for the Triathlon Tritanium Metal-Backed Patella is CoCrWNi alloy, which conforms to ASTM F90 standards.
- The tibial inserts for the Triathlon Tritanium Metal-Backed Patella are made of UHMWPE (Ultra-High-Molecular-Weight Polyethylene).

Therefore, the materials used in the Triathlon Tritanium Metal-Backed Patella are CoCrWNi alloy for the patella component and UHMWPE for the tibial inserts.

**Justification:** The answer provided incorrect information about the materials used in the Triathlon Tritanium Metal-Backed Patella, stating CoCrWNi alloy for the patella component and UHMWPE for the tibial inserts, which does not match the expected answer of conventional polyethylene and Tritanium 3D porous metal.

**RAG Pipeline Analysis:**
- Expected source: ✅ (rank 1)
- Content retrieved: ✅
- Tools used: get_page_content, get_table_data
- Iterations: 5

---

### 4. Correct: True 

**Question:** What are the possible reasons for the page not being processed by the extraction pipeline?

**Expected:** Processing pipeline failed on this page, Complex page layout that couldn't be parsed, Image-only content with no extractable data, PDF corruption or technical issues

**Actual:** The possible reasons for the pages not being processed by the extraction pipeline could include:

1. Processing pipeline failure on the pages.
2. Complex page layouts that couldn't be parsed.
3. Image-only content with no extractable data.
4. PDF corruption or technical issues.

These are the common reasons mentioned in the document data for pages 48, 51, 54, 59, and 60 not being processed by the extraction pipeline.

**Justification:** The answer provided contains all the possible reasons mentioned in the expected answer, albeit in a slightly different order.

**RAG Pipeline Analysis:**
- Expected source: ✅ (rank 3)
- Content retrieved: ✅
- Tools used: get_page_content, get_table_data
- Iterations: 5

---

