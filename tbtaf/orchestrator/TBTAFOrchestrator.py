'''
Created on 02/11/2015

@author: S41nz
'''

import httplib
from common.test_bed import TBTestBed
from common.project import TBProject
from common.smart_suite import TBSmartTestSuite
from common.node import TBTestNode
from interpreter.interpreter import TBInterpreter
from discoverer.discoverer import TBDiscoverer

#from common.node import TBTestNode

class TBTAFOrchestrator(object):
    '''
    
    '''
    
    #Fields
	#Declare global variables
	#TBTAFInterpreter _interpreter
	#projectList
	#suiteTestCases = []

	def __init__(self, nameInitizalizationFile = ""):
        '''
        Constructor
        '''
		#leer archivo los parametros. Si no, tener unos parametros por default.
		#buscar como tirar una initialiation exception
		#buscar como tirar una invalid argument exception
        if isInvalidArgument(nameInitizalizationFile):
            print 'Error: TBTAFOrchestrator.__init__'
        else:
			projectList = []
			#self._interpreter = TBTAFInterpreter()
			#Initialize variables
			#self.suiteType = suiteType
			#self.suiteID = suiteID	

	def addProject(self, newProject)
		self.projectList.append(newProject)

    def createNewProject(tBTestSuiteInstance, tBTestBedInstance, projectName):
		#Revisar si es la forma pythonesca y si funcionan.
		if isInvalidArgument(tBTestSuiteInstance) or isInvalidArgument(tBTestBedInstance) or isInvalidArgument(projectName):
			print 'Error: TBTAFOrchestrator.createNewProject'
		else:
			if projectName in (projectInstance.projectName for projectInstance in projectList):
				raise ValueError("Already Existing Project Exception")
			else:
				project =  TBProject(tBTestSuiteInstance, tBTestBedInstance, projectName)
				self.addProject(project) 
				#Agregar mensajes de confirmacion en linea de comandos
				print 'New project created: ', projectName
				#Duda: Si es un Smart Test Suite, hay que poner todos? porque no se reciben etiquetas como parámetro, sólo el TBTestSuiteInstance
				#Duda: Qué pasa si llamamos a gestTestCases() para un smart suite... se corre el de TBTestSuite o de TBSmartTestSuite?
				print 'Number of tests: ', len(tBTestSuiteInstance.getTestCases()) 
				print 'Execution nodes: ', ', '.join(testNode.getNodeURL() for testNode in tBTestBedInstance.getTestBedNodes())
        
    def parseScript(self, filePath):
		_interpreter = TBTAFInterpreter()
		return _interpreter.parseScript(filePath)

    def createTestBed(self, urlList = ['localhost']):
		tBtestBedInstance = TBTestBed()
		isValidUrlList = True
		
		if  isInvalidArgument(urlList):
			print 'Error: TBTAFOrchestrator.createTestBed'
		else:
			for url in urlList:
				if validateUrl(url):
					tBtestBedInstance.addExecutionNode(url)
				else
					isValidUrlList = False
					print 'Invalid Argument exception'
					print 'Error: TBTAFOrchestrator.createTestBed'
					break
				
			if isValidUrlList:
				print 'New test bed created on: ', urlList
				return tBtestBedInstance

	def isInvalidArgument(argument):
		if argument == None or argument == "":
			raise ValueError("Invalid Argument Exception")
			return True
		else:
			return False
			
	def getServerStatusCode(url):
		#https://pythonadventures.wordpress.com/2010/10/17/check-if-url-exists/
		host, path = urlparse.urlparse(url)[1:3]
		try:
			conn = httplib.HTTPConnection(host)
			conn.request('HEAD', path)
			status = conn.getresponse().status
			conn.close()
			return status
		except StandardError:
			#Test this
			conn.close()
			return None
	 
	def validateUrl(url):
		#https://pythonadventures.wordpress.com/2010/10/17/check-if-url-exists/
		good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
		valid = getServerStatusCode(url) in good_codes
		return valid
	
	#filePath - String containing the filepath where the test cases are located.
	#smartFilePath - Optional string containing the filepath where the production source code is located. This would be useful for TBSmartTestSuite creation.
	#tagList - String containing the list of tags which are desired to be executed among the existing test code within the specified location
    def createTestSuite(self, filePath, smartFilePath, tagList):
	
	_discoverer = TBTAFInterpreter()
	testCasesList = _discoverer.LoadTests(filePath)
	
	if
	
	for testCase in testCasesList
		
		
	
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

	#projectName - String describing the project from which the query is being made.
	def GetTags(projectName)
		tagList[]
		testCase in getProject(projectName).tbTestSuiteInstance.getTestCases()
			tagList.append(testCase.getMetadata.getTags)
		return tagList
		#Excepciones
		#If null string is provided as Project ID then an Invalid Argument Exception will be thrown.
	
    def getEventSource(self):
        return self.eventSource