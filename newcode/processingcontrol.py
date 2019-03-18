import sys
import time

class Measurement():
    isPaused = False   

    def __init__(self, mainlog):
        super().__init__()
        self.logger = mainlog
        
    def beginTest(self):
        iteration = 1
        while iteration < 100:
            if self.isPaused:
                pass
            else:
                self.logger('Iteration %s' % iteration)
                time.sleep(0.1)
                iteration += 1
                
class MotorControl():
    def __init__(self, mainlog):
        self.logger = mainlog

    def initializeControls(self):
        #TODO: Fix this function, currently returns boolean for testing
        self.logger('Homing Motors')
        return True

    def checkConnection(self):
        #TODO: Fix, boolean return is for testing purposes
        self.logger('Test connection')
        return True

    def lowerMotor(self, direction):
        pass

    def upperMotor(self, direction):
        pass