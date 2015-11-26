'''
Crstr(e)atstr(e)d on 22/11/2015
@author:
'''

from exceptions import IOError
import re
import os as _os
import sys
from result import Result
from status import TBTAFParsingScriptStatus
from parsing_summary import ParsingSummary
from common.enums.filter_type import TBTAFFilterType
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator

class TBTAFInterpreter(object):
    '''
        TBTAFInterpreter
    '''

    summary = ParsingSummary()
    urlPattern = urlPattern = "(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?"

    ##Params in commands
    TEST_SUITE_PARAM = "testSuite"
    FILE_PATH_PARAM = "filePath"
    TEST_BED_PARAM = "testBed"
    PROJECT_NAME_PARAM = "projectName"
    TAG_LIST_PARAM = "tagList"
    FILTER_PARAM = "filter"
    FORMAT_PARAM = "format"
    URL_LIST_PARAM = "urlList"

    ##Available commands
    CREATE_TEST_BED = "create_test_bed"
    CREATE_TEST_SUITE = "create_test_suite"
    CREATE_NEW_PROJECT = "create_new_project"
    PUBLIS_TEST_PLAN = "publish test_plan"
    EXECUTE = "execute"
    PUBLISH_TEST_RESULT = "publish test_results"
    GET_TEST = "get tests"
    GET_TAGS = "get tags"

    ##Patterns
    TEST_SUITE = "(?P<"+ TEST_SUITE_PARAM +">(\w+))"
    FILE_PATH = "(?P<"+ FILE_PATH_PARAM +">(.*))"
    TEST_BED = "(?P<"+ TEST_BED_PARAM +">(\w+))"
    PROJECT_NAME = "\"(?P<"+ PROJECT_NAME_PARAM +">(.*))\""
    TAG_LIST = "\[(?P<"+ TAG_LIST_PARAM +">((<\w+>)(,<\w+>)*))\]"
    FILTER = "(?P<"+ FILTER_PARAM +">(\w+))"
    FORMAT = "(?P<"+ FORMAT_PARAM +">(\w+))"
    URL_LIST = "(?P<"+ URL_LIST_PARAM +">(("+ urlPattern +")(,"+ urlPattern +")*))"

    ##Message Types
    MSG_ERROR = "Error"
    MSG_WARNING = "Warning"

    FILE_NAME = "fileName"
    FILE_LINE_NUMBER = "lineNumber"

    ##Patterns
    a = "(?P<variable>\w+)\s*=\s*(?P<method>\\create_test_bed\\b)(\("+ URL_LIST +"\))?"
    b = "(?P<variable>\w+)\s*=\s*(?P<method>\\create_test_suite\\b)\("+ FILE_PATH +"(\,"+ TAG_LIST +")?\)"
    c = "(?P<method>\\create_new_project\\b)\("+ TEST_SUITE +","+ TEST_BED +","+ PROJECT_NAME +"\)"
    d = "(?P<method>\\publish test_plan\\b)\("+ TEST_SUITE +","+ FILE_PATH +","+ FORMAT +"\)"
    e = "(?P<variable>\w+)\s*=\s*(?P<method>\\execute\\b)\("+ TEST_SUITE +","+ TEST_BED +"\)"
    f = "(?P<method>\\publish test_results\\b)\("+ TEST_SUITE +","+ FILE_PATH +","+ FORMAT +"\)"
    g = "(?P<method>\\get tests\\b)\("+ PROJECT_NAME +"((\,"+ TAG_LIST +"),"+ FILTER +")?\)"
    h = "(?P<method>\\get tags\\b)\("+ PROJECT_NAME +"\)"

    def __init__(self):
        '''
            Constructor
        '''

    def _formatMsg(self,fileName, lineNumber, message, _type):
        #message = "{} :     File \"{}}\",line {}}\nDescription: {}}\n"
        return message.format(_type, str(fileName), str(lineNumber), message)
        ##return message.format("","","","")
	
    def _parseScript(self, scriptURL):
        result = Result(TBTAFParsingScriptStatus.SUCCESS, "Success")
        file = None
        try:
            file = self._openFile(scriptURL)
            if (self._parseFile(file, result) == -1):
                file.close()
                print(result.status)
                print(result.message)
                return result
        except Exception as e:
            print str(e)
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
        mappingPatterns   = {TBTAFInterpreter.CREATE_TEST_BED  :TBTAFInterpreter.a,TBTAFInterpreter.CREATE_TEST_SUITE:TBTAFInterpreter.b ,TBTAFInterpreter.CREATE_NEW_PROJECT  :TBTAFInterpreter.c,
                      TBTAFInterpreter.PUBLIS_TEST_PLAN:TBTAFInterpreter.d,TBTAFInterpreter.EXECUTE          :TBTAFInterpreter.e ,TBTAFInterpreter.PUBLISH_TEST_RESULT:TBTAFInterpreter.f,
                      TBTAFInterpreter.GET_TEST        :TBTAFInterpreter.g,TBTAFInterpreter.GET_TAGS         :TBTAFInterpreter.h}

        ##________Read each line of the file and look for a match of defined methods________
        for i, line in enumerate(file):
            ##________Delete White Spaces from the corners________
            line = line.strip()
            if (line == ""):
                pass
            elif (line.startswith("//")):
                pass

            for command in mappingPatterns:
                if (command in line):
                    m = re.match(mappingPatterns[command],line)
                    fileName = file.name
                    lineNumber = i + 1

                    if (m is None):
                        result.status  = TBTAFParsingScriptStatus.ERROR
                        result.message = self._formatMsg(fileName, lineNumber, "Cannot find command", TBTAFInterpreter.MSG_ERROR)
                    else:
                        m = m.groupdict()
                        ##print("Matched method = " + str(method))
                        ##print(str(m))
                        error = self._addToSummary(m, fileName, lineNumber)
                        if(error != ""):
                            result.status  = TBTAFParsingScriptStatus.ERROR
                            result.message = error
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
                return formatMsg(fileName, index, error, TBTAFInterpreter.MSG_ERROR)
            if not(m[TBTAFInterpreter.TEST_BED_PARAM] in TBTAFInterpreter.summary.createTestBed):
                error = error.format(m[TBTAFInterpreter.TEST_BED_PARAM])
                return formatMsg(fileName, index, error, TBTAFInterpreter.MSG_ERROR)

            TBTAFInterpreter.summary.createNewProject[m[TBTAFInterpreter.PROJECT_NAME_PARAM]] = m

        elif (command == TBTAFInterpreter.PUBLIS_TEST_PLAN):
            if not(m[TBTAFInterpreter.TEST_SUITE_PARAM] in TBTAFInterpreter.summary.createTestSuite):
                error = error.format(m[TBTAFInterpreter.TEST_SUITE_PARAM])
                return formatMsg(fileName, index, error, TBTAFInterpreter.MSG_ERROR)

            TBTAFInterpreter.summary.publishTestPlan.append(m)

        elif (command == TBTAFInterpreter.EXECUTE):
            if not(m[TBTAFInterpreter.TEST_SUITE_PARAM] in TBTAFInterpreter.summary.createTestSuite):
                error = error.format(m[TBTAFInterpreter.TEST_SUITE_PARAM])
                return formatMsg(fileName, index, error, TBTAFInterpreter.MSG_ERROR)

            TBTAFInterpreter.summary.execute[m["variable"]] = m

        elif (command == TBTAFInterpreter.PUBLISH_TEST_RESULT):
            if not(m[TBTAFInterpreter.TEST_SUITE_PARAM] in TBTAFInterpreter.summary.createTestSuite):
                error = error.format(m[TBTAFInterpreter.TEST_SUITE_PARAM])
                return formatMsg(fileName, index, error, TBTAFInterpreter.MSG_ERROR)

            TBTAFInterpreter.summary.publishTestResults.append(m)

        elif (command == TBTAFInterpreter.GET_TEST):
            if not(m[TBTAFInterpreter.PROJECT_NAME_PARAM] in TBTAFInterpreter.summary.createNewProject):
                error = error.format(m[TBTAFInterpreter.PROJECT_NAME_PARAM])
                return formatMsg(fileName, index, error, TBTAFInterpreter.MSG_ERROR)

            TBTAFInterpreter.summary.getTest.append(m)
        elif (command ==TBTAFInterpreter.GET_TAGS):
            if not(m[TBTAFInterpreter.PROJECT_NAME_PARAM] in TBTAFInterpreter.summary.createNewProject):
                error = error.format(m[TBTAFInterpreter.PROJECT_NAME_PARAM])
                return formatMsg(fileName, index, error, TBTAFInterpreter.MSG_ERROR)

            TBTAFInterpreter.summary.getTags.append(m)
        error = ""
        return error

    def setOrchestratorReference(self, orchestrator):
        self.startExecution(orchestrator)
        pass

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

        except (Exception) as e:
        ##except (ValueError, IllegalArgumentException, NonSupportedFormatException) as e:
            print self._formatMsg(fileName, lineNumber, "Fatal Error. Execution cannot continue. " + str(e), TBTAFInterpreter.MSG_ERROR)

        #PublishTestPlan
        try:
            for var in TBTAFInterpreter.summary.publishTestPlan:
                fileName = var[TBTAFInterpreter.FILE_NAME]
                lineNumber = var[TBTAFInterpreter.FILE_LINE_NUMBER]

                testSuite = var[TBTAFInterpreter.TEST_SUITE_PARAM]
                filePath = var[TBTAFInterpreter.FILE_PATH_PARAM]
                format = var[TBTAFInterpreter.FORMAT_PARAM]

                orchestrator.PublishTestPlan(testSuite, filePath, format)

        except (ValueError) as e:
        ##except (ValueError, IllegalArgumentException, NonSupportedFormatException) as e:
            print self._formatMsg(fileName, lineNumber, str(e), TBTAFInterpreter.MSG_WARNING)

        #PublishResultReport
        try:
            for var in TBTAFInterpreter.summary.publishTestResults:
                fileName = var[TBTAFInterpreter.FILE_NAME]
                lineNumber = var[TBTAFInterpreter.FILE_LINE_NUMBER]

                testSuite = var[TBTAFInterpreter.TEST_SUITE_PARAM]
                filePath = var[TBTAFInterpreter.FILE_PATH_PARAM]
                format = var[TBTAFInterpreter.FORMAT_PARAM]

                orchestrator.PublishResultReport(testSuite, filePath, format)
        except (ValueError) as e:
        ##except (ValueError, IllegalArgumentException, NonSupportedFormatException) as e:
            print self._formatMsg(fileName, lineNumber, str(e), TBTAFInterpreter.MSG_WARNING)

        #ExecuteTests
        try:
            #TBTAFInterpreter.summary.execute = executions
            executions= TBTAFInterpreter.summary.execute
            for var in executions.keys():
                fileName = executions[var][TBTAFInterpreter.FILE_NAME]
                lineNumber = executions[var][TBTAFInterpreter.FILE_LINE_NUMBER]

                testSuite = objs[executions[var][TBTAFInterpreter.TEST_SUITE_PARAM]]
                testBed = objs[executions[var][TBTAFInterpreter.TEST_SUITE_PARAM]]

                objs[var] = orchestrator.executeTests(testSuite, testBed)
        except ValueError as e:
            print self._formatMsg(fileName, lineNumber, str(e), TBTAFInterpreter.MSG_WARNING)


        #GetTests
        try:
            for var in TBTAFInterpreter.summary.getTest:
                fileName = var[TBTAFInterpreter.FILE_NAME]
                lineNumber = var[TBTAFInterpreter.FILE_LINE_NUMBER]

                projectName = var[TBTAFInterpreter.PROJECT_NAME_PARAM]
                tagList = var[TBTAFInterpreter.TAG_LIST_PARAM]
                if not(tagList is None):
                    tagList = tagList.split(",")
                filter = var[TBTAFInterpreter.FILTER_PARAM]
                if(filter == "IN"):
                    filter = TBTAFFilterType.IN
                elif(filter == "OUT"):
                    filter = TBTAFFilterType.OUT
                else:
                    filter = None

                if (tagList is None or _filter is None):
                    orchestrator.getTests(projectName)
                else:
                    orchestrator.getTests(projectName, tagList, _filter)

        except ValueError as e:
            print self._formatMsg(fileName, lineNumber, str(e), TBTAFInterpreter.MSG_WARNING)

        #GetTags
        try:
            for var in TBTAFInterpreter.summary.getTags:
                fileName = var[TBTAFInterpreter.FILE_NAME]
                lineNumber = var[TBTAFInterpreter.FILE_LINE_NUMBER]

                projectName = var[TBTAFInterpreter.PROJECT_NAME_PARAM]

                orchestrator.getTags(projectName)

        except ValueError as e:
            print self._formatMsg(fileName, lineNumber, str(e), TBTAFInterpreter.MSG_WARNING)

