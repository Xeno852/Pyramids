from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QLineEdit, QInputDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
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
        self.imageLabel.setMouseTracking(True)
        self.layout.addWidget(self.imageLabel)

        self.referenceLines = []

        self.drawing = False
        self.lastPoint = QPoint()
        self.scaleFactor = 1.0

    def loadImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        if imagePath:
            self.imagePixmap = QPixmap(imagePath)
            self.displayImage()

    def displayImage(self):
        if hasattr(self, 'imagePixmap'):
            self.imageLabel.setPixmap(self.imagePixmap.scaled(self.imageLabel.size() * self.scaleFactor, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    
    def resizeEvent(self, event):
        self.displayImage()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            endPoint = event.pos()

            # Draw line on pixmap
            if hasattr(self, 'imagePixmap'):
                p = QPainter(self.imagePixmap)
                pen = QPen(Qt.red, 10)
                p.setPen(pen)
                p.drawLine(self.imageLabel.mapFromParent(self.lastPoint), self.imageLabel.mapFromParent(endPoint))
                p.end()

            # Update display
            self.displayImage()

            print(f"Start point: {self.lastPoint}, End point: {endPoint}")

            # Ask for the real-world distance
            realWorldDistance, ok = QInputDialog.getDouble(self, "Real-world distance", "Enter the real-world distance for the line (in meters):")
            if ok:
                self.referenceLines.append((self.lastPoint, endPoint, realWorldDistance))
                print(f"Real-world distance: {realWorldDistance}")

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
