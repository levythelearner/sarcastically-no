# sarcastically-no
Want to comeup with an reason to say no? Here you go. Inspired by https://github.com/hotheadhacker/no-as-a-service - I modified the reason file and add an MCP server so that your LLM can choose that for you

An MCP server that provides tools to randomly pick reasons from a CSV file using FastMCP.

## Features

- **get_random_reason()**: Pick a single random reason
- **get_multiple_random_reasons(count)**: Pick multiple random reasons (1-10)
- **get_reason_stats()**: Get statistics about the reasons database
- **reload_reasons()**: Reload reasons from CSV file

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements_mcp.txt
   ```

2. **Make sure your `reasons_full.csv` file is in the same directory as the script**

3. **Run the MCP server:**
   ```bash
   python3 reason_picker_mcp.py
   ```

## Usage with MCP Clients

The server exposes the following tools:

### get_random_reason()
Returns a single random reason from the CSV file.

### get_multiple_random_reasons(count: int)
Returns multiple random reasons. The `count` parameter is optional (default: 3, max: 10).

### get_reason_stats()
Returns statistics about the loaded reasons including total count and sample reasons.

### reload_reasons()
Clears the cache and reloads reasons from the CSV file.

## CSV File Format

The server expects a CSV file named `reasons_full.csv` with reasons in the first column. The first row can be a header (will be automatically detected and skipped if it contains "reason_id").

Example CSV format:
```
reason_id
"In a different season of life, I might say yes-but not right now."
"While I appreciate it, pursuing this isn't something I can commit to."
"Every time I think about it, I hear a tiny 'nope' in the wind."
```

## Configuration

The MCP server can be configured using the provided `mcp_server_config.json` file for integration with MCP-compatible applications.

## Error Handling

The server includes comprehensive error handling for:
- Missing CSV files
- Empty CSV files
- File reading errors
- Invalid parameters

All errors are returned as descriptive messages rather than raising exceptions.
