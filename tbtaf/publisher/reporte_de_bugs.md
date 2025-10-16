# Reporte de Bugs Detectados - Proyecto TBTAF GenAI

Este documento sirve como un registro formal de los problemas técnicos (bugs) identificados y resueltos durante la configuración y desarrollo del proyecto de mejora del framework TBTAF. Cada bug está documentado en un formato similar al de un "Issue" de GitHub para facilitar su trazabilidad.

---

### **BUG #1: Falla de Conexión con Oracle en Entorno WSL**

-   **ID:** `ENV-001`
-   **Labels:** `bug`, `environment-setup`, `database`, `wsl`
-   **Status:** `CLOSED / RESOLVED`

#### **Descripción (Síntomas)**

Al intentar ejecutar el `launcher` en modo Oracle desde la terminal de Ubuntu (WSL), la aplicación se detiene inmediatamente y arroja un `Traceback` con el error `cx_Oracle.DatabaseError: DPI-1047: Cannot locate a 64-bit Oracle Client library`.

#### **Análisis de Causa Raíz (Diagnóstico)**

El error indicaba que la librería de Python `cx_Oracle` no podía encontrar las librerías del Cliente de Oracle. La investigación determinó que, aunque el Cliente estaba instalado en el sistema anfitrión (Windows), el entorno de WSL no tenía conocimiento de su ubicación. El problema se agravó al descubrir que al Cliente de Oracle le faltaba una dependencia fundamental del sistema operativo Linux, la librería `libaio.so.1`.

#### **Resolución**

La solución se implementó en dos fases a nivel del sistema operativo:

1.  **Instalación de la Dependencia:** Se instaló la librería faltante en Ubuntu. Se descubrió que el nombre del paquete había cambiado en la versión 24.04, por lo que se usó el nuevo nombre y se creó un enlace simbólico para compatibilidad:
    ```bash
    # Instalar el paquete con el nuevo nombre
    sudo apt-get install libaio1t64
    
    # Crear un enlace simbólico para que se encuentre con el nombre antiguo
    sudo ln -s /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /usr/lib/x86_64-linux-gnu/libaio.so.1
    ```
2.  **Configuración del Entorno:** Se configuró el enlazador dinámico de Linux para que el sistema siempre supiera dónde encontrar las librerías del Cliente de Oracle.

---

### **BUG #2: Falla de Conexión con el Servicio de IA (Ollama) desde WSL**

-   **ID:** `NET-001`
-   **Labels:** `bug`, `networking`, `integration`, `wsl`, `gen-ai`
-   **Status:** `CLOSED / RESOLVED`

#### **Descripción (Síntomas)**

Al ejecutar la nueva funcionalidad de análisis de reportes, el script falla con un error `Connection refused`. La consola muestra un `Traceback` de la librería `requests` indicando que no se pudo establecer una conexión con el servidor de Ollama.

#### **Análisis de Causa Raíz (Diagnóstico)**

El problema era una compleja barrera de red entre el entorno de Ubuntu (WSL) y el sistema anfitrión Windows:

* **Conflicto de `localhost`:** El script de Python, al ejecutarse en WSL, intentaba conectar a `localhost`, que dentro de WSL se refiere a sí mismo y no a Windows, donde el servicio de Ollama estaba corriendo.
* **Proxy de Red:** Incluso al usar la IP correcta de Windows, se descubrió que una política de red (proxy) en el equipo estaba interceptando y bloqueando la petición.

#### **Resolución**

La solución definitiva fue eliminar por completo la necesidad de comunicación entre WSL y Windows.

1.  **Instalación de Ollama en WSL:** Se instaló el servicio de Ollama directamente dentro del entorno de Ubuntu (WSL) usando su script de instalación para Linux.
2.  **Configuración Local:** Se configuró el `AIAnalyzer` para que apuntara a `http://localhost:11434/api/generate`.

