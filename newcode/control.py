import sys
import time
                                           
class MotorControl():
    logger = None
    def __init__(self, mainlog):
        self.logger = mainlog

    def initializeControls(self):
        #TODO: Fix this function, currently returns boolean for testing
        self.logger('Test initialize')
        return True

    def checkConnection(self):
        #TODO: Fix, boolean return is for testing purposes
        self.logger('Test connection')
        return True

    def lowerMotor(self, direction):
        pass

    def upperMotor(self, direction):
        pass


