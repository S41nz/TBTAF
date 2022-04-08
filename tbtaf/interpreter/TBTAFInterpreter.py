'''
Crstr(e)atstr(e)d on 22/11/2015
@author:
'''

from __future__ import absolute_import
from __future__ import print_function
# from exceptions import IOError
import regex as re
import os as _os
import sys
from .result import Result
from .status import TBTAFParsingScriptStatus
from .parsing_summary import ParsingSummary
from common.enums.filter_type import TBTAFFilterType
import orchestrator.TBTAFOrchestrator
from common.exception.IllegalArgumentException import IllegalArgumentException
from common.exception.NonSupportedFormatException import NonSupportedFormatException

class TBTAFInterpreter(object):
    '''
        TBTAFInterpreter
    '''

    OrchestratorReference = None
    summary = ParsingSummary()
    urlPattern = urlPattern = "\"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?\""

    ##Params in commands
    TEST_SUITE_PARAM = "testSuite"
    FILE_PATH_PARAM = "filePath"
    TEST_BED_PARAM = "testBed"
    PROJECT_NAME_PARAM = "projectName"
    TAG_LIST_PARAM = "tagList"
    FLAG_LIST_PARAM_1 = "flagList1"
    FLAG_LIST_PARAM_2 = "flagList2"
    FILTER_PARAM = "filter"
    FORMAT_PARAM = "format"
    URL_LIST_PARAM = "urlList"
    TEST_SUITE_ID_PARAM = "testSuiteId"

    ##Available commands
    CREATE_TEST_BED = "create_test_bed"
    CREATE_TEST_SUITE = "create_test_suite"
    CREATE_NEW_PROJECT = "create_new_project"
    PUBLIS_TEST_PLAN = "publish test_plan"
    EXECUTE = "execute"
    PUBLISH_TEST_RESULT = "publish test_results"
    GET_TEST = "get_tests"
    GET_TAGS = "get_tags"
    STORE_TEST_RESULT = "ingest test_results"
    GET_TEST_RESULT = "get test_results"

    ##Patterns
    TEST_SUITE = "(?P<"+ TEST_SUITE_PARAM +">(\w+))"
    FILE_PATH = "\"(?P<"+ FILE_PATH_PARAM +">(.+))\""
    TEST_BED = "(?P<"+ TEST_BED_PARAM +">(\w+))"
    PROJECT_NAME = "\"(?P<"+ PROJECT_NAME_PARAM +">(.+))\""
    TAG_LIST = "\[(?P<"+ TAG_LIST_PARAM +">((\"\w+\")(,\"\w+\")*))\]"
    FILTER = "(?P<"+ FILTER_PARAM +">(\w+))"
    FORMAT = "(?P<"+ FORMAT_PARAM +">(\w+))"
    TEST_SUITE_ID = "(?P<"+ TEST_SUITE_ID_PARAM +">(\w+))"
    FLAG_LIST_1 = "\[(?P<"+ FLAG_LIST_PARAM_1 +">((\w+)(,\w+)*))\]"
    FLAG_LIST_2 = "\[(?P<"+ FLAG_LIST_PARAM_2 +">((\w+)(,\w+)*))\]"
    ##URL_LIST = "(?P<"+ URL_LIST_PARAM +">(("+ urlPattern +")(,"+ urlPattern +")*))"
    ##URL_LIST = "(?P<"+ URL_LIST_PARAM +">(("+ "\".+\"" +")(,"+ "\".+\"" +")*))"
    URL_LIST = "\[(?P<"+ URL_LIST_PARAM +">(("+ "\".+\"" +")(,"+ "\".+\"" +")*))\]"

    ##Message Types
    MSG_ERROR = "Error"
    MSG_WARNING = "Warning"

    FILE_NAME = "fileName"
    FILE_LINE_NUMBER = "lineNumber"

    ##Patterns
    a = "(?P<variable>\w+)\s*=\s*(?P<method>\\create_test_bed\\b)\(("+ URL_LIST +")?\)"
    b = "(?P<variable>\w+)\s*=\s*(?P<method>\\create_test_suite\\b)\("+ FILE_PATH +"(,"+ TAG_LIST +")?\)"
    c = "(?P<method>\\create_new_project\\b)\("+ TEST_SUITE +","+ TEST_BED +","+ PROJECT_NAME +"\)"
    d = "(?P<method>\\publish test_plan\\b)\("+ TEST_SUITE +","+ FILE_PATH +","+ FORMAT +"\)"
    e = "(?P<variable>\w+)\s*=\s*(?P<method>\\execute\\b)\("+ TEST_SUITE +","+ TEST_BED +"(,"+ FLAG_LIST_1 +")?(,"+ FLAG_LIST_2 +")?\)"
    f = "(?P<method>\\publish test_results\\b)\("+ TEST_SUITE +","+ FILE_PATH +","+ FORMAT +"\)"
    g = "(?P<method>\\get_tests\\b)\("+ PROJECT_NAME +"((\,"+ TAG_LIST +"),"+ FILTER +")?\)"
    h = "(?P<method>\\get_tags\\b)\("+ PROJECT_NAME +"\)"
    i = "(?P<method>\\ingest test_results\\b)\("+ TEST_SUITE +"\)"
    j = "(?P<method>\\get test_results\\b)\("+ TEST_SUITE_ID +","+ FILE_PATH +","+ FORMAT +"\)"

    def __init__(self):
        '''
            Constructor
        '''

    def _formatMsg(self,fileName, lineNumber, text, _type):
        message = "{} :     File {},line {},Description: {}\n"
        return message.format(_type, str(fileName), str(lineNumber), text)
        ##return message.format("","","","")

    def parseScript(self, scriptURL):
        result = Result(TBTAFParsingScriptStatus.SUCCESS, "Success")
        file = None
        try:
            file = self._openFile(scriptURL)
            self._parseFile(file, result)

            if (result.status==TBTAFParsingScriptStatus.ERROR):
                file.close()
                ##return result
            else:
                if (TBTAFInterpreter.OrchestratorReference is None):
                    result.status=TBTAFParsingScriptStatus.ERROR
                    result.message="Orchestrator Reference has not been set."
                    ##return result

                if(result.status==TBTAFParsingScriptStatus.SUCCESS):
                    self.startExecution(TBTAFInterpreter.OrchestratorReference)

            #print result.status
            #print result.message

        except Exception as e:
            #traceback.print_exc(e)
            raise e
        finally:
            if(file is not None):
                file.close()

        return result

    def _openFile(self,file):
        """
            This method returns object "_file"
        """
        ##________Verify is File exists________
        if (_os.path.isfile(file)):
            pass
        else:
            raise ValueError("File does not exist.")
        ##________Open File and return result________
        try:
            _file = open(file,"r")
            return _file
        except IOError:
            raise ValueError("Cannot open file.")


    ##----------------------------------------------
    ## Main method that will parse tbtaf script    -
    ##----------------------------------------------
    def _parseFile(self,file,result):
        """
        """
        ##________Dict for calling each regular expression________
        mappingPatterns   = {
        TBTAFInterpreter.CREATE_TEST_BED    :TBTAFInterpreter.a,
        TBTAFInterpreter.CREATE_TEST_SUITE  :TBTAFInterpreter.b,
        TBTAFInterpreter.CREATE_NEW_PROJECT :TBTAFInterpreter.c,
        TBTAFInterpreter.PUBLIS_TEST_PLAN   :TBTAFInterpreter.d,
        TBTAFInterpreter.EXECUTE            :TBTAFInterpreter.e,
        TBTAFInterpreter.PUBLISH_TEST_RESULT:TBTAFInterpreter.f,
        TBTAFInterpreter.GET_TEST           :TBTAFInterpreter.g,
        TBTAFInterpreter.GET_TAGS           :TBTAFInterpreter.h,
        TBTAFInterpreter.STORE_TEST_RESULT  :TBTAFInterpreter.i,
        TBTAFInterpreter.GET_TEST_RESULT  :TBTAFInterpreter.j}
        ##________Read each line of the file and look for a match of defined methods________
        for i, line in enumerate(file):
            ##________Delete White Spaces from the corners________
            line = line.strip()
            fileName = file.name
            lineNumber = i + 1

            if (line == ""):
                continue
            elif (line.startswith("//")):
                continue
            for command in mappingPatterns:
                if (command in line):
                    m = re.match(mappingPatterns[command],line)
                    if (m is None):
                        result.status  = TBTAFParsingScriptStatus.ERROR
                        result.message = self._formatMsg(fileName, lineNumber, "Cannot find command", TBTAFInterpreter.MSG_ERROR)
                    else:
                        m = m.groupdict()
                        error = self._addToSummary(m, fileName, lineNumber)
                        if(error == ""):
                            break
                        else:
                            result.status  = TBTAFParsingScriptStatus.ERROR
                            result.message = error
                            return -1
            else:
                result.status  = TBTAFParsingScriptStatus.ERROR
                result.message = self._formatMsg(fileName, lineNumber, "Malformed command", TBTAFInterpreter.MSG_ERROR)
                return -1

    def _addToSummary(self,m, fileName, lineNumber):
        m[TBTAFInterpreter.FILE_NAME] = fileName
        m[TBTAFInterpreter.FILE_LINE_NUMBER] = lineNumber
        error = '{} is not defined.'
        command = m["method"]

        if (command == TBTAFInterpreter.CREATE_TEST_BED):
            TBTAFInterpreter.summary.createTestBed[m["variable"]] = m

        elif (command == TBTAFInterpreter.CREATE_TEST_SUITE):
            TBTAFInterpreter.summary.createTestSuite[m["variable"]] = m

        elif (command == TBTAFInterpreter.CREATE_NEW_PROJECT):
            if not(m[TBTAFInterpreter.TEST_SUITE_PARAM] in TBTAFInterpreter.summary.createTestSuite):
                error = error.format(m[TBTAFInterpreter.TEST_SUITE_PARAM])
                return self._formatMsg(fileName, lineNumber, error, TBTAFInterpreter.MSG_ERROR)
            if not(m[TBTAFInterpreter.TEST_BED_PARAM] in TBTAFInterpreter.summary.createTestBed):
                error = error.format(m[TBTAFInterpreter.TEST_BED_PARAM])
                return self._formatMsg(fileName, lineNumber, error, TBTAFInterpreter.MSG_ERROR)

            TBTAFInterpreter.summary.createNewProject[m[TBTAFInterpreter.PROJECT_NAME_PARAM]] = m

        elif (command == TBTAFInterpreter.PUBLIS_TEST_PLAN):
            if not(m[TBTAFInterpreter.TEST_SUITE_PARAM] in TBTAFInterpreter.summary.createTestSuite):
                error = error.format(m[TBTAFInterpreter.TEST_SUITE_PARAM])
                return self._formatMsg(fileName, lineNumber, error, TBTAFInterpreter.MSG_ERROR)

            TBTAFInterpreter.summary.publishTestPlan.append(m)

        elif (command == TBTAFInterpreter.EXECUTE):
            if not(m[TBTAFInterpreter.TEST_SUITE_PARAM] in TBTAFInterpreter.summary.createTestSuite):
                error = error.format(m[TBTAFInterpreter.TEST_SUITE_PARAM])
                return self._formatMsg(fileName, lineNumber, error, TBTAFInterpreter.MSG_ERROR)

            TBTAFInterpreter.summary.execute[m["variable"]] = m

        elif (command == TBTAFInterpreter.PUBLISH_TEST_RESULT):
            if not(m[TBTAFInterpreter.TEST_SUITE_PARAM] in TBTAFInterpreter.summary.createTestSuite):
                error = error.format(m[TBTAFInterpreter.TEST_SUITE_PARAM])
                return self._formatMsg(fileName, lineNumber, error, TBTAFInterpreter.MSG_ERROR)

            TBTAFInterpreter.summary.publishTestResults.append(m)

        elif (command == TBTAFInterpreter.GET_TEST):
            if not(m[TBTAFInterpreter.PROJECT_NAME_PARAM] in TBTAFInterpreter.summary.createNewProject):
                error = error.format(m[TBTAFInterpreter.PROJECT_NAME_PARAM])
                return self._formatMsg(fileName, lineNumber, error, TBTAFInterpreter.MSG_ERROR)

            TBTAFInterpreter.summary.getTest.append(m)
        elif (command ==TBTAFInterpreter.GET_TAGS):
            if not(m[TBTAFInterpreter.PROJECT_NAME_PARAM] in TBTAFInterpreter.summary.createNewProject):
                error = error.format(m[TBTAFInterpreter.PROJECT_NAME_PARAM])
                return self._formatMsg(fileName, lineNumber, error, TBTAFInterpreter.MSG_ERROR)

            TBTAFInterpreter.summary.getTags.append(m)
            
        elif (command == TBTAFInterpreter.STORE_TEST_RESULT):
            if not(m[TBTAFInterpreter.TEST_SUITE_PARAM] in TBTAFInterpreter.summary.createTestSuite):
                error = error.format(m[TBTAFInterpreter.TEST_SUITE_PARAM])
                return self._formatMsg(fileName, lineNumber, error, TBTAFInterpreter.MSG_ERROR)
            TBTAFInterpreter.summary.storeTestResults.append(m)

        elif (command == TBTAFInterpreter.GET_TEST_RESULT):
            TBTAFInterpreter.summary.getTestResults.append(m)            
        error = ""
        return error

    def setOrchestratorReference(self, orchestrator):
        TBTAFInterpreter.OrchestratorReference=orchestrator

    def startExecution(self,orchestrator):
        objs = {}
        fileName = ""
        lineNumber = ""

        try:
            #CreateTestBed
            testBeds = TBTAFInterpreter.summary.createTestBed
            for var in testBeds.keys():
                fileName = testBeds[var][TBTAFInterpreter.FILE_NAME]
                lineNumber = testBeds[var][TBTAFInterpreter.FILE_LINE_NUMBER]

                urlList = testBeds[var][TBTAFInterpreter.URL_LIST_PARAM]

                if(urlList is None):
                    objs[var] = orchestrator.createTestBed()
                else:
                    urlList = urlList.split(",")
                    urlList = [url.replace('\"', '') for url in urlList]
                    objs[var] = orchestrator.createTestBed(urlList)

            #CreateTestSuite
            testSuites = TBTAFInterpreter.summary.createTestSuite
            for var in testSuites.keys():
                fileName = testSuites[var][TBTAFInterpreter.FILE_NAME]
                lineNumber = testSuites[var][TBTAFInterpreter.FILE_LINE_NUMBER]

                filePath = testSuites[var][TBTAFInterpreter.FILE_PATH_PARAM]
                tagList = testSuites[var][TBTAFInterpreter.TAG_LIST_PARAM]
                if not(tagList is None):
                    tagList = tagList.split(",")
                    tagList = [tag.replace('\"', '') for tag in tagList]

                objs[var] = orchestrator.createTestSuite(filePath, tagList)

            #CreateNewProject
            projects = TBTAFInterpreter.summary.createNewProject
            for var in projects.keys():
                fileName = projects[var][TBTAFInterpreter.FILE_NAME]
                lineNumber = projects[var][TBTAFInterpreter.FILE_LINE_NUMBER]

                testSuite = objs[projects[var][TBTAFInterpreter.TEST_SUITE_PARAM]]
                testBed = objs[projects[var][TBTAFInterpreter.TEST_BED_PARAM]]
                projectName = projects[var][TBTAFInterpreter.PROJECT_NAME_PARAM]

                orchestrator.createNewProject(testSuite, testBed, projectName)

        except (ValueError, IllegalArgumentException, NonSupportedFormatException) as e:
            print(self._formatMsg(fileName, lineNumber, "Fatal Error. Execution cannot continue. " + str(e), TBTAFInterpreter.MSG_ERROR))

        #ExecuteTests
        try:
            #TBTAFInterpreter.summary.execute = executions
            executions= TBTAFInterpreter.summary.execute
            for var in executions.keys():
                fileName = executions[var][TBTAFInterpreter.FILE_NAME]
                lineNumber = executions[var][TBTAFInterpreter.FILE_LINE_NUMBER]

                testSuite = objs[executions[var][TBTAFInterpreter.TEST_SUITE_PARAM]]
                testBed = objs[executions[var][TBTAFInterpreter.TEST_SUITE_PARAM]]

                flagList1 = executions[var][TBTAFInterpreter.FLAG_LIST_PARAM_1]
                flagList2 = executions[var][TBTAFInterpreter.FLAG_LIST_PARAM_2]

                if not(flagList1 is None):
                    flagList1 = flagList1.split(",")
                    flagList1 = [flag.replace('\"', '') for flag in flagList1]
                else:
                    flagList1=[]

                if not(flagList2 is None):
                    flagList2 = flagList2.split(",")
                    flagList2 = [flag.replace('\"', '') for flag in flagList2]
                else:
                   flagList2=[]

                objs[var] = orchestrator.executeTestSuite(testSuite, testBed, flagList1, flagList2)

        except ValueError as e:
            print(self._formatMsg(fileName, lineNumber, str(e), TBTAFInterpreter.MSG_ERROR))
            return

        #PublishTestPlan
        try:
            for var in TBTAFInterpreter.summary.publishTestPlan:
                fileName = var[TBTAFInterpreter.FILE_NAME]
                lineNumber = var[TBTAFInterpreter.FILE_LINE_NUMBER]

                #testSuite = var[TBTAFInterpreter.TEST_SUITE_PARAM]
                testSuite= objs[var[TBTAFInterpreter.TEST_SUITE_PARAM]]
                filePath = var[TBTAFInterpreter.FILE_PATH_PARAM]
                format = var[TBTAFInterpreter.FORMAT_PARAM]

                orchestrator.publishTestPlan(testSuite, filePath, format)

        except (ValueError, IllegalArgumentException, NonSupportedFormatException) as e:
            print(self._formatMsg(fileName, lineNumber, str(e), TBTAFInterpreter.MSG_WARNING))

        #PublishResultReport
        try:
            for var in TBTAFInterpreter.summary.publishTestResults:
                fileName = var[TBTAFInterpreter.FILE_NAME]
                lineNumber = var[TBTAFInterpreter.FILE_LINE_NUMBER]

                testSuite= objs[var[TBTAFInterpreter.TEST_SUITE_PARAM]]
                filePath = var[TBTAFInterpreter.FILE_PATH_PARAM]
                format = var[TBTAFInterpreter.FORMAT_PARAM]

                orchestrator.publishResultReport(testSuite, filePath, format)
				
        except (ValueError, IllegalArgumentException, NonSupportedFormatException) as e:
            print(self._formatMsg(fileName, lineNumber, str(e), TBTAFInterpreter.MSG_WARNING))

        #StoreResultReport
        try:
            for var in TBTAFInterpreter.summary.storeTestResults:
                fileName = var[TBTAFInterpreter.FILE_NAME]
                lineNumber = var[TBTAFInterpreter.FILE_LINE_NUMBER]

                testSuite= objs[var[TBTAFInterpreter.TEST_SUITE_PARAM]]

                orchestrator.storeResultReport(testSuite)
				
        except (ValueError, IllegalArgumentException, NonSupportedFormatException) as e:
            print(self._formatMsg(fileName, lineNumber, str(e), TBTAFInterpreter.MSG_WARNING))

        #GetResultReport
        try:
            for var in TBTAFInterpreter.summary.getTestResults:
                fileName = var[TBTAFInterpreter.FILE_NAME]
                lineNumber = var[TBTAFInterpreter.FILE_LINE_NUMBER]

                testSuiteId= var[TBTAFInterpreter.TEST_SUITE_ID_PARAM]
                filePath = var[TBTAFInterpreter.FILE_PATH_PARAM]
                format = var[TBTAFInterpreter.FORMAT_PARAM]
                orchestrator.getResultReport(testSuiteId, filePath, format)
				
        except (ValueError, IllegalArgumentException, NonSupportedFormatException) as e:
            print(self._formatMsg(fileName, lineNumber, str(e), TBTAFInterpreter.MSG_WARNING))

        #GetTests
        try:
            for var in TBTAFInterpreter.summary.getTest:
                fileName = var[TBTAFInterpreter.FILE_NAME]
                lineNumber = var[TBTAFInterpreter.FILE_LINE_NUMBER]

                projectName = var[TBTAFInterpreter.PROJECT_NAME_PARAM]
                tagList = var[TBTAFInterpreter.TAG_LIST_PARAM]
                if not(tagList is None):
                    tagList = tagList.split(",")
                    tagList = [tag.replace('\"', '') for tag in tagList]
                filter = var[TBTAFInterpreter.FILTER_PARAM]
                if(filter == "IN"):
                    filter = TBTAFFilterType.IN
                elif(filter == "OUT"):
                    filter = TBTAFFilterType.OUT
                else:
                    filter = None

                if (tagList is None or filter is None):
                    orchestrator.getTests(projectName)
                else:
                    orchestrator.getTests(projectName, tagList, filter)

        except ValueError as e:
            print(self._formatMsg(fileName, lineNumber, str(e), TBTAFInterpreter.MSG_WARNING))

        #GetTags
        try:
            for var in TBTAFInterpreter.summary.getTags:
                fileName = var[TBTAFInterpreter.FILE_NAME]
                lineNumber = var[TBTAFInterpreter.FILE_LINE_NUMBER]

                projectName = var[TBTAFInterpreter.PROJECT_NAME_PARAM]

                orchestrator.getTags(projectName)

        except ValueError as e:
            print(self._formatMsg(fileName, lineNumber, str(e), TBTAFInterpreter.MSG_WARNING))
