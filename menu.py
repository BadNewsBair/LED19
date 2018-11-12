import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class MainWindow(QDialog):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.title = 'Main Menu'
        self.left = 500
        self.top = 500
        self.width = 500
        self.height = 100
        self.mainMenu()
 
    def mainMenu(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.mainLayout()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
 
        self.show()
 
    def mainLayout(self):
        self.horizontalGroupBox = QGroupBox("Simply LED Test Module")
        layout = QHBoxLayout()

        initializeButton = QPushButton('Initialize', self)
        initializeButton.setToolTip('Checks Connections and Homes Controls')
        initializeButton.clicked.connect(self.initialize)
        layout.addWidget(initializeButton)

        self.testButton = QPushButton('Begin Test',self)
        self.testButton.setToolTip('Test Options')
        self.testButton.clicked.connect(self.testOptions)
        self.testButton.setEnabled(False)
        layout.addWidget(self.testButton)
 
        self.horizontalGroupBox.setLayout(layout)
 
    def initialize(self):
        print('Checking Connections and Zeroizing Controls')
        #TODO: intialize needs to be set by checking connections and homing controls
        initialize = True
        if initialize == True:
            self.testButton.setEnabled(True)
        else:
            print('Initialize Failed. Check Connections')

    def testOptions(self):
        print('Select Test')
        self.options = TestWindow()
        self.options.show()
        main.close()

class TestWindow(QDialog):
    def __init__(self, parent = None):
        super(TestWindow, self).__init__(parent)
        self.testTitle = 'Test Menu'
        self.left = 500
        self.top = 500
        self.width = 500
        self.height = 100
        self.testMenu()

    def testMenu(self):
        self.setWindowTitle(self.testTitle)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.testLayout()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
 
        self.show()
        
    def testLayout(self):
        self.horizontalGroupBox = QGroupBox("Select Test Mode")
        layout = QHBoxLayout()

        testButtonOne = QPushButton('Test 1 text', self)
        testButtonOne.clicked.connect(self.testButtonOne)
        layout.addWidget(testButtonOne)

        testButtonTwo = QPushButton('Test 2 text',self)
        testButtonTwo.clicked.connect(self.testButtonTwo)
        layout.addWidget(testButtonTwo)

        testButtonThree = QPushButton('Test 3 text')
        testButtonThree.clicked.connect(self.testButtonThree)
        layout.addWidget(testButtonThree)
 
        self.horizontalGroupBox.setLayout(layout)

    def testButtonOne(self):
        pass

    def testButtonTwo(self):
        pass

    def testButtonThree(self):
        print('yoyoyo')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
