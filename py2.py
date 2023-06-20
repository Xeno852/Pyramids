from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QLineEdit, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QPainterPath
from PyQt5.QtCore import Qt, QPoint
import sys
import numpy as np
import cv2

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = QPainterPath()

    def mousePressEvent(self, event):
        self.path.moveTo(event.pos())

    def mouseMoveEvent(self, event):
        self.path.lineTo(event.pos())
        self.update()

    def mouseReleaseEvent(self, event):
        self.path.lineTo(event.pos())
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.drawPath(self.path)


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

        self.imageLabel = ImageLabel()
        self.layout.addWidget(self.imageLabel)

        self.addLineButton = QPushButton("Add Silhouette")
        self.addLineButton.clicked.connect(self.addSilhouette)
        self.layout.addWidget(self.addLineButton)

        self.imagePath = None

    def loadImage(self):
        self.imagePath, _ = QFileDialog.getOpenFileName()
        if self.imagePath:
            pixmap = QPixmap(self.imagePath)
            self.imageLabel.setPixmap(pixmap)

    def addSilhouette(self):
        if self.imagePath:
            # convert image to grayscale
            img = cv2.imread(self.imagePath, cv2.IMREAD_GRAYSCALE)
            # apply threshold to get silhouette
            _, img_thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
            # save the silhouette image
            cv2.imwrite('silhouette.png', img_thresh)
            # show the silhouette image
            pixmap = QPixmap('silhouette.png')
            self.imageLabel.setPixmap(pixmap)

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())