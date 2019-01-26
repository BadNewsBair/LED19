import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon('icon.png'))
        self.left = 500
        self.top = 200
        self.width = 1200
        self.height = 800
        self.red = QColor(255, 0, 0)
        self.black = QColor(0, 0, 0)
        self.font = QFont()
        self.font.setPointSize(12)

        self.initButton = self.initializeButton()
        self.comboLabel = self.comboBoxLabel()
        self.combo = self.comboBox()
        self.startButton = self.startTestButton()
        self.textInput = self.wattageInput()
        self.textOutput = self.outputText()
        
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

    def mainLayout(self): 
        menuLayout = QVBoxLayout()
        gridLayout = QGridLayout()
        picLayout = QVBoxLayout()

        self.horizontalGroupBox = QGroupBox('LED Test Module')
        
        menuLayout.addWidget(self.initButton)
        menuLayout.addLayout(gridLayout)
        gridLayout.addWidget(self.comboLabel)
        gridLayout.addWidget(self.combo) 
        gridLayout.addWidget(self.textInput)
        gridLayout.addWidget(self.startButton)

        self.image = QPixmap('testDevice.jpg')
        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.image)
        picLayout.addWidget(self.lbl)
        picLayout.addWidget(self.textOutput)     

        fullLayout = QHBoxLayout()
        fullLayout.addLayout(menuLayout)
        fullLayout.addLayout(picLayout)

        self.horizontalGroupBox.setLayout(fullLayout) 

    def comboBoxLabel(self):
        comboLabel = QLabel()
        comboLabel.setText('--Select Test Type--')
        comboLabel.setAlignment(Qt.AlignCenter)
        return comboLabel

    def comboBox(self):
        combo = QComboBox()
        combo.setFont(self.font)
        combo.addItem('Test 1', 1)
        combo.addItem('Test 2', 2)
        combo.addItem('Test 3', 3)
        return combo

    def initializeButton(self):
        initButton = QPushButton('Initialize Controls', self)
        initButton.setToolTip('Checks Connections and Homes Controls')
        initButton.clicked.connect(self.initialize)
        initButton.setFont(self.font)     
        return initButton

    def startTestButton(self):
        startButton = QPushButton('Begin Selected Test')
        startButton.setToolTip('Initialize Controls must be complete prior to test start')
        startButton.clicked.connect(self.startTest)
        startButton.setEnabled(False)
        startButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        startButton.setFont(self.font)
        return startButton

    def outputText(self):
        outputText = QTextEdit(self)
        outputText.setFontPointSize(11)
        outputText.setReadOnly(True)
        outputText.hide()
        return outputText

    def wattageInput(self):
        inputText = QLineEdit(self)
        return inputText

    def log(self, output):
        self.textOutput.insertPlainText(output)
        self.textOutput.moveCursor(QTextCursor.End)

    #TODO: intialize variable needs to be set by checking connections and homing controls (To check fail condition set initialize = False) (try textChanged.connect for status update output)
    def initialize(self):
        self.log('Checking Connections and Zeroizing Controls\n')
        initialize = True #This line is for testing purposes ONLY, remove after initialize controls function created
        if initialize:
            self.startButton.setEnabled(True)
            self.startButton.setToolTip('Starts Selected Test')
            self.lbl.hide()
            self.textOutput.show()
        else:
            self.textOutput.setTextColor(self.red)
            self.log('Initialization Failed. Check connections and try again\n')
            self.textOutput.setTextColor(self.black)

    def startTest(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())