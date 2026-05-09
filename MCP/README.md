## MCP Server

The TBTAF MCP Server allows AI agents to run test suites, check job status, 
and retrieve results without manual terminal interaction.

### Prerequisites

Before using the MCP Server, make sure you have the following running:

- Python 3.10+
- TBTAF REST API running on `localhost:8000` (see [Running the API](../README.md#running-the-api) section)
- Claude Desktop installed — [download here](https://claude.ai/download)

### Installation

Move into the MCP server folder and install its dependencies:

```bash
cd ./TBTAF/MCP
python3 -m venv venv
source venv/bin/activate
pip install -r mcp_requirements.txt
```

### Claude Desktop Configuration

To register the TBTAF MCP Server as a tool in Claude Desktop, edit your 
`claude_desktop_config.json` file. This file is located at:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following entry under `mcpServers`:

```json
{
  "mcpServers": {
    "TBTAF": {
      "command": "python",
      "args": ["./TBTAF/MCP/mcp_server.py"]
    }
  }
}
```

Replace `./TBTAF/MCP` with the absolute path to the 
folder where `mcp_server.py` is located on your machine.

### Usage

Once configured, restart Claude Desktop. You can then instruct the agent in 
natural language, for example:

> "Run the test suite 'discoverer' located in ./test/discoverer/samples"

The agent will invoke the MCP tools automatically, poll for the job status, 
and return a summary of results once the execution is complete.

### Available MCP Tools

| Tool | Description |
|---|---|
| `run_suite` | Launches a test suite execution given a suite name and test directory path. |
| `get_job_status` | Checks the current status and progress of a running job. |
| `get_results` | Retrieves the detailed results of a completed job. |

### Startup Order

The TBTAF REST API **must be running before** the agent invokes any MCP tool. 
The MCP Server itself can be started at any time, but its tools will return a 
connection error if FastAPI is not available at `localhost:8000`.