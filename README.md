# TBTAF
Repository for the source code of the Tag-Based Test Automation Framework

## First steps:
Move into the project folder:
> cd tbtaf/

Create a Python virtual environment:
> python3 -m venv <envrionment_name>

Load the created Python virtual environment
> source <environment_name>/bin/activate

Install the required Python modules
> pip install -r requirements.txt

Update the `tbtaf_launcher.py`script to point to any of the sample `tbtaf` scripts contained on `./test/*.tbtaf`

Run launcher:
> python tbtaf_launcher.py

## Fastapi 

After running 
> pip install -r requirements.txt

Run the development server
> fastapi dev main.py

Go to the url indicated by the log console, use the url with the /docs endpoint.

e.g. http://127.0.0.1:8000/docs

This will take you to the documentation page for the api with interactive endpoints.

## OracleDB configuration
Install `Oracle Instant Client` from this [URL](https://www.oracle.com/technetwork/database/database-technologies/instant-client/downloads/index.html)

Download oracle wallet and sae into your python virtual environment

Unzip the wallet

Edit the `sqlnet.ora` file to reflect the location where it's located, edit the `DIRECTORY` atribute

Export the required connection environt variales:
```
export TNS_ADMIN=<Absolute extracted wallet path>
export ODB_USER=<DB username>
export ODB_PASS=<DB password>
export ODB_TNS=<connection URL name, eg: xxxxx_medium>
```

You are ready to connect!

## GenAI Feature Configuration (Ollama)

This project uses a local Large Language Model (LLM) via Ollama to generate intelligent analysis in the test reports. Follow these steps to enable this feature.

1.  *Install Ollama:* Download and install Ollama for your operating system (Windows, macOS, or Linux) from the official website: [ollama.com](https://ollama.com). After installation, ensure the Ollama service is running.

2.  *Pull the AI Model:* Once Ollama is running, open your terminal and pull the required model. This project is configured to use llama3.
    bash
    ollama pull llama3
    

3.  *Export Environment Variables:* Before running the tbtaf_launcher.py, you must set the following environment variables. These tell the framework how to connect to the Ollama service.
    bash
    export OLLAMA_API_URL="http://localhost:11434/api/generate"
    export OLLAMA_MODEL="llama3"
    export TEST_CODE_BASE_PATH="../test/smoke"

After completing these steps, when you run the launcher, the GenAI features will be enabled and will enrich the PDF/HTML reports with an executive summary and failure diagnosis.

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