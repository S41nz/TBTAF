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
    

After completing these steps, when you run the launcher, the GenAI features will be enabled and will enrich the PDF/HTML reports with an executive summary and failure diagnosis.