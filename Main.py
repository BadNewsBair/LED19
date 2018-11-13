import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap

 
class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon('icon.png'))
        self.left = 500
        self.top = 200
        self.width = 1000
        self.height = 500
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
        
        self.setLayout(self.windowLayout)
 
        self.show()

    def testMenu(self):
        self.title = 'Test Menu'
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.testLayout()
 
        self.windowLayout.addWidget(self.testGroupBox)
        self.windowLayout.addWidget(self.text)
        self.setLayout(self.windowLayout)

    def mainLayout(self):        
        menuLayout = QVBoxLayout()
        picLayout = QVBoxLayout()

        self.horizontalGroupBox = QGroupBox('LED Test Module')    

        self.initializeButton = QPushButton('Initialize', self)
        self.initializeButton.setToolTip('Checks Connections and Homes Controls')
        self.initializeButton.clicked.connect(self.initialize)
        menuLayout.addWidget(self.initializeButton)

        self.testButton = QPushButton('Begin Test',self)
        self.testButton.setToolTip('Test Options')
        self.testButton.clicked.connect(self.testOptions)
        self.testButton.setEnabled(False)
        menuLayout.addWidget(self.testButton)

        menuLayout.addWidget(self.text)

        image = QPixmap('testDevice.jpg')
        lbl = QLabel(self)
        lbl.setPixmap(image)
        picLayout.addWidget(lbl)     

        fullLayout = QHBoxLayout()
        fullLayout.addLayout(menuLayout)
        fullLayout.addLayout(picLayout)

        self.horizontalGroupBox.setLayout(fullLayout) 

    def testLayout(self):
        testLayout = QHBoxLayout()
        self.testGroupBox = QGroupBox('Select Test Mode')

        testButtonOne = QPushButton('Type 5', self)
        testButtonOne.setToolTip('0 - 90 in 5 degree increments')
        testButtonOne.clicked.connect(self.testButtonOne)
        testLayout.addWidget(testButtonOne)

        testButtonTwo = QPushButton('Type 2-4',self)
        testButtonTwo.setToolTip('0 - 180 in 5 degree increments')
        testButtonTwo.clicked.connect(self.testButtonTwo)
        testLayout.addWidget(testButtonTwo)

        testButtonThree = QPushButton('Arbitrary Complete')
        testButtonThree.setToolTip('0 - 355 in 5 degree increments')
        testButtonThree.clicked.connect(self.testButtonThree)
        testLayout.addWidget(testButtonThree)

        self.testGroupBox.setLayout(testLayout)

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
            
    def testButtonOne(self):
        self.test = TestWindow(1)
        self.test.show()
        main.close()

    def testButtonTwo(self):
        self.test = TestWindow(2)
        self.test.show()
        main.close()

    def testButtonThree(self):
        self.test = TestWindow(3)
        self.test.show()
        main.close()

class TestWindow(QDialog):
    def __init__(self, testType, parent = None):
        super(TestWindow, self).__init__(parent)
        self.testTitle = 'Test Progress'
        self.testType = testType
        self.left = 500
        self.top = 200
        self.width = 1000
        self.height = 1000
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
        if self.testType == 1:
            testTitle = 'Type 5 Light Test'
            self.text.insertPlainText('Start test to begin Type 5 Test(0-90 in 5 degree increments)\n')
        elif self.testType ==2:
            testTitle = 'Type 2-4 Light Test'
            self.text.insertPlainText('Start test to begin Type 2-4 Test(0-180 in 5 degree increments)\n')
        elif self.testType ==3:
            testTitle = 'Arbitrary Complete Test'
            self.text.insertPlainText('Start test to begin Arbitrary Complete Test(0-355 in 5 degree increments)\n')

        self.horizontalGroupBox = QGroupBox(testTitle)
        layout = QHBoxLayout()

        self.startButton = QPushButton('Start', self)
        self.startButton.setToolTip('Begin Test')
        self.startButton.clicked.connect(self.start)
        layout.addWidget(self.startButton)

        self.pauseButton = QPushButton('Pause Test',self)
        self.pauseButton.setToolTip('Pause Test in Progress')
        self.pauseButton.clicked.connect(self.pause)
        self.pauseButton.setEnabled(False)
        layout.addWidget(self.pauseButton)

        self.continueButton = QPushButton('Continue Test', self)
        self.continueButton.setToolTip('Continue Test in Progress')
        self.continueButton.clicked.connect(self.continueTest)
        layout.addWidget(self.continueButton)
        self.continueButton.hide()

        self.saveButton = QPushButton('Save Data', self)
        self.saveButton.setToolTip('Opens File Directory')
        self.saveButton.clicked.connect(self.saveFile)
        self.saveButton.setEnabled(False)
        layout.addWidget(self.saveButton)

        self.horizontalGroupBox.setLayout(layout)
    def start(self):
        self.pauseButton.setEnabled(True)
        self.startButton.setEnabled(False)
        self.text.insertPlainText('Test Start\n')
    
    def pause(self):
        self.pauseButton.hide()
        self.continueButton.show()
        self.text.insertPlainText('Test Paused\n')

    def continueTest(self):
        self.continueButton.hide()
        self.pauseButton.show()
        self.text.insertPlainText('Test Continued\n')

    def saveFile(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
