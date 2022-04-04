'''
Created on 06/11/2015
'''

from __future__ import absolute_import
import glob
import importlib
import inspect
import logging
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
        testCollection = []
        testModules = []
        pyFiles = TBTAFDiscoverer._findPyFiles(path,True)
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
    def LoadCodeMetadata(path):
        '''
        Inputs:
        ----String specifying the directory where specific production source
         code files are contained or the complete filepath to a single file.
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
        if not path:
            raise ValueError("No path was provided")
        pyFiles = TBTAFDiscoverer._findPyFiles(path,False)
        codeMetadata = []
        for f in pyFiles:
            firstComment = TBTAFDiscoverer._readFirstMultilineComment(f)
            metaData = TBTAFDiscoverer._parseXML(firstComment,f,
                                                 TBTAFMetadataType.PRODUCT_CODE
                                                 )
            if metaData is not None:
                codeMetadata.append(metaData)
        return codeMetadata

    @staticmethod
    def _findPyFiles(path,add_to_sys_path=False):
        '''
        Inputs:
        ----<path>: String with path to single .py file or to folder containing
         .py files.
        ----[add_to_sys_path]: Boolean determining whether of nor to add the
         corresponding path to sys.path (i.e. modules will be imported or not).
        Outputs:
        ----List of found files with their full, normalized paths.
        Notes:
        ----Currently is not recursive.
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
        if add_to_sys_path and dirPath not in sys.path:
            sys.path.insert(0, dirPath)
        return pyFiles

    @staticmethod
    def _parseXML(s,f,t):
        '''
        Inputs:
        ----<s>: String potentially containing the pXML-encoded metadata.
        ----<f>: Filename where said string was obtained from. 
        ----<t>: Metadata type according to caller.
        Outputs:
        ----TBMetadata instance containing the corresponding metadata.
        ------None if no metadata was found or a required field was empty or
              not found.

        Process:
        ----(1) Loads XML data from string. May return with None.
        ----(2) Based on the current specifications [1] do:
        ----(2.1) Get metadata
        ----(2.2) Confirm required info
        ----(2.3) Fill TBMetadata instance, 
        ----(2.3*) Assign the corresponding uninitialized value for empty tags.
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
        
        assetID = e.find("TestID")
        tags = e.find("Tags")
        priority = e.find("Priority")
        assetDescription = e.find("Description")
        
        if t == TBTAFMetadataType.TEST_CODE:
            if assetID is None or assetID.text is None :
                logging.info("ID (required) not found in file " + f)
                return None
            md = TBMetadata(TBTAFMetadataType.TEST_CODE)
        else:
            md = TBMetadata(TBTAFMetadataType.PRODUCT_CODE)
        if tags is None or tags.text is None :
            logging.info("Tags (required) not found in file " + f)
            return None
        
        if assetID is not None and assetID.text is not None :
            md.setAssetID(int(assetID.text))
        else:
            md.setAssetID(TBMetadata.NON_INITIALIZED)
        if tags.text is not None :
            md.setTags([t.strip() for t in tags.text.split(',')])
        else:
            md.setTags([])
        if priority is not None and priority.text is not None:
            md.setPriority(int(priority.text))
        else:
            md.setPriority(TBMetadata.NON_INITIALIZED)
        if assetDescription is not None and assetDescription.text is not None:
            md.setAssetDescription(assetDescription.text)
        else:
            md.setAssetDescription('')
        return md
    
    @staticmethod
    def _readFirstMultilineComment(path):
        '''
        Inputs:
        ----<path>: Filepath from where the comment will be read.
        Outputs:
        ----Multiline comment (i.e. three apostrophes) found on first line, or
         on second line if first line starts with a she-bang (i.e. #!).
         Excludes the comment symbols.
        Notes:
        ----The she-bang on the first line must be accepted because it's 
         potentially necessary for users, and the O.S. has priority and doesn't
         forgive.
        '''
        textInComment = ''
        with open(path) as f:
            in_comment = False
            ln = 1
            for line in f:
                clean_line = line.strip()
                if ln == 1 and clean_line.startswith("#!"):
                    continue
                elif ((ln == 1 or ln == 2)
                      and not in_comment
                      and clean_line.startswith("'''")):
                    closing_pos = clean_line.find("'''",3)
                    in_comment = True
                    if closing_pos != -1:
                        textInComment += clean_line[3:closing_pos]
                        break
                    else:
                        textInComment += clean_line[3:]
                elif in_comment:
                    closing_pos = clean_line.find("'''")
                    if closing_pos != -1:
                        textInComment += clean_line[:closing_pos]
                        break
                    else:
                        textInComment += clean_line
                elif ln > 2:
                    textInComment = ''
                    logging.warning("File ignored. No metadata found in file" +
                                 f.name)
                    break
                ln += 1
        return textInComment
