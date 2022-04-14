from __future__ import absolute_import
import os
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator
import unittest

class TBTAFOrchestrator_UnitTests(unittest.TestCase):

	def test_createTestBed(self):
		with self.assertRaises(ValueError):
			TBTAFOrchestrator().createTestBed(["InvalidPath"])
	
	def test_createTestSuite(self):
		with self.assertRaises(ValueError):
			TBTAFOrchestrator().createTestSuite("InvalidPath")
			
	def test_createNewProject(self):
		with self.assertRaises(ValueError):
			TBTAFOrchestrator().createNewProject("", "", "")
			
	def test_getTags(self):
		orchestrator = TBTAFOrchestrator()
		testBed = orchestrator.createTestBed()
		testSuite1 = orchestrator.createTestSuite("C:\\Users\\frgutier\\OneDrive\\Maestria MCC\\Pruebas de Software y Calidad Gerardo Padilla\\Proyecto Final\\GIT Repo\\TBTAF\\tbtaf\\test\\discoverer\\samples")
		testSuite2 = orchestrator.createTestSuite("C:\\Users\\frgutier\\OneDrive\\Maestria MCC\\Pruebas de Software y Calidad Gerardo Padilla\\Proyecto Final\\GIT Repo\\TBTAF\\tbtaf\\test\\discoverer\\samples", ["TBTAF"])
		testSuite3 = orchestrator.createTestSuite("C:\\Users\\frgutier\\OneDrive\\Maestria MCC\\Pruebas de Software y Calidad Gerardo Padilla\\Proyecto Final\\GIT Repo\\TBTAF\\tbtaf\\test\\discoverer\\samples", ["Dummy"])
		#1
		project1 = orchestrator.createNewProject(testSuite1, testBed, 'Prueba1')
		ltest1 = ['TBTAF', 'Discoverer', 'Textbook']
		self.assertTrue(set(ltest1) == set(orchestrator.getTags('Prueba1')))
		#2
		project2 = orchestrator.createNewProject(testSuite2, testBed, 'Prueba2')
		ltest2 = ['TBTAF', 'Textbook', 'Discoverer']
		self.assertTrue(set(ltest2) == set(orchestrator.getTags('Prueba2')))
		#3
		project3 = orchestrator.createNewProject(testSuite3, testBed, 'Prueba3')
		ltest3 = []
		self.assertTrue(ltest3 == orchestrator.getTags('Prueba3'))
		#self.assertRaises(ValueError, orchestrator.getTags('Prueba8'))

	def test_getTests(self):
		orchestrator = TBTAFOrchestrator()
		testBed = orchestrator.createTestBed()
		testSuite1 = orchestrator.createTestSuite("C:\\Users\\frgutier\\OneDrive\\Maestria MCC\\Pruebas de Software y Calidad Gerardo Padilla\\Proyecto Final\\GIT Repo\\TBTAF\\tbtaf\\test\\discoverer\\samples")
		testSuite2 = orchestrator.createTestSuite("C:\\Users\\frgutier\\OneDrive\\Maestria MCC\\Pruebas de Software y Calidad Gerardo Padilla\\Proyecto Final\\GIT Repo\\TBTAF\\tbtaf\\test\\discoverer\\samples", ["TBTAF"])
		testSuite3 = orchestrator.createTestSuite("C:\\Users\\frgutier\\OneDrive\\Maestria MCC\\Pruebas de Software y Calidad Gerardo Padilla\\Proyecto Final\\GIT Repo\\TBTAF\\tbtaf\\test\\discoverer\\samples", ["Dummy"])
		#1
		project1 = orchestrator.createNewProject(testSuite1, testBed, 'Prueba1')
		dtest1 = {'TBTAF': [2021],'Textbook':[2021],'Discoverer':[2021]}
		self.assertTrue(dtest1 == orchestrator.getTests('Prueba1'))
		#2
		project2 = orchestrator.createNewProject(testSuite2, testBed, 'Prueba2')
		dtest2 = {'TBTAF': [2021],'Textbook':[2021],'Discoverer':[2021]}
		dtest3 = {'TBTAF': [],'Textbook':[],'Discoverer':[]}
		self.assertTrue(dtest2 == orchestrator.getTests('Prueba2', ["TBTAF"]))
		self.assertTrue(dtest2 == orchestrator.getTests('Prueba2', ["TBTAF"], TBTAFFilterType.IN))
		self.assertTrue(dtest2 == orchestrator.getTests('Prueba2', ["TBTAF", "Discoverer", "Dummy"], TBTAFFilterType.IN))
		self.assertTrue(dtest2 == orchestrator.getTests('Prueba2', ["Dummy"], TBTAFFilterType.OUT))
		self.assertTrue(dtest3 == orchestrator.getTests('Prueba2', ["Textbook"], TBTAFFilterType.OUT))
		#3
		project3 = orchestrator.createNewProject(testSuite3, testBed, 'Prueba3')
		dtest4 = {}
		self.assertTrue(dtest4 == orchestrator.getTests('Prueba3'))
		self.assertTrue(dtest4 == orchestrator.getTests('Prueba3', ["TBTAF"]))
		
	def test_isInvalidArgument(self):
		'''
		Method for testing expected results in isInvalidArgument.
		'''
		with self.assertRaises(ValueError):
			TBTAFOrchestrator().isInvalidArgument("")
		with self.assertRaises(ValueError):
			TBTAFOrchestrator().isInvalidArgument(None)			
		self.assertEqual(False,TBTAFOrchestrator().isInvalidArgument("Prueba"))
	
	def test_isInvalidList(self):
		'''
		Method for testing expected results in test_isInvalidList.
		'''
		self.assertEqual(False,TBTAFOrchestrator().isInvalidList([1,2,3]))
		self.assertEqual(False,TBTAFOrchestrator().isInvalidList([]))
		with self.assertRaises(ValueError):
			TBTAFOrchestrator().isInvalidList([1,2,None,3])
		
	def test_isInvalidPath(self):
		#self.assertEqual(True,TBTAFOrchestrator().isInvalidPath(""))
		#self.assertEqual(True,TBTAFOrchestrator().isInvalidPath("Prueba"))
		with self.assertRaises(ValueError):
			TBTAFOrchestrator().isInvalidPath("")
		with self.assertRaises(ValueError):
			TBTAFOrchestrator().isInvalidPath("Prueba")	
		self.assertEqual(False,TBTAFOrchestrator().isInvalidPath("C:\Users\ifariar"))	
	
	def test_isInvalidFile(self):
		with self.assertRaises(ValueError):
			TBTAFOrchestrator().isInvalidFile("")

unittest.main()