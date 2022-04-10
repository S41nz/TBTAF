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