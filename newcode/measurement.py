import sys
import time

class Measurement():
    logger = None
    isPaused = False
    app = None

    def __init__(self, mainlog, app):
        super().__init__()
        self.logger = mainlog
        self.app = app

    def beginTest(self):
        self.logger('testing log output')
        iteration = 1
        while iteration < 200:
            if self.isPaused:
                pass
            else:
                self.app.processEvents()
                self.logger('Iteration %s' % iteration)
                time.sleep(0.1)
                iteration += 1

    def pauseTest(self, pauseToggle):
        self.pause = pauseToggle
        while self.pause:
            time.sleep(.1)
            break