import sys
import time

class Measurement():
    isPaused = False   

    def __init__(self, mainlog, wattage, distance, fileName):
        super().__init__()
        self.log = mainlog
        self.wattage = wattage
        self.distance = distance
        self.fileName = fileName
        
    def beginTest(self):
        iteration = 1
        while iteration < 100:
            if self.isPaused:
                pass
            else:
                self.log('Iteration %s' % iteration)
                time.sleep(0.1)
                iteration += 1
                
class MotorControl():
    def __init__(self, mainlog):
        self.log = mainlog

    def initializeControls(self):
        #TODO: Fix this function, currently returns boolean for testing
        self.log('Homing Motors')
        return True

    def checkConnection(self):
        #TODO: Fix, boolean return is for testing purposes
        self.log('Test connection')
        return True

    def lowerMotor(self, direction):
        pass

    def upperMotor(self, direction):
        pass