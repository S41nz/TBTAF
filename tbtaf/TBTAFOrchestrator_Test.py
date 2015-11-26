'''
Created on 02/11/2015

@author: S41nz
'''
import os
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator
#from TBTAFOrchestrator import TBTAFOrchestrator

_orchestrator = TBTAFOrchestrator()
_testBed = _orchestrator.createTestBed()
#orchestrator.createTestBed(['http://localhosti/','http://localhosta/'])
_testSuite = _orchestrator.createTestSuite(r'./\\\\\samples/\//')
_orchestrator.createNewProject(_testSuite, _testBed, 'projectName_01')
#solo carga 6 testcases y hay 8 archivos

#_orchestrator.publishTestPlan(_testSuite, "x", "x")
#_orchestrator.publishResultReport(_testSuite, "result_report.html", "html")

#_orchestrator.executeTestSuite(_testSuite, _testBed)
#Cambiar el nombre a executeTests para que sea consistente con el Executor
#El testBed es opcional?

#_orchestrator.getTests('projectName_01')
#_orchestrator.getTags('projectName_01')


#orchestrator.runUnitTests()