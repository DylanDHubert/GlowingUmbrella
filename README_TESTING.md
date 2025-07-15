# 🌾 Farm System Testing Framework

This directory contains a comprehensive testing framework for the Farm RAG system using knee documents and pre-generated test questions.

## 📁 Files Overview

- `test_farm_knee_system.py` - **Main testing framework** with comprehensive test suite
- `test_simple_farm.py` - **Simple verification script** to test basic functionality
- `README_TESTING.md` - This documentation file

## 🚀 Quick Start

### 1. Basic System Test
First, verify the farm system is working:

```bash
python test_simple_farm.py
```

This will test:
- ✅ Farm module import
- ✅ Farmer creation
- ✅ Document loading
- ✅ Simple query execution

### 2. Full Test Suite
Run the comprehensive test suite:

```bash
# Run all tests
python test_farm_knee_system.py

# Run with debug mode
python test_farm_knee_system.py --debug

# Run limited tests (e.g., first 50)
python test_farm_knee_system.py --max-tests 50

# Run without saving results
python test_farm_knee_system.py --no-save
```

## 📊 Test Framework Features

### 🔍 **Comprehensive Testing**
- **Multiple Documents**: Loads all 4 knee documents simultaneously
- **Pre-generated Questions**: Uses 8000+ test questions with expected answers
- **Automated Grading**: Compares actual vs expected answers
- **Performance Metrics**: Response times, success rates, detailed statistics

### 📈 **Detailed Analytics**
- **Success Rate**: Overall and by difficulty level
- **Response Times**: Average, median, min/max, standard deviation
- **Difficulty Breakdown**: Performance by easy/medium/hard questions
- **Answer Type Analysis**: Performance by question type (data_extraction, analysis, etc.)
- **System Status**: Document loading, memory usage, etc.

### 🐛 **Debug Mode**
- **Detailed Output**: Shows LLM reasoning, tool calls, context used
- **Error Tracking**: Captures and reports specific failures
- **Performance Profiling**: Detailed timing breakdown

### 💾 **Results Storage**
- **JSON Export**: Complete results saved with timestamp
- **Structured Data**: All metrics, responses, and metadata preserved
- **Reproducible**: Can be loaded and analyzed later

## 📋 Test Questions Structure

The test questions are loaded from `data/questions/knee_test_questions_20250712_160235.json` and include:

```json
{
  "question": "What are the common expressions used by patients to describe instability?",
  "expected_answer_type": "data_extraction",
  "difficulty": "easy",
  "target_content": "\"Giving way\" or \"Just will not hold them up\"",
  "page_id": "page_7",
  "page_title": "Some Common Symptoms of Instability",
  "doc_file": "jsons/knee_original_20250701_171754.json"
}
```

### Question Types:
- **data_extraction**: Extract specific facts
- **comparison**: Compare concepts or features
- **analysis**: Analyze relationships or implications
- **concept**: Understand abstract concepts
- **instruction**: Follow procedural instructions
- **clinical**: Clinical implications and applications
- **technical**: Technical specifications and details

### Difficulty Levels:
- **easy**: Simple fact extraction
- **medium**: Analysis and comparison
- **hard**: Complex reasoning and synthesis

## 📊 Sample Output

```
🌾 INITIALIZING FARM KNEE TESTER
📁 Knee documents: 4
❓ Questions file: data/questions/knee_test_questions_20250712_160235.json
🐛 Debug mode: False
💾 Save results: True

📖 LOADING TEST QUESTIONS...
✅ Loaded 8000+ test questions

🚜 INITIALIZING FARMER...
📚 LOADING KNEE DOCUMENTS...
  📄 Loading knee_original_20250701_144728...
    ✅ Successfully loaded knee_original_20250701_144728
  📄 Loading knee_original_20250701_171754...
    ✅ Successfully loaded knee_original_20250701_171754
  📄 Loading knee_original_20250702_233749...
    ✅ Successfully loaded knee_original_20250702_233749
  📄 Loading ts_knee_original_20250701_175753...
    ✅ Successfully loaded ts_knee_original_20250701_175753

📊 System Status: ready
📄 Loaded documents: 4

🧪 RUNNING ALL TESTS...
📝 Running 100 tests...
  🔍 Test 1/100: At what degrees of flexion is the knee stable...
  🔍 Test 2/100: How does the stability of the knee change...
  ...

================================================================================
📊 TEST RESULTS SUMMARY
================================================================================
📝 Total Questions: 100
✅ Successful Answers: 85
❌ Failed Answers: 15
📈 Success Rate: 85.0%

⏱️  TIMING STATISTICS:
   Average Response Time: 2.34s
   Median Response Time: 2.12s
   Min Response Time: 1.45s
   Max Response Time: 4.67s
   Response Time Std Dev: 0.89s

🔧 SYSTEM STATUS:
   status: ready
   loaded_documents: 4
   total_notes: 0

📊 DIFFICULTY BREAKDOWN:
   Easy: 45/50 (90.0%)
   Medium: 32/38 (84.2%)
   Hard: 8/12 (66.7%)

📋 ANSWER TYPE BREAKDOWN:
   data_extraction: 65/75 (86.7%)
   analysis: 12/15 (80.0%)
   comparison: 8/10 (80.0%)
```

