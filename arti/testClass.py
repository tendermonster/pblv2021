import os
import sys

class Test:
    def __init__(self,value):
        self.value = str(value)
    def checkPath(self):
        return os.getcwd()
