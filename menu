import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.title = 'Main Menu'
        self.left = 500
        self.top = 500
        self.width = 320
        self.height = 100
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createHorizontalLayout()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
 
        self.show()
 
    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox("Simply LED Test Module")
        layout = QHBoxLayout()

        initializeButton = QPushButton('Initialize', self)
        initializeButton.setToolTip('Check Connections')
        initializeButton.clicked.connect(self.initialize)
        layout.addWidget(initializeButton)

        zeroButton = QPushButton('Zeroize', self)
        zeroButton.setToolTip('Zeroize')
        zeroButton.clicked.connect(self.zeroize)
        layout.addWidget(zeroButton)

        testButton = QPushButton('Begin Test',self)
        testButton.setToolTip('Test Options')
        testButton.clicked.connect(self.testOptions)
        layout.addWidget(testButton)
 
        self.horizontalGroupBox.setLayout(layout)
 
 
    @pyqtSlot()
    def initialize(self):
        print('Checking Connections')

    def zeroize(self):
        print('Controls Zeroizing')

    def testOptions(self):
        print('Select Test')
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
