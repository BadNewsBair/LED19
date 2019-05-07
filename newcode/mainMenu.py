import sys
import os
import time
import datetime
import threading
from processingcontrol import Measurement, MotorControl
from PyQt5.QtGui import QColor, QPixmap, QFont, QIcon, QTextCursor
from PyQt5.QtCore import QDateTime, QDir, Qt, QTimer, QUrl 
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMessageBox, QPushButton, QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle('Simply LEDs')
        self.left = 100
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
        
        ## Set either Maximized or parameters
        # self.showMaximized()
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.motor = MotorControl(self.log)

    def createLeftGroup(self):
        text = self.instructionManual()
        self.LeftGroup = QGroupBox('LED Test Module')

        self.logoLabel = self.logoImage()
        self.initInfo = self.informationLabel('Prior to test start all controls must return to their home position.\n'
                                            'To accomplish this use the Initialize Controls button.\n'
                                            'Once a test is started, all input fields will be disabled and their inputs will be saved.\n'
                                            'The test will not be able to start if a data  field is left blank or an improper data type is used.')
        self.fileName = self.fileNameInput()
        self.testLine = self.testNumberInput()
        self.devicePartNumber = self.partNumberInput()
        self.driverPartNumber = self.driverPartNumberInput()
        self.initButton = self.initializeButton()
        self.typeComboLabel = self.comboBoxLabel()
        self.typeCombo = self.typeComboBox()
        self.wattLabel = self.wattageLabel()
        self.wattage = self.wattageInput()
        self.distanceCombo = self.disCombo()
        self.distance = self.distanceInput()
        self.startButton = self.startTestButton()
        self.pauseButton = self.pauseTestButton()
        self.continueButton = self.continueTestButton()
        self.restartButton = self.restartModuleButton()
        self.endInfo = self.informationLabel('For additional support, refer to the manual at the following link: ' + text)
        self.endInfo.setOpenExternalLinks(True)
        
        layout = QGridLayout()
        layout.addWidget(self.logoLabel, 1, 0)       
        layout.addWidget(self.initInfo, 2, 0, 1, 2)
        layout.addWidget(self.initButton, 3, 0, 1, 2)
        layout.addWidget(self.fileName, 4, 0, 1, 2)
        layout.addWidget(self.testLine, 5, 0, 1, 2)
        layout.addWidget(self.devicePartNumber, 6, 0, 1, 2)
        layout.addWidget(self.driverPartNumber, 7, 0 , 1, 2)        
        layout.addWidget(self.typeComboLabel, 8, 1)
        layout.addWidget(self.typeCombo, 8, 0, 1, 1)
        layout.addWidget(self.wattage, 9, 0, 1, 1)
        layout.addWidget(self.wattLabel, 9, 1)
        layout.addWidget(self.distance, 10, 0, 1, 1)
        layout.addWidget(self.distanceCombo, 10, 1)
        layout.addWidget(self.startButton, 11, 0, 1, 2)
        layout.addWidget(self.pauseButton, 12, 0, 1, 2)
        layout.addWidget(self.continueButton, 13, 0, 1, 2)
        layout.addWidget(self.restartButton, 14, 0, 1, 2)
        layout.addWidget(self.endInfo, 15, 0, 1, 2)
        self.LeftGroup.setLayout(layout)

    def logoImage(self):
        simplyLogo = QPixmap('simplyleds.png')
        logoLabel = QLabel(self)
        logoLabel.setPixmap(simplyLogo)
        return logoLabel

    def instructionManual(self):
        manualPath = os.path.dirname(os.path.realpath(__file__)) + r'\InstructionManual.docx'
        instructionManual = QDir.home().filePath(manualPath)
        url = bytearray(QUrl.fromLocalFile(instructionManual).toEncoded()).decode()
        text = '<a href={}>Instruction Manual</a>'.format(url)
        return text

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
        typecomboLabel = QLabel()
        typecomboLabel.setText('Test Mode')
        typecomboLabel.setFont(self.font12)
        return typecomboLabel

    def typeComboBox(self):
        combo = QComboBox()
        combo.setFont(self.font12)
        combo.addItem('Single Measurement', 1)
        combo.addItem('Type 3 - ', 3)
        combo.addItem('Type 4 - ', 4)
        combo.addItem('Type 5 - ', 5)
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

    def restartModuleButton(self):
        restartButton = QPushButton('Restart Module')
        restartButton.setToolTip('Restarts entire program')
        restartButton.clicked.connect(self.restartModule)
        restartButton.setFont(self.font12)
        self.setButtonSize(restartButton)
        return restartButton

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

    def fileNameInput(self):
        name = QLineEdit(self)
        name.setPlaceholderText('IESNA/Input name to save file as')
        name.setFont(self.font12)
        return name
    
    def testNumberInput(self):
        num = QLineEdit(self)
        num.setPlaceholderText('Input Test Number')
        num.setFont(self.font12)
        return num

    def partNumberInput(self):
        num = QLineEdit(self)
        num.setPlaceholderText('LumCat/Input Device Part Number')
        num.setFont(self.font12)
        return num

    def driverPartNumberInput(self):
        num = QLineEdit(self)
        num.setPlaceholderText('BallastCat/Input Driver Part Number')
        num.setFont(self.font12)
        return num

    def disCombo(self):
        comboDis = QComboBox()
        comboDis.setFont(self.font12)
        comboDis.addItem('Feet', 1)
        comboDis.addItem('Meters', 2)
        return comboDis

    def distanceInput(self):
        distance = QLineEdit(self)
        distance.setPlaceholderText('Input Distance')
        distance.setFont(self.font12)
        return distance

    def convertMetric(self, feet):
        meters = feet/3.2808
        return meters

    def units(self):
        if self.distanceCombo.currentData() == 1:
            unit = 'Feet'
        elif self.distanceCombo.currentData() == 2:
            unit = 'Meters'
        return unit

    def log(self, output):
        self.textOutput.append(output)
        self.textOutput.moveCursor(QTextCursor.End)
    
    def errorLog(self, output):
        self.textOutput.setTextColor(self.red)
        self.textOutput.append(output)
        self.textOutput.setTextColor(self.black)

    def getFileName(self):
        fileName = str(self.fileName.text())
        if fileName == '':
            fileName = str(datetime.datetime.now())
        return fileName
        
    def getDistance(self):
        try:
            distance = float(self.distance.text())
            if self.distanceCombo.currentData() == 1:
                distance = round(self.convertMetric(distance), 2)
            return distance
        except ValueError:
            self.errorLog('Unable to Start Test: Check Input Distance Value-Must be able to convert to float')

    def getWattage(self):
        try:
            return float(self.wattage.text())
        except ValueError:
            self.errorLog('Unable to Start Test: Check Input Wattage Value-Must be able to conver to float')

    def getTestNumber(self):
        return str(self.testLine.text())

    def getDeviceNumber(self):
        return str(self.devicePartNumber.text())

    def getDriverNumber(self):
        return str(self.driverPartNumber.text())

    def getTestType(self):
        return int(self.typeCombo.currentData())

    def setButtonSize(self, button):
        button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    #TODO: intialize variable needs to be set by checking connections and homing controls (To check fail condition set initialize = False) 
    def initialize(self):
        self.mainLabel.hide()
        self.textOutput.show()
        self.log('Checking Connections and Zeroizing Controls')
        connection = self.motor.checkConnection()
        initialize = self.motor.initializeControls()
        if initialize and connection:
            self.startButton.setEnabled(True)
        else:
            self.errorLog('Initialization Failed. Check connections and try again')
            
    def startTest(self):
        fileName = self.getFileName()
        testType = self.getTestType()
        testNumber = self.getTestNumber()
        deviceNumber = self.getDeviceNumber()
        driverNumber = self.getDriverNumber()
        distance = self.getDistance()
        wattage = self.getWattage()

        if distance and wattage != None:
            self.log('--User Inputs--')
            self.log('File Name: %s' % fileName)
            self.log('Test Type: %s' % testType)
            self.log('Distance: %s Meters' % distance)
            self.log('Wattage: %s Watts' % wattage)
            self.measure = Measurement(self.log, wattage, distance, fileName, testType, testNumber, deviceNumber, driverNumber)
            self.thread = threading.Thread(target = self.measure.beginTest)
            self.wattage.setDisabled(True)
            self.distance.setDisabled(True) 
            self.initButton.setDisabled(True)
            self.pauseButton.setDisabled(False)
            self.startButton.setDisabled(True)
            self.typeCombo.setDisabled(True)
            self.log('Test Starting')
            self.thread.daemon = True
            self.thread.start()

    def pauseTest(self):
        self.pauseButton.hide()
        self.continueButton.show()
        self.log('Test Paused')
        self.measure.isPaused = True
        
    def continueTest(self):
        self.continueButton.hide()
        self.pauseButton.show()
        self.log('Test Continued')
        self.measure.isPaused = False

    def restartModule(self):
        confirmRestart = QMessageBox.question(self, 'Confirm Restart', 'Are you sure you want to restart the module? All unsaved data will be lost.',
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmRestart == QMessageBox.Yes:
            python = sys.executable
            os.execl(python, python, * sys.argv)
        else:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())