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
        Builds a test execution report on a desired format
        based on the execution result of a given test suite
        '''
        #Read HTML Template file and put into a string
        htmlTemplate = open('template.html','r')
        htmlString = htmlTemplate.read()
        #Get summary result from the test suite instance
        summaryTestSuite = tBTestSuiteInstance.getSuiteResult()
        #Calculate total number of test cases
        totalTests = len(tBTestSuiteInstance.suiteTestCases)
        #Calculate success rate of test summary results 
        successRate = (float(summaryTestSuite.passTests) / float(totalTests))*100
        s_successRate = format("%.2f" % successRate)
        #Get start & end dates and format them for display 
        startTime = summaryTestSuite.getStartTimestamp()
        endTime = summaryTestSuite.getEndTimestamp()
        s_startTime = startTime.strftime('%B %d,%Y %H:%M:%S')
        s_endTime = endTime.strftime('%B %d,%Y %H:%M:%S')
        #Calculate elapsed time and format it for display
        elapsedTime = endTime - startTime
        s_elapsedTime = str(elapsedTime)
        #Calculate report time
        reportTime = datetime.datetime.now()
        s_reportTime = reportTime.strftime('%B %d,%Y %H:%M:%S')


        #Replace the html string with summary results
        htmlString = htmlString.replace('r_total_tests',total_tests)
        htmlString = htmlString.replace('r_passed',summaryTestSuite.passTests )
        htmlString = htmlString.replace('r_failed',summaryTestSuite.failedTests)
        htmlString = htmlString.replace('r_inconclusive',summaryTestSuite.inconclusiveTests)
        htmlString = htmlString.replace('r_success_rate',s_successRate + '%')
        htmlString = htmlString.replace('r_start_time',s_start_time)
        htmlString = htmlString.replace('r_end_time',s_end_time)
        htmlString = htmlString.replace('r_end_time',s_elapsed_time)
        htmlString = htmlString.replace('r_report_time',s_report_time)
        htmlFile = open(filePath,'w')
        htmlFile.write(htmlString)
        htmlFile.close()
