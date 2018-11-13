import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSlot
 
class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon('icon.png'))
        self.left = 500
        self.top = 500
        self.width = 500
        self.height = 250
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.windowLayout = QVBoxLayout()
        self.mainMenu()
 
    def mainMenu(self):
        self.title = 'Main Menu'
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.mainLayout()
 
        
        self.windowLayout.addWidget(self.horizontalGroupBox)
        self.windowLayout.addWidget(self.text)
        self.setLayout(self.windowLayout)
 
        self.show()

    def testMenu(self):
        self.title = 'Test Mode'
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.testLayout()
 
        self.windowLayout.addWidget(self.testGroupBox)
        self.windowLayout.addWidget(self.text)
        self.setLayout(self.windowLayout)

    def mainLayout(self):        
        menuLayout = QHBoxLayout()
        self.horizontalGroupBox = QGroupBox('Simply LED Test Module')    

        self.initializeButton = QPushButton('Initialize', self)
        self.initializeButton.setToolTip('Checks Connections and Homes Controls')
        self.initializeButton.clicked.connect(self.initialize)
        menuLayout.addWidget(self.initializeButton)

        self.testButton = QPushButton('Begin Test',self)
        self.testButton.setToolTip('Test Options')
        self.testButton.clicked.connect(self.testOptions)
        self.testButton.setEnabled(False)
        menuLayout.addWidget(self.testButton)

        self.horizontalGroupBox.setLayout(menuLayout) 

    def testLayout(self):
        testLayout = QHBoxLayout()
        self.testGroupBox = QGroupBox('Select Test Mode')

        testButtonOne = QPushButton('Test 1 text', self)
        testButtonOne.clicked.connect(self.testButtonOne)
        testLayout.addWidget(testButtonOne)

        testButtonTwo = QPushButton('Test 2 text',self)
        testButtonTwo.clicked.connect(self.testButtonTwo)
        testLayout.addWidget(testButtonTwo)

        testButtonThree = QPushButton('Test 3 text')
        testButtonThree.clicked.connect(self.testButtonThree)
        testLayout.addWidget(testButtonThree)

        self.testGroupBox.setLayout(testLayout)
            
    def testButtonOne(self):
        self.text.insertPlainText('I do something\n')

    def testButtonTwo(self):
        self.text.insertPlainText('I do something too\n')

    def testButtonThree(self):
        self.text.insertPlainText('yoyoyo\n')
 
    #TODO: intialize variable needs to be set by checking connections and homing controls (To check fail condition set initialize = False)
    def initialize(self):
        self.text.insertPlainText('Checking Connections and Zeroizing Controls\n')
        initialize = True
        if initialize:
            self.testButton.setEnabled(True)
            self.text.insertPlainText('Complete\n')
        else:
            red = QColor(255, 0, 0)
            black = QColor(0, 0, 0)
            self.text.setTextColor(red)
            self.text.insertPlainText('Initialization Failed. Check Connections\n')
            self.text.setTextColor(black)
            
    def testOptions(self):
        self.testMenu()
        self.horizontalGroupBox.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