## 🔧 Configuration Options

### Command Line Arguments:
- `--debug`: Enable detailed debug output
- `--max-tests N`: Limit to first N tests
- `--no-save`: Don't save results to file
- `--save-results`: Save results (default: True)

### Environment Variables:
- `OPENAI_API_KEY`: Required for LLM functionality
- `OPENAI_MODEL`: Model to use (default: gpt-3.5-turbo)

## 📁 Data Requirements

### Required Files:
```
data/
├── jsons/
│   ├── knee_original_20250701_144728.json
│   ├── knee_original_20250701_171754.json
│   ├── knee_original_20250702_233749.json
│   └── ts_knee_original_20250701_175753.json
└── questions/
    └── knee_test_questions_20250712_160235.json
```

### Farm System:
```
farm/
└── src/
    └── farm/
        ├── farmer.py
        ├── barn.py
        ├── silo.py
        └── ...
```

## 🎯 Testing Strategy

### 1. **Validation Testing**
- Verify system loads all documents correctly
- Test basic query functionality
- Check response quality and accuracy

### 2. **Performance Testing**
- Measure response times across different question types
- Identify bottlenecks in processing
- Monitor memory usage and system stability

### 3. **Accuracy Testing**
- Compare actual vs expected answers
- Analyze success rates by difficulty and question type
- Identify areas for improvement

### 4. **Debug Testing**
- Use debug mode to understand system behavior
- Analyze tool usage and context selection
- Optimize prompt engineering and strategies

## 📈 Results Analysis

### Success Metrics:
- **Overall Success Rate**: Percentage of correct answers
- **Difficulty Performance**: Success rate by difficulty level
- **Question Type Performance**: Success rate by question type
- **Response Time Analysis**: Performance and consistency

### Improvement Areas:
- **Low Success Questions**: Identify patterns in failed questions
- **Slow Response Times**: Optimize processing bottlenecks
- **Context Selection**: Improve relevance of retrieved content
- **Answer Quality**: Enhance response accuracy and completeness

## 🚨 Troubleshooting

### Common Issues:

1. **Import Errors**:
   ```bash
   # Check farm installation
   python test_simple_farm.py
   ```

2. **Document Loading Failures**:
   ```bash
   # Verify file paths
   ls data/jsons/
   ```

3. **LLM API Errors**:
   ```bash
   # Check API key
   echo $OPENAI_API_KEY
   ```

4. **Memory Issues**:
   ```bash
   # Run with fewer tests
   python test_farm_knee_system.py --max-tests 10
   ```

## 🔄 Continuous Testing

### Automated Testing:
```bash
# Run tests periodically
crontab -e
# Add: 0 */6 * * * cd /path/to/farm && python test_farm_knee_system.py --max-tests 100
```

### Results Tracking:
- Save results with timestamps
- Track performance over time
- Identify regression issues

## 📚 Advanced Usage

### Custom Test Sets:
```python
# Modify test_farm_knee_system.py to use custom questions
custom_questions = [
    {
        "question": "Your custom question?",
        "target_content": "Expected answer",
        "difficulty": "medium",
        "expected_answer_type": "analysis"
    }
]
```

### Integration Testing:
```python
# Test with different document combinations
doc_combinations = [
    ["knee_original_20250701_144728.json"],
    ["knee_original_20250701_144728.json", "knee_original_20250701_171754.json"],
    # ... all combinations
]
```

---

**Ready to test?** Start with `python test_simple_farm.py` to verify your setup! 🚀 