'''
S41nz 		05/07/2023	Corrected the hardcoding to enable the Oracle Databridge by default 
Created on 02/11/2015

@author: 
'''

from __future__ import absolute_import
from __future__ import print_function
import six.moves.http_client
import os
import six.moves.urllib.parse
import subprocess
import time
import platform

from common.test_bed import TBTestBed
from common.project import TBProject
from common.node import TBTestNode
from common.suite import TBTestSuite
from common.smart_suite import TBSmartTestSuite

from common.enums.suite_type import TBTAFTestSuiteType
from common.enums.filter_type import TBTAFFilterType
from common.enums.execution_status_type import TBTAFExecutionStatusType

from interpreter.TBTAFInterpreter import TBTAFInterpreter
from discoverer.discoverer import TBTAFDiscoverer
from publisher.TBTAFPublisher import TBTAFPublisher
from executor.Executor import TBTAFExecutor
from databridge.TBTAFDataBridge import TBTAFDatabridge

class TBTAFOrchestrator(object):
	
	INVALID_ARGUMENT_EXCEPTION_TEXT = 'Invalid Argument Exception'
	
	def __init__(self, nameInitizalizationFile = None,targetDatabridge = None):
		_databridge = targetDatabridge
		if _databridge is not None:
			_databridge.connect()
		if nameInitizalizationFile is None:
			self.projectList = []
		else:
			if not self.isInvalidFile(nameInitizalizationFile):
				self.projectList = []
			else:
				print('Error: TBTAFOrchestrator.__init__')

	def addProject(self, newProject):
		self.projectList.append(newProject)
	
	def createNewProject(self, tBTestSuiteInstance, tBTestBedInstance, projectName):
		#Revisar si es la forma pythonesca y si funcionan.
		if self.isInvalidArgument(tBTestSuiteInstance) or self.isInvalidArgument(tBTestBedInstance) or self.isInvalidArgument(projectName):
			print('Error: TBTAFOrchestrator.createNewProject')
		else:
			if projectName in [projectInstance.projectName for projectInstance in self.projectList]:
				raise ValueError("Already Existing Project Exception")
			else:
				project =  TBProject(tBTestSuiteInstance, tBTestBedInstance, projectName)
				self.addProject(project) 
				#Agregar mensajes de confirmacion en linea de comandos
				print('New project created: ', projectName)
				#Duda: Si es un Smart Test Suite, hay que poner todos? porque no se reciben etiquetas como parametro, solo el TBTestSuiteInstance
				#Duda: Que pasa si llamamos a gestTestCases() para un smart suite... se corre el de TBTestSuite o de TBSmartTestSuite?
				print('Number of tests: ', len(tBTestSuiteInstance.getTestCases())) 
				print('Execution nodes: ', ', '.join([testNode.getNodeURL() for testNode in tBTestBedInstance.getTestBedNodes()]))

	def parseScript(self, filePath):
		_interpreter = TBTAFInterpreter()
		_interpreter.setOrchestratorReference(self)
		return _interpreter.parseScript(filePath)
    
	def createTestBed(self, urlList = ['127.0.0.1']):
		tBtestBedInstance = TBTestBed()
		isValidUrlList = True
		
		if  self.isInvalidArgument(urlList):
			print('Error: TBTAFOrchestrator.createTestBed')
		else:
			for url in urlList:
				if self.validateUrl(url):
					tBtestBedInstance.addExecutionNode(url)
				else:
					isValidUrlList = False
					print('Error: TBTAFOrchestrator.createTestBed')
					break
				
			if isValidUrlList:
				print('New test bed created on: ', urlList)
				return tBtestBedInstance
			else:
				return
	
	#filePath - String containing the filepath where the test cases are located.
	#tagList - Optional String containing the list of tags which are desired to be executed among the existing test code within the specified location.
	def createTestSuite(self, filePath, tagList = None):	
		if self.isInvalidPath(filePath):
			print('filePath')
			print('Error: TBTAFOrchestrator.createTestSuite')
		else:
			_discoverer = TBTAFDiscoverer()
			testCaseList = _discoverer.LoadTests(filePath)
			testSuiteID = 'testSuiteID_01'
			
			if tagList is None:
				_testSuite = TBTestSuite(TBTAFTestSuiteType.NORMAL, testSuiteID)
				_testSuite.addTestCaseList(testCaseList)
				
				print('Test ', testSuiteID, ' loaded from: ', filePath)
				print('Test suite created with ', len(_testSuite.getTestCases()), ' test cases')
				return _testSuite
			else:
				if self.isInvalidList(tagList):
					print('tagList')
					print('Error: TBTAFOrchestrator.createTestSuite')
					return 
				else:
					_smartTestSuite = TBSmartTestSuite(testSuiteID)
					_smartTestSuite.addTestCaseList(testCaseList)
					
					filteredTestCases = _smartTestSuite.getTestCasesByTags(tagList, TBTAFFilterType.IN)
					_smartTestSuite.clearTestCaseList()
					_smartTestSuite.addTestCaseList(filteredTestCases)
					
					print('Test ', testSuiteID, ' loaded from: ', filePath)
					print('Smart test suite created with ', len(_smartTestSuite.getTestCases()), ' test cases')								
					return _smartTestSuite	
	
	#tbTestSuiteInstance - Reference to a given TBTestSuite instance from which the test plan will be generated.
	#testPlanLocation - String specifying the location where the test plan wants to be placed.
	#outputFormat - Enumeration flag specifying the output format of the created test plan.

	def publishTestPlan(self, tbTestSuiteInstance, testPlanLocation, outputFormat = 'html'):
		#_publisher = TBTAFPublisher()
		TBTAFPublisher().PublishTestPlan(tbTestSuiteInstance, testPlanLocation, outputFormat)
		print('Test plan published at: ', testPlanLocation)

	#tbTestSuiteInstance - Reference to a given TBTestSuite instance from which the result report will be generated.
	#resultLocation - String specifying the location where the result report wants to be placed.
	#outputFormat - Enumeration flag specifying the output format of the created result report.

	def publishResultReport(self, tbTestSuiteInstance, resultLocation, outputFormat = 'html'):
		TBTAFPublisher().PublishResultReport(tbTestSuiteInstance, resultLocation, outputFormat)
		print('Test result created at: ', resultLocation)

	#tbTestSuiteInstance - Reference to a given TBTestSuite instance which will be inserted

	def storeResultReport(self, tbTestSuiteInstance):
		if self._databridge is not None:
			id = self._databridge.storeResult(tbTestSuiteInstance)
			print('Testsuite result stored with id: ', id)


	#tbTestSuiteInstance - Reference to a given TBTestSuite instance from which the result report will be generated.
	#resultLocation - String specifying the location where the result report wants to be placed.
	#outputFormat - Enumeration flag specifying the output format of the created result report.

	def getResultReport(self, suiteId, resultLocation, outputFormat = 'html'):
		TBTAFPublisher().PublishResultReport(self._databridge.getTestResultBySuiteId(suiteId), resultLocation, outputFormat)
		print('Test result created at: ', resultLocation)
		

		#tbTestSuiteInstance - Reference to a given TBTestSuite instance from which the result report will be generated.
        #tbTestSuiteInstance - Reference of the TBTestSuite representing the set of tests that will be executed.
        #urlCollection - Optional collection of URLs corresponding to the nodes on which the test execution will be distributed.
        #flagsCollection - Optional collection of flags that can customize the execution of such TBTestSuite.
        #executorListenerCollection - Optional collection of ExecutorListener implementations that would want to listen and react to specific events during the execution of that specific TBTestSuite
	def executeTestSuite(self, tbTestSuiteInstance, testBed = "dummy", flagsCollection = [], executorListenerCollection = []):
		#tbtafExecutorInstance = TBTAFExecutor()
		_executor = TBTAFExecutor()
		suiteResult = _executor.executeTests(tbTestSuiteInstance, testBed, flagsCollection, executorListenerCollection)

		waitingComplete = True
		while waitingComplete:
			result = _executor.getStatus(tbTestSuiteInstance)
			time.sleep(5)
			waitingComplete = result.getExecutionStatusType() != TBTAFExecutionStatusType.COMPLETED
		
		#return suiteResult
		#Si esto no funciona, el executor tiene que poner un metodo llamado getSuiteResult que devuelva getSuiteResult.
		return tbTestSuiteInstance.getSuiteResult()
	
        #projectName - String identifying the Project from where the query is being made.
        #tagList - Optional List of tags in order to filter the query being made.
        #indicatorEnumeration - If the list of tags is provided, then an additional enumeration can be passed in order to specify if the tags will be used to filter IN or OUT the results found.	
	def getTests(self, projectName, tagList = [], filterType = None):
		#If the parameters being passed are null or contain null then an Invalid Argument Exception will be thrown.
		#If the provided Project key does not exist on the currently connected datasource, then a Not Existing Project Exception will be thrown.
		#If the provided filtering enumeration is provided, then a Not Supported Filter Exception will be thrown. -- What's this?
		if self.isInvalidArgument(projectName):
			print('Error: TBTAFOrchestrator.GetTests')
		elif not self.isExistingProject(projectName):
			print('Error: TBTAFOrchestrator.GetTests')
		elif self.isInvalidList(tagList):
			print('Error: TBTAFOrchestrator.GetTests')
		#I think this is what Pablo means in the iii. exception description. 
		#Do I need to use the TBTAFFilterType.IN or TBTAFFilterType.OUT values?
		elif not self.isSupportedFilter(filterType):
			print('Error: TBTAFOrchestrator.GetTests')
		else:
			#Get TBProject object related to our projectName
			projectInstance = next((project for project in self.projectList if project.projectName == projectName), None)
			#Get TBTestSuite object for our projectInstance
			tbTestSuite = projectInstance.getTBTestSuite()
			#vale la pena agregar excepcion si se provee lista de tags y el proyecto tiene un TBTestSuite y no smart?
			#si el proyecto tiene ligado un TBTestSuite, como puedo usar getTestCases() de TBSmartTestSuite para filtrar por Tag. En caso que siguiente exception no deba levantarse.
			if tbTestSuite.getTestSuiteType() == TBTAFTestSuiteType.NORMAL and len(tagList):
				raise ValueError("Normal TBTestSuite not compatible with Tag list Exception")
				print('Error: TBTAFOrchestrator.GetTests')
			else:
				#Check what type of Test Suite that project has and action accordingly
				#Get initial list of test cases. This depends on what type of TBTestSuite we have. 
				#Al parecer la lista de tags es para filtar que test cases quieres obtener del total del proyecto. 
				if tbTestSuite.getTestSuiteType() == TBTAFTestSuiteType.NORMAL or not len(tagList):
					queriedTests = tbTestSuite.getTestCases()
				else:
					#Do I need to append list each time I get from getTestCases?
					#Should we suggest getting a list in getTestCases() for inOutList (list of filterType)
					if filterType is not None:
						queriedTests = tbTestSuite.getTestCasesByTags(tagList, filterType)
					else:
						queriedTests = tbTestSuite.getTestCasesByTags(tagList) #Asi se pueden omitir parametros opcionales? Y si mejor le pongo el filterType siempre?
				#Duda: En el diccionario, debo tener un tag por cada tag del proyecto, aunque este filtrado por el parametro de tagList? O, si es filtrado, lo saco del diccionario.
				tagDictionary = self.getTags(projectName, 'N')
				#Create empty dictionary
				# Empty dict
				d = {}
				for tag in tagDictionary:
					d[tag] = self.getTestsForTag(queriedTests, tag)
				for tagkey, testIds in d.items(): #CHANGE testIds
					print(tagkey, ': ', ', '.join(str(x) for x in testIds))
				return d  
				
	def getTestsForTag(self, testList, tag): 
		'''
		Method to obtain the tests that contain the tag from the input
		'''
		dataSet = testList
		resultTestCases = []
		#Check if the base data set is not None
		if dataSet is not None:
			for candidateTest in dataSet:
				#Fetch the test metadata
				testMetadata = candidateTest.getTestMetadata()
				if testMetadata is not None:
					testTags = testMetadata.getTags()
					if tag in testTags and testMetadata.getAssetID() not in resultTestCases: #Should I verify for repeated asset ids in case the header of distinct test cases have exact same asset id values like -1?
						resultTestCases.append(testMetadata.getAssetID()) #CHANGE testMetadata.getAssetID().					
		return resultTestCases

	#projectName - String describing the project from which the query is being made.
	def getTags(self, projectName, printFlag = 'Y'):
		if self.isInvalidArgument(projectName):
			print('Error: TBTAFOrchestrator.GetTags')
		elif not self.isExistingProject(projectName):
			print('Error: TBTAFOrchestrator.GetTags')
		else:
			tagList = []
			projectInstance = next((project for project in self.projectList if project.projectName == projectName), None)
			tbTestSuiteInstance = projectInstance.getTBTestSuite()
			testCases = tbTestSuiteInstance.getTestCases()
			for testCase in testCases:
				testMetadata = testCase.getTestMetadata()
				if testMetadata is not None:
					testTags = testMetadata.getTags()
					for tag in testTags:
						if tag not in tagList:
							tagList.append(tag)
			if printFlag == 'Y':
				print('Tags: ', ', '.join(tagList))
			return tagList
		
	#Validations
	
	def isInvalidArgument(self, argument):
		if argument == None or argument == "":
			raise ValueError(self.INVALID_ARGUMENT_EXCEPTION_TEXT)
			return True
		return False
			
	def isInvalidList(self, list):
		if not all(list):
			raise ValueError(self.INVALID_ARGUMENT_EXCEPTION_TEXT)
			return True
		return False
		
	def isInvalidPath(self, path):
		if not os.path.exists(path):
			raise ValueError(self.INVALID_ARGUMENT_EXCEPTION_TEXT)
			return True
		return False
		
	def isInvalidFile(self, fileName):
		if not os.path.isfile(fileName):
			print('Invalid file: ', fileName)
			raise ValueError(self.INVALID_ARGUMENT_EXCEPTION_TEXT)
			return True
		return False
		
	def isSupportedFilter(self, filterType):
		if (filterType == TBTAFFilterType.IN or filterType == TBTAFFilterType.OUT or filterType is None):
			return True
		raise ValueError("Not Supported Filter Exception")
		return False

	def isExistingProject(self, projectName):
		if projectName in [projectInstance.projectName for projectInstance in self.projectList]:
			return True
		raise ValueError("Not Existing Project Exception")
		return False

	def validateUrl(self, url):
		DEVNULL = open(os.devnull, 'w')
		os_name = platform.system()
		base_command = ''
		if os_name == 'Darwin':
			base_command = 'ping -c 1 '
		else :
			base_command = 'ping -n 1 '
		response = subprocess.call(base_command + url, stdout = DEVNULL, stderr = DEVNULL, shell=True)
		valid = response == 0
		if not valid:
			print('Invalid URL:', url)
			raise ValueError(self.INVALID_ARGUMENT_EXCEPTION_TEXT)
		return valid
