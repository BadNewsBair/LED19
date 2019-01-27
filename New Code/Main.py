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
        self.font15 = QFont()
        self.font15.setPointSize(15)
        self.font12 = QFont()
        self.font12.setPointSize(12)

        self.initInfo = self.informationLabel('Prior to test start a connection test must be made and all controls must return to their home position.\n'
                                            'To accomplish this use the Initialize Controls button.')
        self.initButton = self.initializeButton()
        self.comboLabel = self.comboBoxLabel()
        self.combo = self.comboBox()
       
        self.wattLabel = self.wattageLabel()
        self.watttInput = self.wattageInput()
        self.disLabel = self.distanceLabel()
        self.disInput = self.distanceInput()
        self.textOutput = self.outputText()
        
        self.startButton = self.startTestButton()
        self.pauseButton = self.pauseTestButton()
        self.continueButton = self.continueTestButton()
        self.saveButton = self.saveDataButton()
        self.endInfo = self.informationLabel('Please refer to the following link for a walkthrough tutorial and instruction manual *******link********')
        
        self.image = QPixmap('testDevice.jpg')
        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.image)

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
        gridLayout = QGridLayout()
        picLayout = QVBoxLayout()

        self.horizontalGroupBox = QGroupBox('LED Test Module')
        
        gridLayout.addWidget(self.initInfo, 0, 0, 1, 0)
        gridLayout.addWidget(self.initButton, 1, 0, 1, 2)
        gridLayout.addWidget(self.comboLabel, 2, 0, 1, 1)
        gridLayout.addWidget(self.combo, 2, 1, 1, 1)
        gridLayout.addWidget(self.wattLabel, 3, 0)
        gridLayout.addWidget(self.watttInput, 3, 1)
        gridLayout.addWidget(self.disLabel, 4, 0)
        gridLayout.addWidget(self.disInput, 4, 1)
        gridLayout.addWidget(self.startButton, 5, 0, 1, 2)
        gridLayout.addWidget(self.pauseButton, 6, 0, 1, 2)
        gridLayout.addWidget(self.saveButton, 7, 0, 1, 2)
        gridLayout.addWidget(self.endInfo, 8, 0, 1, 0)
        

        picLayout.addWidget(self.lbl)
        picLayout.addWidget(self.textOutput)     

        fullLayout = QHBoxLayout()
        fullLayout.addLayout(gridLayout)
        fullLayout.addLayout(picLayout)

        self.horizontalGroupBox.setLayout(fullLayout) 

    def comboBoxLabel(self):
        comboLabel = QLabel()
        comboLabel.setText('--Select Test Mode--')
        comboLabel.setFont(self.font15)
        return comboLabel

    def comboBox(self):
        combo = QComboBox()
        combo.setFont(self.font15)
        combo.addItem('Test 1', 1)
        combo.addItem('Test 2', 2)
        combo.addItem('Test 3', 3)
        return combo

    def initializeButton(self):
        initButton = QPushButton('Initialize Controls', self)
        initButton.setToolTip('Checks Connections and Homes Controls')
        initButton.clicked.connect(self.initialize)
        initButton.setFont(self.font15) 
        # initButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)    
        return initButton

    def startTestButton(self):
        startButton = QPushButton('Begin Selected Test')
        startButton.setToolTip('Initialize Controls must be complete prior to test start')
        startButton.clicked.connect(self.startTest)
        startButton.setEnabled(False)
        # startButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        startButton.setFont(self.font15)
        return startButton

    def pauseTestButton(self):
        pauseButton = QPushButton('Pause Test')
        pauseButton.setToolTip('Pause Test')
        pauseButton.clicked.connect(self.pauseTest)
        pauseButton.setEnabled(False)
        # pauseButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        pauseButton.setFont(self.font15)
        return pauseButton

    def continueTestButton(self):
        continueButton = QPushButton('Continue Test')
        continueButton.setToolTip('Continue Test')
        continueButton.clicked.connect(self.continueTest)
        return continueButton

    def saveDataButton(self):
        saveButton = QPushButton('Save Data')
        saveButton.setToolTip('Save Data to File')
        saveButton.clicked.connect(self.saveData)
        saveButton.setEnabled(False)
        # saveButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        saveButton.setFont(self.font15)
        return saveButton

    def informationLabel(self, text):
        info = QLabel()
        info.setText(text)
        info.setFont(self.font12)
        info.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        return info

    def outputText(self):
        outputText = QTextEdit(self)
        outputText.setFontPointSize(11)
        outputText.setReadOnly(True)
        outputText.hide()
        return outputText

    def wattageLabel(self):
        wattageLabel = QLabel()
        wattageLabel.setText('--Input Wattage--')
        wattageLabel.setFont(self.font15)
        return wattageLabel

    def wattageInput(self):
        inputText = QLineEdit(self)
        inputText.setPlaceholderText('Input Wattage')
        inputText.setFont(self.font15)
        return inputText

    def distanceLabel(self):
        distanceLabel = QLabel()
        distanceLabel.setText('--Input Distance--')
        distanceLabel.setFont(self.font15)
        return distanceLabel

    def distanceInput(self):
        distance = QLineEdit(self)
        distance.setPlaceholderText('Input Distance')
        distance.setFont(self.font15)
        return distance

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

    def pauseTest(self):
        pass

    def continueTest(self):
        pass

    def saveData(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())