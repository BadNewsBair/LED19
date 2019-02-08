import sys
import numpy as np

class Measurement():
    logger = None
    def __init__(self, mainlog):
        self.logger = mainlog

    def beginTest(self):
        self.logger('testing log output')
