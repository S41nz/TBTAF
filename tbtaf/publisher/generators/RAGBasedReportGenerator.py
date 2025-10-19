from __future__ import absolute_import
from __future__ import print_function
import os
from .TBTAFReportGenerator import TBTAFReportGenerator
from common.enums.verdict_type import TBTAFVerdictType
from ai.AIFactory import AIFactory

class RAGBasedReportGenerator(TBTAFReportGenerator):
    """
    An abstract parent class that encapsulates the common RAG (Retrieval-Augmented Generation) logic
    for generating AI-enhanced test reports.

    Child classes are responsible for the final output formatting (e.g., PDF, HTML).
    This follows the Template Method design pattern.
    """

    def __init__(self):
        # Get the base path from 'TEST_CODE_BASE_PATH' environment variable.
        self.test_code_base_path = os.getenv('TEST_CODE_BASE_PATH')

        if not self.test_code_base_path:
            raise ValueError("Configuration Error: The 'TEST_CODE_BASE_PATH' environment variable is not set.")

    def _find_source_file(self, class_name: str, cache: dict) -> str or None:
        """
        Helper method to find the .py source file that contains a specific class definition.
        """
        if class_name in cache:
            return cache[class_name]

        try:
            for filename in os.listdir(self.test_code_base_path):
                if filename.endswith(".py"):
                    filepath = os.path.join(self.test_code_base_path, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            if f"class {class_name}" in f.read():
                                cache[class_name] = filepath
                                return filepath
                    except Exception:
                        continue
        except Exception as e:
            print(f"Error while searching for files in {self.test_code_base_path}: {e}")
        
        cache[class_name] = None
        return None

    def _perform_ai_analysis(self, testCasesList, summaryTestSuite, s_successRate, totalTests):
        """
        This method contains the entire RAG pipeline:
        1. Retrieval: Gathers data and source code for failed tests.
        2. Augmentation & Generation: Builds prompts and calls the AI to get analysis.
        
        Returns a tuple containing the ai_summary and the list of ai_diagnostics.
        """
        ai_interface = None
        try:
            ai_interface = AIFactory.create_ai_interface("ollama")
        except ValueError as e:
            print(f"Warning: Could not initialize AI interface: {e}")

        # Default values if AI is unavailable
        ai_summary = "AI analysis is unavailable for this execution."
        ai_diagnostics = []

        if ai_interface:
            # --- PHASE 1: RETRIEVAL ---
            failed_tests_data = []
            class_to_filepath_cache = {}
            for testCase in testCasesList:
                testResult = testCase.getResult()
                if testResult.getVerdict().strip() == TBTAFVerdictType.FAIL:
                    class_name = testResult.getResultSource()
                    source_file_path = self._find_source_file(class_name, class_to_filepath_cache)
                    
                    test_code = ""
                    if source_file_path:
                        try:
                            with open(source_file_path, 'r', encoding='utf-8') as code_file:
                                test_code = code_file.read()
                        except IOError as e:
                            test_code = f"Error reading file: {e}. Path: '{source_file_path}'"
                    else:
                        test_code = f"Error: Could not find the .py file for class '{class_name}' in '{self.test_code_base_path}'."
                    
                    failed_tests_data.append({
                        "description": testCase.getTestMetadata().getAssetDescription(),
                        "code": test_code
                    })

            # --- PHASE 2: AUGMENTED GENERATION ---
            descriptions = [tc.getTestMetadata().getAssetDescription() for tc in testCasesList]
            prompt_summary = f"""
            Act as a QA Analyst. The following is a test suite report summary:
            - Success Rate: {s_successRate}%
            - Total Tests: {totalTests}
            - Passed Tests: {summaryTestSuite.passTests}
            - Failed Tests: {summaryTestSuite.failedTests}
            - Test Descriptions: {', '.join(descriptions)}

            Generate a concise executive summary (max 60 words) about the functional coverage and overall result of this suite.
            """
            ai_summary = ai_interface.send_prompt(prompt_summary)

            if failed_tests_data:
                for failed_test in failed_tests_data:
                    prompt_diag = f"""
                    Act as a senior developer and an expert in debugging. The test named '{failed_test['description']}' has failed.
                    Based solely on its source code, provide an initial technical diagnosis of the likely cause of failure in under 50 words.
                    Test Code:
                    ```python
                    {failed_test['code']}
                    ```
                    """
                    diagnosis = ai_interface.send_prompt(prompt_diag)
                    ai_diagnostics.append(f"<b>Diagnosis for '{failed_test['description']}':</b> {diagnosis}")
        
        return ai_summary, ai_diagnostics
