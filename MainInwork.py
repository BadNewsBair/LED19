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
        self.initButton = self.initializeButton()
        self.comboLabel = self.comboBoxLabel()
        self.combo = self.comboBox()
        self.startButton = self.startTestButton()
        self.text = QTextEdit(self)
        self.text.setFontPointSize(12)
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

    def mainLayout(self): 
        menuLayout = QVBoxLayout()
        picLayout = QVBoxLayout()

        self.horizontalGroupBox = QGroupBox('LED Test Module')

        
        menuLayout.addWidget(self.initButton)
        menuLayout.addWidget(self.comboLabel)
        menuLayout.addWidget(self.combo)
        menuLayout.addWidget(self.startButton)
        menuLayout.addWidget(self.text)  

        image = QPixmap('testDevice.jpg')
        lbl = QLabel(self)
        lbl.setPixmap(image)
        picLayout.addWidget(lbl)     

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
        combo.addItem('Test 1', 1)
        combo.addItem('Test 2', 2)
        combo.addItem('Test 3', 3)
        return combo

    def initializeButton(self):
        initButton = QPushButton('Initialize Controls', self)
        initButton.setToolTip('Checks Connections and Homes Controls')
        initButton.clicked.connect(self.initialize)
        
        return initButton

    def startTestButton(self):
        startButton = QPushButton('Begin Selected Test')
        startButton.setToolTip('Initialize Controls must be complete prior to test start')
        startButton.clicked.connect(self.startTest)
        startButton.setEnabled(False)
        return startButton

    #TODO: intialize variable needs to be set by checking connections and homing controls (To check fail condition set initialize = False) (try textChanged.connect for status update output)
    def initialize(self):
        self.text.insertPlainText('Checking Connections and Zeroizing Controls\n')
        initialize = True
        if initialize:
            self.startButton.setEnabled(True)
            self.startButton.setToolTip('Starts Selected Test')
        else:
            red = QColor(255, 0, 0)
            black = QColor(0, 0, 0)
            self.text.setTextColor(red)
            self.text.insertPlainText('Initialization Failed. Check connections and try again\n')
            self.text.setTextColor(black)

    def startTest(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())