Esto aseguró que la comunicación fuera puramente interna en WSL, bypassando cualquier firewall o proxy de Windows.

---

### **BUG #3: La Lógica RAG no Encuentra el Código Fuente de los Tests Fallidos**

-   **ID:** `LOGIC-001`
-   **Labels:** `bug`, `framework-logic`, `gen-ai`, `rag`
-   **Status:** `CLOSED / RESOLVED`

#### **Descripción (Síntomas)**

Al generar un reporte con pruebas fallidas, la sección de "Diagnóstico de Fallos" muestra un error indicando que no se pudo leer el archivo de código (`No such file or directory`), a pesar de que el archivo existía.

#### **Análisis de Causa Raíz (Diagnóstico)**

El problema se debía a dos errores lógicos en la implementación:

* **Ruta Incorrecta:** La ruta base definida para buscar los archivos de prueba (`test/smoke`) era incorrecta desde el contexto de ejecución del `launcher` (que se ejecuta desde `tbtaf/`). La ruta correcta debía ser `../test/smoke`.
* **Fuente de Datos Incorrecta:** La función `testResult.getResultSource()` devolvía el nombre de la clase de Python (ej. `TBTAFSampleTest`), no el nombre del archivo `.py` que la contenía.

#### **Resolución**

Se implementó una solución robusta en el `PDFReportGenerator`:

1.  Se corrigió la ruta base a `TEST_CODE_BASE_PATH = "../test/smoke"`.
2.  Se creó una función auxiliar (`_find_source_file`) que busca activamente en la carpeta de pruebas el archivo `.py` que contiene la definición de la clase especificada, encontrando así la ruta correcta de forma dinámica.

---

### **BUG #4: Error de Alcance de Variable (`NameError`) en la Lógica de Búsqueda**

-   **ID:** `CODE-001`
-   **Labels:** `bug`, `python`, `refactor`
-   **Status:** `CLOSED / RESOLVED`

#### **Descripción (Síntomas)**

Tras implementar la función de búsqueda de archivos, el programa fallaba con un `NameError: name 'TEST_CODE_BASE_PATH' is not defined`.

#### **Análisis de Causa Raíz (Diagnóstico)**

La variable `TEST_CODE_BASE_PATH` y la función `find_source_file` fueron definidas dentro del método `publishResultReport`. Esto las convertía en variables locales, inaccesibles desde otras partes del código o en el contexto en que se llamaban.

#### **Resolución**

Se refactorizó el código del `PDFReportGenerator` siguiendo las mejores prácticas de la programación orientada a objetos:

* La variable `TEST_CODE_BASE_PATH` se movió fuera del método para convertirla en un **atributo de la clase**.
* La función `find_source_file` se convirtió en un **método de la clase** (añadiendo `self` como primer parámetro).
* Todas las referencias a estos elementos se actualizaron para ser accedidas a través de `self` (ej. `self.TEST_CODE_BASE_PATH`, `self._find_source_file(...)`), solucionando el error de alcance.
---

### BUG #5: Falla al Abrir Archivo de Wallet de Oracle

* **ID:** DB-001
* **Labels:** `bug`, `database`, `configuration`, `oracle-wallet`
* **Status:** CLOSED / RESOLVED
* **Descripción (Síntomas)**
    Al ejecutar una prueba que requiere conexión a la base de datos, la aplicación falla y arroja el error `cx_Oracle.DatabaseError: ORA-28759: failure to open file`.
* **Análisis de Causa Raíz (Diagnóstico)**
    El error indica que el cliente de Oracle no puede abrir el archivo del Wallet. La investigación reveló que la ruta especificada en el archivo de configuración `sqlnet.ora` dentro de la carpeta del Wallet era un placeholder genérico (`/path/to/your/wallet`) y no apuntaba a una ubicación real en el sistema de archivos.
