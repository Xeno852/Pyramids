from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QLineEdit
from PyQt5.QtGui import QPixmap, QImage
import sys

class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.loadImageButton = QPushButton("Load Image")
        self.loadImageButton.clicked.connect(self.loadImage)
        self.layout.addWidget(self.loadImageButton)

        self.imageLabel = QLabel()
        self.layout.addWidget(self.imageLabel)

        self.referenceLineInput = QLineEdit()
        self.layout.addWidget(self.referenceLineInput)

        self.addLineButton = QPushButton("Add Reference Line")
        self.addLineButton.clicked.connect(self.addReferenceLine)
        self.layout.addWidget(self.addLineButton)

        self.referenceLines = []

    def loadImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        if imagePath:
            pixmap = QPixmap(imagePath)
            self.imageLabel.setPixmap(pixmap)

    def addReferenceLine(self):
        referenceLine = self.referenceLineInput.text()
        self.referenceLines.append(referenceLine)
        self.referenceLineInput.clear()

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
