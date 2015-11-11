'''
Created on 02/11/2015

@author: S41nz
'''

import time

#class TBTAFOrchestrator():
class TBTAFOrchestrator(object):
    '''
    Class that encapsulates the information from a given event within the TBTAF 
    '''
    
    #Fields
	#Declare global variables
	_tBTestSuiteInstance
	_tBTestBedInstance
	_projectName
	TBTAFInterpreter _interpreter
	
    def __init__(self, nameFile = "nameFileDefault.txt"):
		#El parametro nameFile
        '''
        Constructor
        '''
		#leer archivo los parametros. Si no, tener unos parametros por default.
		#buscar como tirar una initialiation exception
		#buscar como tirar una invalid argument exception

		#Initialize variables
		#TBTAFInterpreter _interpreter
		_tBTestSuiteInstance
		_tBTestBedInstance
		_projectName
		

    def createNewProject(tBTestSuiteInstance, tBTestBedInstance, projectName):		
		_tBTestSuiteInstance = tBTestSuiteInstance
		_tBTestBedInstance = tBTestBedInstance
		_projectName = projectName
		#Invalid Argument Exception
        
    def parseScript(self, filePath):
		#return _interpreter.parseScript(filePath)

    def createTestBed(self, urlList):
        #if urlList is null
			#urlList = "localhost"
		
		#Initialize TBTestBed
		#TBTestBed tBtestBedInstance
		#myTestBed = createTestBed(Collection of URLS to the execution nodes)
		#La lista de urls va a estar asociado a un proyecto.
	
	#filePath - String containing the filepath where the test cases are located.
	#smartFilePath - Optional string containing the filepath where the production source code is located. This would be useful for TBSmartTestSuite creation.
	#tagList - String containing the list of tags which are desired to be executed among the existing test code within the specified location
	#puede que sea privado, ahorita lo consideramos publico y no lo mandamos a llamar en el constructor
    def createTestSuite(self, filePath, smartFilePath, tagList):
	
	#Primero hay que checar que las últimas dos variables no sean nulas
	#Si no son deben contener ubicacion válidas
	if smartFilePath is not null or tagList is not null
		if validateExisitingLocations(smartFilePath) and validateExisitingLocations(tagList)
			tbTestSuiteInstance = createTestSuite()
			
	else
		#Throw Invalid Argument Exception.
	
	
	#tbTestSuiteInstance - Reference to a given TBTestSuite instance from which the test plan will be generated.
	#testPlanLocation - String specifying the location where the test plan wants to be placed.
	#outputFormat - Enumeration flag specifying the output format of the created test plan.
	def publishTestPlan(self, tbTestSuiteInstance, testPlanLocation, outputFormat):
		#TBTAFPublisher tbtafPublisherInstance
		#tbtafPublisherInstance.PublishTestPlan(tbTestSuiteInstance, testPlanLocation, outputFormat)

	#tbTestSuiteInstance - Reference to a given TBTestSuite instance from which the result report will be generated.
	#resultLocation - String specifying the location where the result report wants to be placed.
	#outputFormat - Enumeration flag specifying the output format of the created result report.
	def publishTestResults(self, tbTestSuiteInstance, resultLocation, outputFormat):
		#TBTAFPublisher tbtafPublisherInstance
		#tbtafPublisherInstance.PublishTestResults(tbTestSuiteInstance, resultLocation, outputFormat)
	
	#tbTestSuiteInstance - Reference to a given TBTestSuite instance from which the result report will be generated.
    #tbTestSuiteInstance - Reference of the TBTestSuite representing the set of tests that will be executed.
    #urlCollection - Optional collection of URLs corresponding to the nodes on which the test execution will be distributed.
    #flagsCollection - Optional collection of flags that can customize the execution of such TBTestSuite.
    #executorListenerCollection - Optional collection of ExecutorListener implementations that would want to listen and react to specific events during the execution of that specific TBTestSuite
	def excuteTestSuite(self, tbTestSuiteInstance, urlCollection, flagsCollection, executorListenerCollection):
		#TBTAFExecutor tbtafExecutorInstance
		return tbtafExecutorInstance.ExecuteTests(tbTestSuiteInstance, urlCollection, flagsCollection, executorListenerCollection)
	
    #projectName - String identifying the Project from where the query is being made.
    #tagList - Optional List of tags in order to filter the query being made.
    #indicatorEnumeration - If the list of tags is provided, then an additional enumeration can be passed in order to specify if the tags will be used to filter IN or OUT the results found.	
	def GetTests(projectName, tagList, inOutList)
				
		#If the parameters being passed are null or contain null then an Invalid Argument Exception will be thrown.
		#If the provided Project key does not exist on the currently connected datasource, then a Not Existing Project Exception will be thrown.
		#If the provided filtering enumeration is provided, then a Not Supported Filter Exception will be thrown.

		return _tBTestSuiteInstance.getTestCases(tagList, inOutList)

    def getEventSource(self):
        return self.eventSource