* **Resolución**
    Se modificó el archivo `sqlnet.ora` para que utilizara la variable de entorno `$TNS_ADMIN` como la ruta del directorio del Wallet. Esta solución es dinámica y asegura que la ubicación siempre sea la correcta, sin importar dónde esté almacenado el proyecto en el sistema.

    **Configuración Incorrecta:**
    ```
    # La ruta era un placeholder genérico.
    WALLET_LOCATION = (SOURCE = (METHOD = file) (METHOD_DATA = (DIRECTORY="/path/to/your/wallet")))
    ```
    **Configuración Corregida:**
    ```
    # Se utilizó la variable de entorno $TNS_ADMIN para asegurar que la ruta siempre fuera correcta.
    WALLET_LOCATION = (SOURCE = (METHOD = file) (METHOD_DATA = (DIRECTORY="$TNS_ADMIN")))
    ```

---

### BUG #6: Permisos de Escritura Insuficientes en el Sistema de Archivos

* **ID:** FS-001
* **Labels:** `bug`, `permissions`, `file-system`, `wsl`
* **Status:** CLOSED / RESOLVED
* **Descripción (Síntomas)**
    Al intentar crear un nuevo archivo de código (`ai_analyzer.py`) usando el editor de texto `nano` en la terminal de Ubuntu, el editor muestra el error `[ Error writing lock file ... Permission denied ]` y no permite guardar el archivo.
* **Análisis de Causa Raíz (Diagnóstico)**
    El error es arrojado por el sistema operativo. Indica que el usuario actual (`alexa`) no tiene los permisos necesarios para crear o modificar archivos dentro de la carpeta de destino (`~/TBTAF/tbtaf/publisher/`). Esto suele ocurrir cuando las carpetas se crean o descomprimen con un usuario diferente o con permisos elevados.
* **Resolución**
    Se utilizó el comando `chown` (change owner) con privilegios de superusuario (`sudo`) para cambiar el propietario de la carpeta `publisher` y todo su contenido al usuario actual. Esta acción otorgó los permisos de escritura necesarios de forma permanente.

    **Acción Fallida:**
    ```bash
    # Simplemente intentar guardar en nano fallaba.
    nano ~/TBTAF/tbtaf/publisher/ai_analyzer.py
    ```
    **Comando de Corrección:**
    ```bash
    # Se ejecutó este comando una sola vez para tomar posesión de la carpeta y resolver el problema.
    sudo chown -R alexa:alexa ~/TBTAF/tbtaf/publisher
    ```

---

### BUG #7: Falla en la Resolución de Módulos de Python

* **ID:** CODE-001
* **Labels:** `bug`, `python`, `import-error`, `code-structure`
* **Status:** CLOSED / RESOLVED
* **Descripción (Síntomas)**
    Al ejecutar el launcher, el programa se detiene con el error `ModuleNotFoundError: No module named 'publisher.ai_analyzer'`.
* **Análisis de Causa Raíz (Diagnóstico)**
    El `Traceback` indica que el error ocurre cuando el archivo `PDFReportGenerator.py` intenta importar el nuevo módulo `ai_analyzer.py`. La ruta de importación utilizada (`from publisher.ai_analyzer...`) es relativa. Debido a cómo se ejecuta el launcher desde la carpeta raíz del proyecto, el intérprete de Python no puede resolver esta ruta ambigua.
* **Resolución**
    Se corrigió la declaración de importación en el archivo `PDFReportGenerator.py` para que fuera una ruta absoluta desde la raíz del paquete de software (`tbtaf`). Esto le proporciona al intérprete de Python una "dirección" explícita y sin ambigüedades para encontrar el módulo.

    **Código Incorrecto:**
    ```python
    # Esta ruta relativa confundía a Python.
    from publisher.ai_analyzer import get_ai_analysis
    ```
    **Código Corregido:**
    ```python
    # Se proporcionó la ruta completa desde la raíz del paquete (`tbtaf`), eliminando la ambigüedad.
    from tbtaf.publisher.ai_analyzer import get_ai_analysis
    ```
    
