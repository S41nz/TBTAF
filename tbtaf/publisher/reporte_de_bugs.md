# Bug Report Log - TBTAF GenAI Project

This document serves as a formal record of the technical issues (bugs) identified and resolved during the setup and development of the TBTAF framework enhancement project. Each bug is documented in a format similar to a GitHub Issue to facilitate traceability.

---

### *BUG #1: Oracle Connection Failure in WSL Environment*

-   *ID:* ENV-001
-   *Labels:* bug, environment-setup, database, wsl
-   *Status:* CLOSED / RESOLVED

#### *Description (Symptoms)*

When attempting to run the launcher in Oracle mode from the Ubuntu terminal (WSL), the application immediately stops and throws a Traceback with the error cx_Oracle.DatabaseError: DPI-1047: Cannot locate a 64-bit Oracle Client library.

#### *Root Cause Analysis (Diagnosis)*

The error indicated that the cx_Oracle Python library could not find the Oracle Client libraries. The investigation determined that, although the Client was installed on the host system (Windows), the WSL environment was unaware of its location. The problem was compounded by the discovery that the Oracle Client was missing a fundamental Linux OS dependency, the libaio.so.1 library.

#### *Resolution*

The solution was implemented in two phases at the operating system level:

1.  *Dependency Installation:* The missing library was installed in Ubuntu. It was discovered that the package name had changed in version 24.04, so the new name was used, and a symbolic link was created for compatibility:
    bash
    # Install the package with the new name
    sudo apt-get install libaio1t64
    
    # Create a symbolic link to be found under the old name
    sudo ln -s /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /usr/lib/x86_64-linux-gnu/libaio.so.1
    
2.  *Environment Configuration:* The Linux dynamic linker was configured so the system would always know where to find the Oracle Client libraries.

---

### *BUG #2: RAG Logic Fails to Find Source Code of Failed Tests*

-   *ID:* LOGIC-001
-   *Labels:* bug, framework-logic, gen-ai, rag
-   *Status:* CLOSED / RESOLVED

#### *Description (Symptoms)*

When generating a report with failed tests, the "Failure Diagnosis" section shows an error indicating that the code file could not be read (No such file or directory), even though the file existed.

#### *Root Cause Analysis (Diagnosis)*

The issue was caused by two logical errors in the implementation:

* *Incorrect Path:* The base path defined to search for test files (test/smoke) was incorrect from the launcher's execution context (which runs from tbtaf/). The correct path needed to be ../test/smoke.
* *Incorrect Data Source:* The testResult.getResultSource() function returned the Python class name (e.g., TBTAFSampleTest), not the name of the .py file that contained it.

#### *Resolution*

A robust solution was implemented in the PDFReportGenerator:

1.  The base path was corrected to TEST_CODE_BASE_PATH = "../test/smoke".
2.  A helper function (_find_source_file) was created to actively search the test folder for the .py file containing the specified class definition, thus dynamically finding the correct path.

---

### **BUG #3: Variable Scope Error (NameError) in Search Logic**

-   *ID:* CODE-001
-   *Labels:* bug, python, refactor
-   *Status:* CLOSED / RESOLVED

#### *Description (Symptoms)*

After implementing the file search function, the program failed with a NameError: name 'TEST_CODE_BASE_PATH' is not defined.

#### *Root Cause Analysis (Diagnosis)*

The TEST_CODE_BASE_PATH variable and the find_source_file function were defined inside the publishResultReport method. This made them local variables, inaccessible from other parts of the code or in the context they were being called.

#### *Resolution*

The PDFReportGenerator code was refactored following object-oriented programming best practices:

* The TEST_CODE_BASE_PATH variable was moved outside the method to become a *class attribute*.
* The find_source_file function was converted into a *class method* (by adding self as the first parameter).
* All references to these elements were updated to be accessed via self (e.g., self.TEST_CODE_BASE_PATH, self._find_source_file(...)), fixing the scope error.
---

### BUG #4: Failure to Open Oracle Wallet File

* *ID:* DB-001
* *Labels:* bug, database, configuration, oracle-wallet
* *Status:* CLOSED / RESOLVED
* *Description (Symptoms)*
    When running a test that requires a database connection, the application fails and throws the error cx_Oracle.DatabaseError: ORA-28759: failure to open file.
* *Root Cause Analysis (Diagnosis)*
    The error indicates that the Oracle client cannot open the Wallet file. The investigation revealed that the path specified in the sqlnet.ora configuration file within the Wallet folder was a generic placeholder (/path/to/your/wallet) and did not point to a real location on the filesystem.
* *Resolution*
    The sqlnet.ora file was modified to use the $TNS_ADMIN environment variable as the path to the Wallet directory. This solution is dynamic and ensures the location is always correct, regardless of where the project is stored on the system.

    *Incorrect Configuration:*
    
    # The path was a generic placeholder.
    WALLET_LOCATION = (SOURCE = (METHOD = file) (METHOD_DATA = (DIRECTORY="/path/to/your/wallet")))
    
    *Corrected Configuration:*
    
    # The $TNS_ADMIN environment variable was used to ensure the path is always correct.
    WALLET_LOCATION = (SOURCE = (METHOD = file) (METHOD_DATA = (DIRECTORY="$TNS_ADMIN")))
    

---

### BUG #5: Insufficient Filesystem Write Permissions

* *ID:* FS-001
* *Labels:* bug, permissions, file-system, wsl
* *Status:* CLOSED / RESOLVED
* *Description (Symptoms)*
    When trying to create a new code file (ai_analyzer.py) using the nano text editor in the Ubuntu terminal, the editor displays the error [ Error writing lock file ... Permission denied ] and does not allow saving the file.
* *Root Cause Analysis (Diagnosis)*
    The error is thrown by the operating system. It indicates that the current user (alexa) does not have the necessary permissions to create or modify files within the target folder (~/TBTAF/tbtaf/publisher/). This often occurs when folders are created or unzipped with a different user or with elevated privileges.
* *Resolution*
    The chown (change owner) command was used with superuser privileges (sudo) to change the owner of the publisher folder and all its contents to the current user. This action granted the necessary write permissions permanently.

    *Failed Action:*
    bash
    # Simply trying to save in nano failed.
    nano ~/TBTAF/tbtaf/publisher/ai_analyzer.py
    
    *Corrective Command:*
    bash
    # This command was run once to take ownership of the folder and resolve the issue.
    sudo chown -R alexa:alexa ~/TBTAF/tbtaf/publisher
    

---

### BUG #6: Python Module Resolution Failure

* *ID:* CODE-001
* *Labels:* bug, python, import-error, code-structure
* *Status:* CLOSED / RESOLVED
* *Description (Symptoms)*
    When running the launcher, the program stops with the error ModuleNotFoundError: No module named 'publisher.ai_analyzer'.
* *Root Cause Analysis (Diagnosis)*
    The Traceback indicates that the error occurs when the PDFReportGenerator.py file attempts to import the new ai_analyzer.py module. The import path used (from publisher.ai_analyzer...) is relative. Due to how the launcher is executed from the project's root folder, the Python interpreter cannot resolve this ambiguous path.
* *Resolution*
    The import statement in the PDFReportGenerator.py file was corrected to be an absolute path from the software package's root (tbtaf). This provides the Python interpreter with an explicit and unambiguous "address" to find the module.

    *Incorrect Code:*
    python
    # This relative path confused Python.
    from publisher.ai_analyzer import get_ai_analysis
    
    *Corrected Code:*
    python
    # The full path from the package root (`tbtaf`) was provided, removing the ambiguity.
    from tbtaf.publisher.ai_analyzer import get_ai_analysis
    