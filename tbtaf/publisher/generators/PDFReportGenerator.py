'''
Created on 04/11/2022

@author: @brody7u7
'''
from __future__ import absolute_import
from __future__ import print_function
import datetime
from xhtml2pdf import pisa
from common.exception.IllegalArgumentException import IllegalArgumentException
from common.exception.NonSupportedFormatException import NonSupportedFormatException
from .TBTAFReportGenerator import TBTAFReportGenerator
class PDFReportGenerator(TBTAFReportGenerator):
    '''
    PDFReportGenerator generates all the test 
    execution on PDF format.
    '''

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
        Builds a test execution report on a PDF format
        based on the execution result of a given test suite
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

        #Replace the html string with summary results
        htmlString = htmlString.replace('r_suite',str(tBTestSuiteInstance.getSuiteID()))
        htmlString = htmlString.replace('r_total_tests',str(totalTests))
        htmlString = htmlString.replace('r_passed',str(summaryTestSuite.passTests))
        htmlString = htmlString.replace('r_failed',str(summaryTestSuite.failedTests))
        htmlString = htmlString.replace('r_inconclusive',str(summaryTestSuite.inconclusiveTests))
        htmlString = htmlString.replace('r_success_rate',s_successRate + '%')
        htmlString = htmlString.replace('r_start_time',s_startTime)
        htmlString = htmlString.replace('r_end_time',s_endTime)
        htmlString = htmlString.replace('r_elapsed_time',s_elapsedTime)
        htmlString = htmlString.replace('r_overview',s_overview)
        htmlString = htmlString.replace('r_report_time',s_reportTime)
        
        headTagIndex = htmlString.index("</head>")
        htmlString = htmlString[:headTagIndex] + "<style> @page {size: a4 landscape;margin: 2cm;} .table th {text-align: left;} </style>" + htmlString[headTagIndex:]
        pisa.CreatePDF(htmlString, dest=htmlFile)
        htmlFile.close()