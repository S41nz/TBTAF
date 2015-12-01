'''
Created on 22/11/2015
@author: @carofermin
Class that indicate whether or not the parsing process was a success, warning or error.
'''
class Result:
    def __init__(self, status, message):
        self.status = status
        self.message = message
