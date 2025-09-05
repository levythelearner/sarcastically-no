#!/usr/bin/env python3
"""
Random Reason Picker MCP Server

An MCP server that provides tools to randomly pick reasons from a CSV file.
Uses FastMCP for easy MCP server creation.
"""

import random
import csv
import os
from pathlib import Path
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Random Reason Picker")

# Global variable to cache reasons
_reasons_cache = None
_csv_file_path = "./reasons_full.csv"

def load_reasons():
    """Load reasons from CSV file and cache them."""
    global _reasons_cache
    
    if _reasons_cache is not None:
        return _reasons_cache
    
    reasons = []
    csv_path = Path(_csv_file_path)
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {_csv_file_path}")
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        # Skip header if it exists
        first_row = next(reader, None)
        if first_row and first_row[0].lower() != "reason_id":
            reasons.append(first_row[0])
        
        # Read all reasons
        for row in reader:
            if row and row[0].strip():  # Skip empty rows
                reasons.append(row[0].strip().strip('"'))
    
    _reasons_cache = reasons
    return reasons

def _get_random_reason_internal() -> str:
    """
    Internal function to pick a random reason from the loaded CSV file.
    
    Returns:
        str: A randomly selected reason
    """
    try:
        reasons = load_reasons()
        if not reasons:
            return "No reasons available in the CSV file."
        
        return random.choice(reasons)
    except Exception as e:
        return f"Error loading reasons: {str(e)}"

@mcp.tool()
def get_random_reason() -> str:
    """
    Pick a random reason from the loaded CSV file.
    
    Returns:
        str: A randomly selected reason
    """
    return _get_random_reason_internal()

@mcp.tool()
def get_multiple_random_reasons(count: int = 3) -> list[str]:
    """
    Pick multiple random reasons from the loaded CSV file.
    
    Args:
        count: Number of reasons to pick (default: 3, max: 10)
    
    Returns:
        list[str]: A list of randomly selected reasons
    """
    try:
        # Limit count to reasonable range
        count = max(1, min(count, 10))
        
        reasons = load_reasons()
        if not reasons:
            return ["No reasons available in the CSV file."]
        
        # If we have fewer reasons than requested, return all available
        if len(reasons) < count:
            return random.sample(reasons, len(reasons))
        
        return random.sample(reasons, count)
    except Exception as e:
        return [f"Error loading reasons: {str(e)}"]

@mcp.tool()
def get_reason_stats() -> dict:
    """
    Get statistics about the reasons database.
    
    Returns:
        dict: Statistics including total count and sample reasons
    """
    try:
        reasons = load_reasons()
        
        stats = {
            "total_reasons": len(reasons),
            "csv_file": _csv_file_path,
            "sample_reasons": reasons[:3] if len(reasons) >= 3 else reasons
        }
        
        return stats
    except Exception as e:
        return {"error": f"Error loading reasons: {str(e)}"}

@mcp.tool()
def reload_reasons() -> str:
    """
    Reload reasons from the CSV file (clears cache).
    
    Returns:
        str: Status message
    """
    global _reasons_cache
    try:
        _reasons_cache = None
        reasons = load_reasons()
        return f"Successfully reloaded {len(reasons)} reasons from {_csv_file_path}"
    except Exception as e:
        return f"Error reloading reasons: {str(e)}"

if __name__ == "__main__":
    import sys
    
    # Check if we want to run as normal Python script or MCP server
    if len(sys.argv) > 1:
        # Any argument means run as normal Python script - just get a random reason and print it
        reason = _get_random_reason_internal()
        print(reason)
    else:
        # Default behavior: Run the MCP server
        mcp.run()
