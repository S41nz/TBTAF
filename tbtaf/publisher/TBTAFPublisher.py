'''
Created on 07/11/2015

@author: @andresmuro , @andres.alvarado , @mestradago , @rnunezc
'''
import datetime
#class TBTAFPublisher():
class TBTAFPublisher(object):
    '''
    The TBTAF Publisher is in charge of generating all the test 
    execution related documentation.
    '''

    def __init__(self):
        #Constructor
        pass

    def PublishTestPlan(self, tBTestSuiteInstance, filePath, formatFlag):
        '''
        Builds a test plan specification on a desired format
        based on the discovered metadata
        '''
        htmlString = ""
        testCasesList = tBTestSuiteInstance.getTestCases();

        for testCase in testCasesList:
            testMetaData = testCase.getTestMetadata()
            print testMetaData.getAssetID()
            testTags = testMetaData.getTags()
            tagsString = ""
            for tag in testTags:
                tagsString = tagsString + tag + " "
                print "Tags: " + tagsString
            print testMetaData.getPriority()
            print testMetaData.getAssetDescription()

        '''
        htmlFile = open(filePath,'w')
        htmlFile.write(htmlString)
        htmlFile.close()
        '''

    def PublishResultReport(tBTestSuiteInstance, filePath, formatFlag):
        '''
        Builds a test execution report on a HTML format
        based on the execution result of a given test suite
        '''
        #Read HTML Template file and put into a string
        htmlTemplate = open('/publisher/results_template.html','r')
        htmlString = htmlTemplate.read()
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
            for tag in testTags:
                s_overview = s_overview + "<td>" + tag + ","
            #Remove last character from tags
            s_overview = s_overview[:-1]
            #Add close table data tag to HTML
            s_overview = s_overview + + "</td>"
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
        s_reportTime = reportTime.strftime('%B %d,%Y %H:%M:%S')
        reportTime = datetime.datetime.now()

        #Replace the html string with summary results
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
        htmlFile = open(filePath,'w+')
        htmlFile.write(htmlString)
        htmlFile.close()
