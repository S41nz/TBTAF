'''
Created on 04/11/2022

@author: @brody7u7
'''
from __future__ import absolute_import
from __future__ import print_function
import datetime
import os
from xhtml2pdf import pisa
from common.exception.IllegalArgumentException import IllegalArgumentException
from common.exception.NonSupportedFormatException import NonSupportedFormatException
from .TBTAFReportGenerator import TBTAFReportGenerator
from common.enums.verdict_type import TBTAFVerdictType

from ai.AIFactory import AIFactory

class PDFReportGenerator(TBTAFReportGenerator):
    '''
    PDFReportGenerator generates test 
    execution reports in PDF format.
    '''
    # Define the base path as a class attribute
    TEST_CODE_BASE_PATH = "../test/smoke"

    def _find_source_file(self, class_name, cache):
        """
        Helper method to find the .py file that contains a class definition.
        It uses 'self' to access class attributes like TEST_CODE_BASE_PATH.
        """
        if class_name in cache:
            return cache[class_name]
        try:
            for filename in os.listdir(self.TEST_CODE_BASE_PATH):
                if filename.endswith(".py"):
                    filepath = os.path.join(self.TEST_CODE_BASE_PATH, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            if f"class {class_name}" in f.read():
                                cache[class_name] = filepath
                                return filepath
                    except Exception:
                        # Ignore files that cannot be read
                        continue
        except Exception as e:
            print(f"Error while searching for files in {self.TEST_CODE_BASE_PATH}: {e}")
        
        cache[class_name] = None
        return None

    def publishTestPlan(self, tBTestSuiteInstance, filePath):
        '''
        Builds a test plan specification on a PDF format
        based on the discovered metadata
        '''
        
        if not filePath.lower().endswith(".pdf"):
            print("The file path doesn't contain a valid pdf file")
            raise NonSupportedFormatException("NonSupportedFormatException in PublishTestPlan")

        try:
            htmlFile = open(filePath, 'w+b')
        except IOError:
            print("Invalid file path")
            raise IllegalArgumentException("IllegalArgumentException in filePath argument in PublishTestPlan")
              
        #Read HTML Template file and put into a string
        htmlTemplate = open('publisher/test_plan_template.html','r')
        htmlString = htmlTemplate.read()
        htmlTemplate.close()
        #Initialize tests HTML string
        s_tests = ""
        
        #Iterate over test cases and retrieve test metadata
        testCasesList = tBTestSuiteInstance.getTestCases();
        
        #Define to sort the test cases by priority or by asset id
        sortPriority = True
        for testCase in testCasesList:
            if not str(testCase.getTestMetadata().getPriority()).isdigit():
                sortPriority = False
                break
        
        if sortPriority:
            #Sort by priority
            testCasesList.sort(key=lambda x:x.getTestMetadata().getPriority(), reverse=False)
        else:
            #Sort by asset id
            testCasesList.sort(key=lambda x:x.getTestMetadata().getAssetID(), reverse=False)
        
        for testCase in testCasesList:
            #Initialize table row tag 
            s_tests = s_tests  + "<tr>"
            testMetaData = testCase.getTestMetadata()
            #Add test ID to HTML
            s_tests = s_tests + "<td>" + str(testMetaData.getAssetID()) + "</td>"
            #Add test description to HTML
            s_tests = s_tests + "<td>" + testMetaData.getAssetDescription() + "</td>"
            #Add test tags to HTML
            testTags = testMetaData.getTags()
            s_tests = s_tests + "<td>"
            for tag in testTags:
                s_tests = s_tests + tag + ", "
            #Remove last character from tags
            s_tests = s_tests[:-2]
            #Add close table data tag to HTML
            s_tests = s_tests + "</td>"
            #Add priority to HTML
            s_tests = s_tests + "<td>" + str(testMetaData.getPriority()) + "</td>"
            #Add close table row tag to HTML
            s_tests = s_tests + "</tr>"
        
        #Calculate report time
        reportTime = datetime.datetime.now()
        s_reportTime = reportTime.strftime('%B %d,%Y %H:%M:%S')
        #Replace strings in HTML file
        htmlString = htmlString.replace('r_suite',str(tBTestSuiteInstance.getSuiteID()))
        htmlString = htmlString.replace('r_report_time',s_reportTime)
        htmlString = htmlString.replace('r_tests',s_tests)
        
        headTagIndex = htmlString.index("</head>")
        htmlString = htmlString[:headTagIndex] + "<style> @page {size: a4 landscape;margin: 2cm;} .table th {text-align: left;} </style>" + htmlString[headTagIndex:]
        pisa.CreatePDF(htmlString, dest=htmlFile)
        htmlFile.close()


    def publishResultReport(self, tBTestSuiteInstance, filePath):
        '''
        Builds a test execution report and enriches it with AI analysis.
        '''
        if not filePath.lower().endswith(".pdf"):
            raise NonSupportedFormatException("File must be .pdf")

        try:
            htmlFile = open(filePath, 'w+b')
        except IOError:
            raise IllegalArgumentException("Invalid file path")
        
         #Read HTML Template file and put into a string
        htmlTemplate = open('publisher/results_template.html','r')
        htmlString = htmlTemplate.read()
        htmlTemplate.close()
        #Get summary result from the test suite instance
        summaryTestSuite = tBTestSuiteInstance.getSuiteResult()
        #Calculate total number of test cases
        totalTests = len(tBTestSuiteInstance.suiteTestCases)
        #Calculate success rate of test summary results 
        successRate = (float(summaryTestSuite.passTests) / float(totalTests))*100
        s_successRate = format("%.2f" % successRate)
        #Get start & end datetime and format them for display 
        startTime = summaryTestSuite.getStartTimestamp()
        endTime = summaryTestSuite.getEndTimestamp()
        s_startTime = startTime.strftime('%B %d,%Y %H:%M:%S')
        s_endTime = endTime.strftime('%B %d,%Y %H:%M:%S')
        #Calculate elapsed time and format it for display
        elapsedTime = endTime - startTime
        s_elapsedTime = str(elapsedTime)
        #Get individual test cases
        testCasesList = tBTestSuiteInstance.getTestCases();
        #Initialize overview HTML string
        s_overview = ""
        
        #Define to sort the test cases by priority or by asset id
        sortPriority = True
        for testCase in testCasesList:
            if not str(testCase.getTestMetadata().getPriority()).isdigit():
                sortPriority = False
                break
        
        if sortPriority:
            #Sort by priority
            testCasesList.sort(key=lambda x:x.getTestMetadata().getPriority(), reverse=False)
        else:
            #Sort by asset id
            testCasesList.sort(key=lambda x:x.getTestMetadata().getAssetID(), reverse=False)

        #Iterate over test cases and retrieve test metadata
        for testCase in testCasesList:
            #Initialize table row tag 
            s_overview = s_overview  + "<tr>"
            testMetaData = testCase.getTestMetadata()
            #Add test ID to HTML
            s_overview = s_overview + "<td>" + str(testMetaData.getAssetID()) + "</td>"
            #Add test description to HTML
            s_overview = s_overview + "<td>" + testMetaData.getAssetDescription() + "</td>"
            #Add test tags to HTML
            testTags = testMetaData.getTags()
            s_overview = s_overview + "<td>"
            for tag in testTags:
                s_overview = s_overview + tag + ", "
            #Remove last character from tags
            s_overview = s_overview[:-2]
            #Add close table data tag to HTML
            s_overview = s_overview + "</td>"
            #Add priority to HTML
            s_overview = s_overview + "<td>" + str(testMetaData.getPriority()) + "</td>"
            #Retrieve test case result
            testResult = testCase.getResult()
            #Add result source to HTML
            s_overview = s_overview + "<td>" + testResult.getResultSource() + "</td>"
            #Get start & end datetime from result and format them for display 
            resultStartTime = testResult.getStartTimestamp()
            resultEndTime = testResult.getEndTimestamp()
            s_resultStartTime = resultStartTime.strftime('%B %d,%Y %H:%M:%S')
            s_resultEndTime = resultEndTime.strftime('%B %d,%Y %H:%M:%S')
            #Add start time to HTML
            s_overview = s_overview + "<td>" + s_resultStartTime + "</td>"
            #Add end time to HTML
            s_overview = s_overview + "<td>" + s_resultEndTime + "</td>"
            #Calculate elapsed time and add it to HTML
            resultElapsedTime = resultEndTime - resultStartTime
            s_overview = s_overview + "<td>" + str(resultElapsedTime) + "</td>"
            #Add verdict to HTML
            s_overview = s_overview + "<td>" + str(testResult.getVerdict()) + "</td>"
            #Add close table row tag to HTML
            s_overview = s_overview + "</tr>"

        #Calculate report time
        reportTime = datetime.datetime.now()
        s_reportTime = reportTime.strftime('%B %d,%Y %H:%M:%S')
                    
        # ========== START: INTEGRATION WITH THE AI FACTORY ==========       
        
        ai_interface = None
        try:
            # CHANGE: Use the factory to get the AI interface.
            # This generator no longer knows that "Ollama" exists.
            ai_interface = AIFactory.create_ai_interface("ollama")
        except ValueError as e:
            print(f"Warning: Could not initialize AI interface: {e}")

        # --- PHASE 1: RETRIEVAL ---
        failed_tests_data = []
        class_to_filepath_cache = {} # Cache per report execution for efficiency
        for testCase in testCasesList:
            testResult = testCase.getResult()
            if testResult.getVerdict().strip() == TBTAFVerdictType.FAIL:
                class_name = testResult.getResultSource()
                # Call the helper method using 'self'
                source_file_path = self._find_source_file(class_name, class_to_filepath_cache)
                
                test_code = ""
                if source_file_path:
                    try:
                        with open(source_file_path, 'r', encoding='utf-8') as code_file:
                            test_code = code_file.read()
                    except IOError as e:
                        test_code = f"Error reading file: {e}. Path: '{source_file_path}'"
                else:
                    test_code = f"Error: Could not find the .py file for class '{class_name}' in '{self.TEST_CODE_BASE_PATH}'."
                
                failed_tests_data.append({
                    "description": testCase.getTestMetadata().getAssetDescription(),
                    "code": test_code
                })

        # --- PHASE 2: AUGMENTED GENERATION ---
        ai_summary = "AI analysis was not available for this execution."
        ai_diagnostics = []

        # Only proceed if the AI interface was successfully initialized
        if ai_interface:
            # 2.1 - Generate Executive Summary
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
            # CHANGE: Use the standardized interface method
            ai_summary = ai_interface.send_prompt(prompt_summary)

            # 2.2 - Generate Diagnostics for each failed test
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
                    # CHANGE: Use the standardized interface method
                    diagnosis = ai_interface.send_prompt(prompt_diag)
                    ai_diagnostics.append(f"<b>Diagnosis for '{failed_test['description']}':</b> {diagnosis}")                

        htmlString = htmlString.replace('r_suite', str(tBTestSuiteInstance.getSuiteID()))
        htmlString = htmlString.replace('r_total_tests', str(totalTests))
        htmlString = htmlString.replace('r_passed', str(summaryTestSuite.passTests))
        htmlString = htmlString.replace('r_failed', str(summaryTestSuite.failedTests))
        htmlString = htmlString.replace('r_inconclusive', str(summaryTestSuite.inconclusiveTests))
        htmlString = htmlString.replace('r_success_rate', s_successRate + '%')
        htmlString = htmlString.replace('r_start_time', s_startTime)
        htmlString = htmlString.replace('r_end_time', s_endTime)
        htmlString = htmlString.replace('r_elapsed_time', s_elapsedTime)
        htmlString = htmlString.replace('r_overview', s_overview)
        htmlString = htmlString.replace('r_report_time', s_reportTime)

        # Replace AI placeholders
        htmlString = htmlString.replace('r_ai_summary', ai_summary)
        if ai_diagnostics:
            formatted_diagnostics = "".join([f"<p>{d}</p>" for d in ai_diagnostics])
            htmlString = htmlString.replace('r_ai_diagnostics', formatted_diagnostics)
        else:
            htmlString = htmlString.replace('r_ai_diagnostics', "<p>No failed tests were found to analyze.</p>")

        headTagIndex = htmlString.index("</head>")
        htmlString = htmlString[:headTagIndex] + "<style> @page {size: a4 landscape;margin: 2cm;} .table th {text-align: left;} </style>" + htmlString[headTagIndex:]
        pisa.CreatePDF(htmlString, dest=htmlFile)
        htmlFile.close()

