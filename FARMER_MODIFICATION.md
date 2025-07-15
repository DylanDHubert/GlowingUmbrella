# Farmer Modification for max_agentic_iterations

## Overview
Modified the Farmer class to accept and pass through the `max_agentic_iterations` parameter to the underlying Barn instance.

## Changes Made

### File: `farm/src/farm/farmer.py`

**Modified the `__init__` method:**

```python
def __init__(self, 
             data_path: Optional[str] = None,
             llm_api_key: Optional[str] = None,
             llm_model: str = "gpt-3.5-turbo",
             max_agentic_iterations: int = 5):  # ADDED PARAMETER
    """
    Initialize the Farmer with data and optional LLM configuration.
    
    Args:
        data_path: Path to document data file
        llm_api_key: OpenAI API key for LLM responses
        llm_model: LLM model to use (default: gpt-3.5-turbo)
        max_agentic_iterations: Maximum iterations for agentic loop (default: 5)  # ADDED DOC
    """
    self.barn = Barn(data_path=data_path, max_agentic_iterations=max_agentic_iterations)  # PASSED THROUGH
```

## Usage Example

```python
# Default 5 iterations
farmer = Farmer()

# Custom 10 iterations
farmer = Farmer(max_agentic_iterations=10)
```

## Impact
- Allows control over how many iterations the agentic loop can run
- Default remains 5 iterations (backward compatible)
- Can be increased for complex queries that need more exploration
- Can be decreased for faster responses on simple queries

## Testing Results
With 10 iterations, the system:
- Found more tables in discovery phase (102 vs 0 for OKS questions)
- Used additional tools like `table_summary`
- Had more opportunities to find relevant content
- Still needs better search term strategies for specific data 