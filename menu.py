import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSlot
 
class MainWindow(QDialog):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.title = 'Main Menu'
        self.setWindowIcon(QIcon('icon.png'))
        self.left = 500
        self.top = 500
        self.width = 500
        self.height = 100
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.mainMenu()
 
    def mainMenu(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.mainLayout()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.text)
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
 
    #TODO: intialize variable needs to be set by checking connections and homing controls
    def initialize(self):
        self.text.insertPlainText('Checking Connections and Zeroizing Controls\n')
        initialize = True
        if initialize == True:
            self.testButton.setEnabled(True)
            self.text.insertPlainText('Complete\n')
        else:
            red = QColor(255, 0, 0)
            black = QColor(0, 0, 0)
            self.text.setTextColor(red)
            self.text.insertPlainText('Initialization Failed. Check Connections\n')
            self.text.setTextColor(black)
            
    def testOptions(self):
        self.options = TestWindow()
        self.options.show()
        main.close()

class TestWindow(QDialog):
    def __init__(self, parent = None):
        super(TestWindow, self).__init__(parent)
        self.testTitle = 'Test Menu'
        self.setWindowIcon(QIcon('icon.png'))
        self.left = 500
        self.top = 500
        self.width = 500
        self.height = 100
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.testMenu()

    def testMenu(self):
        self.setWindowTitle(self.testTitle)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.testLayout()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.text)
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
        self.text.insertPlainText('yoyoyo\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
