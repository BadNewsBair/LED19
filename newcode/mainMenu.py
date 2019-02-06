import sys
import time
from control import MotorControl
from measurement import Measurement
from PyQt5.QtGui import QColor, QPixmap, QFont, QIcon, QTextCursor
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon('icon.png'))
        self.left = 200
        self.top = 100
        self.width = 1000
        self.height = 800
        self.red = QColor(255, 0, 0)
        self.black = QColor(0, 0, 0)
        self.font12 = QFont()
        self.font12.setPointSize(12)

        self.createLeftGroup()
        self.createRightGroup()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.LeftGroup, 1, 0, 1, 1)
        mainLayout.addWidget(self.RightGroup, 1, 1, 2, 1)
        mainLayout.setColumnStretch(1, 1)
        mainLayout.setRowStretch(1, 1)
        self.setLayout(mainLayout)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.motor = MotorControl(self.log)
        # self.measure = Measurement(self.log)

    def createLeftGroup(self):
        self.LeftGroup = QGroupBox('LED Test Module')
        simplyLogo = QPixmap('simplyleds.png')
        logoLabel = QLabel(self)
        logoLabel.setPixmap(simplyLogo)
        self.initInfo = self.informationLabel('Prior to test start all controls must return to their home position.\n'
                                             'To accomplish this use the Initialize Controls button.')
        self.initButton = self.initializeButton()
        self.comboLabel = self.comboBoxLabel()
        self.combo = self.comboBox()
        self.wattLabel = self.wattageLabel()
        self.wattage = self.wattageInput()
        self.disLabel = self.distanceLabel()
        self.distance = self.distanceInput()
        self.startButton = self.startTestButton()
        self.pauseButton = self.pauseTestButton()
        self.continueButton = self.continueTestButton()
        self.saveButton = self.saveDataButton()
        self.endInfo = self.informationLabel('Please refer to the following link for a walkthrough tutorial and\ninstruction manual *******link********')
        
        layout = QGridLayout()
        layout.addWidget(logoLabel, 1, 0)
        layout.addWidget(self.initInfo, 2, 0, 1, 2)
        layout.addWidget(self.initButton, 3, 0, 1, 2)
        layout.addWidget(self.comboLabel, 4, 1)
        layout.addWidget(self.combo, 4, 0, 1, 1)
        layout.addWidget(self.wattage, 5, 0, 1, 1)
        layout.addWidget(self.wattLabel, 5, 1)
        layout.addWidget(self.distance, 6, 0, 1, 1)
        layout.addWidget(self.disLabel, 6, 1)
        layout.addWidget(self.startButton, 7, 0, 1, 2)
        layout.addWidget(self.pauseButton, 8, 0, 1, 2)
        layout.addWidget(self.continueButton, 9, 0, 1, 2)
        layout.addWidget(self.saveButton, 10, 0, 1, 2)
        layout.addWidget(self.endInfo, 11, 0, 1, 2)
        self.LeftGroup.setLayout(layout)

    def createRightGroup(self):
        self.RightGroup = QGroupBox()
        self.mainimage = QPixmap('testDevice.jpg')
        self.mainLabel = QLabel(self)
        self.mainLabel.setPixmap(self.mainimage)
        self.textOutput = self.outputText()

        layout = QVBoxLayout()
        layout.addWidget(self.mainLabel)
        layout.addWidget(self.textOutput)
        self.RightGroup.setLayout(layout)

    def comboBoxLabel(self):
        comboLabel = QLabel()
        comboLabel.setText('Test Mode')
        comboLabel.setFont(self.font12)
        return comboLabel

    def comboBox(self):
        combo = QComboBox()
        combo.setFont(self.font12)
        combo.addItem('Test 1', 1)
        combo.addItem('Test 2', 2)
        combo.addItem('Test 3', 3)
        return combo

    def initializeButton(self):
        initButton = QPushButton('Initialize Controls', self)
        initButton.setToolTip('Checks Connections and Homes Controls')
        initButton.clicked.connect(self.initialize)
        initButton.setFont(self.font12) 
        self.setButtonSize(initButton)   
        return initButton

    def startTestButton(self):
        startButton = QPushButton('Begin Selected Test')
        startButton.setToolTip('Starts Selected Test')
        startButton.clicked.connect(self.startTest)
        startButton.setEnabled(False)
        startButton.setFont(self.font12)
        self.setButtonSize(startButton)
        return startButton

    def pauseTestButton(self):
        pauseButton = QPushButton('Pause Test')
        pauseButton.setToolTip('Pause Test')
        pauseButton.clicked.connect(self.pauseTest)
        pauseButton.setEnabled(False)
        pauseButton.setFont(self.font12)
        self.setButtonSize(pauseButton)
        return pauseButton

    def continueTestButton(self):
        continueButton = QPushButton('Continue Test')
        continueButton.setToolTip('Continue Test')
        continueButton.clicked.connect(self.continueTest)
        continueButton.setFont(self.font12)
        self.setButtonSize(continueButton)
        continueButton.hide()
        return continueButton

    def saveDataButton(self):
        saveButton = QPushButton('Save Data')
        saveButton.setToolTip('Save Data to File')
        saveButton.clicked.connect(self.saveData)
        saveButton.setEnabled(False)
        saveButton.setFont(self.font12)
        self.setButtonSize(saveButton)
        return saveButton

    def informationLabel(self, text):
        info = QLabel()
        info.setText(text)
        info.setFont(self.font12)
        self.setButtonSize(info)
        return info

    def outputText(self):
        outputText = QTextEdit(self)
        outputText.setFontPointSize(11)
        outputText.setReadOnly(True)
        outputText.hide()
        outputText.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return outputText

    def wattageLabel(self):
        wattageLabel = QLabel()
        wattageLabel.setText('Watts')
        wattageLabel.setFont(self.font12)
        return wattageLabel

    def wattageInput(self):
        inputText = QLineEdit(self)
        inputText.setPlaceholderText('Input Wattage')
        inputText.setFont(self.font12)
        return inputText

    def distanceLabel(self):
        distanceLabel = QLabel()
        #TODO: Fix distance measurement, Meters or Feet
        distanceLabel.setText('Feet ')
        distanceLabel.setFont(self.font12)
        return distanceLabel

    def distanceInput(self):
        distance = QLineEdit(self)
        distance.setPlaceholderText('Input Distance')
        distance.setFont(self.font12)
        return distance

    def log(self, output):
        self.textOutput.append(output)
        self.textOutput.moveCursor(QTextCursor.End)
    
    def errorLog(self, output):
        self.textOutput.setTextColor(self.red)
        self.textOutput.append(output)
        self.textOutput.setTextColor(self.black)


    def setButtonSize(self, button):
        button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    #TODO: intialize variable needs to be set by checking connections and homing controls (To check fail condition set initialize = False) (try textChanged.connect for status update output)
    def initialize(self):
        self.mainLabel.hide()
        self.textOutput.show()
        self.log('Checking Connections and Zeroizing Controls')
        initialize = self.motor.initializeControls()
        connection = self.motor.checkConnection()
        if initialize and connection:
            self.startButton.setEnabled(True)
        else:
            self.errorLog('Initialization Failed. Check connections and try again')
            
    def startTest(self):
        try: 
            userWattage = float(self.wattage.text())  
            userDistance = float(self.distance.text())
            self.wattage.setDisabled(True)
            self.distance.setDisabled(True) 
            self.initButton.setDisabled(True)
            self.pauseButton.setDisabled(False)
            self.startButton.setDisabled(True)
            self.combo.setDisabled(True)
            self.log('Test Starting')
        except ValueError:
            self.errorLog('Unable to Start Test: Check Input Values-Must be able to convert to float')

    def pauseTest(self):
        self.pauseButton.hide()
        self.continueButton.show()
        self.log('Test Paused')
        
    def continueTest(self):
        self.continueButton.hide()
        self.pauseButton.show()
        self.log('Test Continued')

    def saveData(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())