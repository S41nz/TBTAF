'''
Created on 06/11/2015
'''

import glob
import importlib
import inspect
import logging
import re
import sys
import os
import xml.etree.ElementTree

from common.enums.metadata_type import TBTAFMetadataType
from common.metadata import TBMetadata
from common.test import TBTestCase

class TBTAFDiscoverer():
    '''
    The Discoverer is the module in charge of parsing the TBTAF metadata
    embedded on source code (both test and production) and communicate the
    discovered data to the TBTAF Orchestrator.
    '''
    

    def __init__(self):
        '''
        This class only contains static methods. Therefore no initialization.
        '''
    
    # Currently is very explicit for clarity. Can be made shorter and use less
    #  memory.    
    @staticmethod
    def LoadTests(path):
        '''
        Input:
        ----String specifying the directory where the tests are contained or 
         the complete filepath to a single test.
        Output:
        ----A collection of TBTestCase instances with their corresponding 
         TBMetatadata instances of describing the metadata being discovered on 
         the source code of each test within the provided location.
        Exceptions:
        ----ValueError Exception: If the provided location is either null
         or inaccessible then an Invalid Argument Exception will be thrown.
        Undefined scenarios:
        ----A filename is given which is neither a folder nor a .py file.
         (General result: empty collection)
        
        Process:
        ----(1) Cleans the path given and looks for the .py files
        ----(2) Imports the modules
        ----(3) Gets the first comment in the modules
        ----(4) Parse metadata. Only continue for files which contain metadata:
        ----(4.1) Read all classes from the file
        ----(4.2) Instantiate and load metadata into all TBTestcase inheritors
        ----(4.3) Return a collection of those instances
        '''
        pyFiles = []
        if path is None:
            raise ValueError("Empty path was provided")
        if path.endswith('.py'):
            dirPath = os.path.realpath(os.path.abspath(os.path.dirname(path)))
            filePath = os.path.realpath(os.path.abspath(path))
            if not os.path.exists(filePath):
                raise ValueError("Invalid path was provided")
            pyFiles.append(filePath)
        else:
            dirPath = os.path.realpath(os.path.abspath(path))
            if not os.path.exists(dirPath):
                raise ValueError("Invalid path was provided")
            pyFiles = [f for f in glob.glob(os.path.join(dirPath, '*.py'))]
        if dirPath not in sys.path:
            sys.path.insert(0, dirPath)
        testCollection = []
        testModules = []
        for f in pyFiles:
            moduleName = os.path.basename(f)[:-3]
            if moduleName.startswith('__'): continue
            module = importlib.import_module(moduleName)
            firstComment = inspect.getdoc(module)
            metaData = TBTAFDiscoverer._parseXML(firstComment,f,
                                                 TBTAFMetadataType.TEST_CODE)
            if metaData is not None:
                testClasses = [m for m in 
                               inspect.getmembers(module,inspect.isclass) if 
                               m[1].__module__ == moduleName]
                testModules.append((module,testClasses))
                for className, _ in testClasses:
                    classObj = getattr(module,className)
                    if issubclass(classObj, TBTestCase):
                        classInstance = classObj()
                        classInstance.setTestMetadata(metaData)
                        testCollection.append(classInstance)
        return testCollection
    
    
    @staticmethod
    def LoadCodeMetadata(paths):
        '''
        Inputs:
        ----Collection of strings describing the location of specific
         production source code files.
        Outputs:
        ----A collection of TBMetadata instances describing the metadata being
         discovered on the source code of each test within the provided
          locations.
        Exceptions:
        ----If the provided locations are either null or non-existent then an
         Invalid Argument Exception will be thrown.

        
        Process:
        ----(1) Cleans the path given and looks for the .py files
        ----(2) Imports the modules
        ----(3) Gets the first comment in the modules
        ----(4) Parse metadata. Only continue for files which contain metadata:
        ----(4.1) Read all metadata from the files
        ----(4.2) Return a collection of this metadata
        '''
        if not paths:
            raise ValueError("No paths were provided")
        pyFiles = []
        for p in paths: 
            if p is None:
                raise ValueError("Empty path was provided")
            dirPath = os.path.realpath(os.path.abspath(os.path.dirname(p)))
            filePath = os.path.realpath(os.path.abspath(p))
            if not os.path.exists(filePath):
                raise ValueError("Invalid path was provided")
            if not p.endswith('.py'):
                continue
            pyFiles.append(filePath)
            if dirPath not in sys.path:
                sys.path.insert(0, dirPath)
        codeMetadata = []
        for f in pyFiles:
            moduleName = os.path.basename(f)[:-3]
            module = importlib.import_module(moduleName)
            firstComment = inspect.getdoc(module)
            metaData = TBTAFDiscoverer._parseXML(firstComment,f,
                                                 TBTAFMetadataType.PRODUCT_CODE
                                                 )
            if metaData is not None:
                codeMetadata.append(metaData)
        return codeMetadata

    @staticmethod
    def _parseXML(s,f,t):
        '''
        Inputs:
        ----<s>: String potentially containing the pXML-encoded metadata.
        ----<f>: Filename where said string was obtained from. 
        ----<t>: Metadata type according to caller.
        Outputs:
        ----TBMetadata instance containing the corresponding metadata.
        ------None if no metadata was found or a required field was not found.
        '''
        if s is None:
            logging.info("No metadata (no comment on first line) found in"
                            " file " + f)
            return None
        try:
            e = xml.etree.ElementTree.fromstring(s)
        except xml.etree.ElementTree.ParseError:
            logging.info("No metadata found in file " + f)
            return None
        
        md = TBMetadata(TBTAFMetadataType.PRODUCT_CODE)
        assetID = None
        if t == TBTAFMetadataType.TEST_CODE:
            assetID = e.find("TestID")
            if assetID is None : # Required but not found. Fail gracefully
                logging.info("ID (required) not found in file " + f)
                return None
            md = TBMetadata(TBTAFMetadataType.TEST_CODE)
        else:
            md = TBMetadata(TBTAFMetadataType.PRODUCT_CODE)

        tags = e.find("Tags")
        if tags is None : # Required but not found. Fail gracefully
            logging.info("Tags (required) not found in file " + f)
            return None
        priority = e.find("Priority")
        assetDescription = e.find("Description")
        
        if assetID is not None and assetID.text is not None :
            md.setAssetID(int(assetID.text))
        else:
            md.setAssetID(None)
        if tags.text is not None :
            md.setTags(re.split(', ',tags.text))
        else:
            md.setTags(None)
        if priority is not None and priority.text is not None:
            md.setPriority(int(priority.text))
        else:
            md.setPriority(None)
        if assetDescription is not None and assetDescription.text is not None:
            md.setAssetDescription(assetDescription.text)
        else:
            md.setAssetDescription(None)
        return md
        
if __name__ == '__main__':
    # Any path style works! Woohoo!
    testCollection = TBTAFDiscoverer.LoadTests(r'./\\\\\samples/\//')
    for i in testCollection:
        print i.getTestMetadata().getAssetDescription()
        i.setup()
        i.execute()
        i.cleanup()
    codeMetaDataCollection = TBTAFDiscoverer.LoadCodeMetadata([r'.\samples\testCompleteAndValid.py'])
    for md in codeMetaDataCollection:
        print md.getTags()
    