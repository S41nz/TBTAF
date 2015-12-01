'''
Created on 22/11/2015
@author: @carofermin
'''

class TBTAFParsingScriptStatus(object):
    '''
    Simple enumeration class that describes the status of the parsing process.
    '''
    #Status enumeration types
    
    #Parsing complete
    SUCCESS="Success"
    #Parsing complete but warnings have been found.
    WARNING="Warning"
    #Couldn't complete parsing. An error was found. 
    ERROR="Error"