from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QLabel, QFileDialog, QInputDialog, QScrollArea)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QPointF
import sys
import json
import os


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

        self.saveSilhouetteButton = QPushButton("Save Silhouette")
        self.saveSilhouetteButton.clicked.connect(self.saveSilhouette)
        self.layout.addWidget(self.saveSilhouetteButton)

        self.scrollArea = QScrollArea(self)
        self.layout.addWidget(self.scrollArea)

        self.imageLabel = QLabel()
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setWidgetResizable(True)

        self.referenceLines = []

        self.pointsCollected = 0
        self.scaleFactor = 1.0

        # Panning
        self.panning = False
        self.lastMousePos = QPointF()

        # Initial window size
        self.setMinimumSize(800, 600)

        # Set an initial zoom factor
        self.zoomFactor = 1.0

        # Load silhouettes
        self.loadSilhouettes()
        self.loadSilhouetteButton = QPushButton("Load Silhouette")
        self.loadSilhouetteButton.clicked.connect(self.loadSilhouette)
        self.layout.addWidget(self.loadSilhouetteButton)

    def loadImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        if imagePath:
            self.originalPixmap = QPixmap(imagePath)
            self.displayImage()
    def displayImage(self):
        if hasattr(self, 'originalPixmap'):
            # Scale the image by the zoom factor
            scaled_pixmap = self.originalPixmap.scaled(self.scrollArea.size() * self.zoomFactor, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Compute the effective scaling factors
            sx = scaled_pixmap.width() / self.originalPixmap.width()
            sy = scaled_pixmap.height() / self.originalPixmap.height()

            # Create a pixmap to draw on
            self.imagePixmap = QPixmap(scaled_pixmap.size())
            self.imagePixmap.fill(Qt.transparent)

            # Create a QPainter and draw the scaled image
            p = QPainter(self.imagePixmap)
            p.drawPixmap(0, 0, scaled_pixmap)

            # Draw the lines
            for line_data in self.referenceLines:
                p1, p2, distance = line_data
                # Apply the effective scaling factors to the points
                p1 = QPointF(p1.x() * sx, p1.y() * sy)
                p2 = QPointF(p2.x() * sx, p2.y() * sy)
                # Draw the line and text
                self.drawLineAndText(p, p1, p2, distance)

            # End the QPainter
            p.end()

            # Set the pixmap to the label
            self.imageLabel.setPixmap(self.imagePixmap)

    def wheelEvent(self, event):
        # Handle zooming using the mouse wheel
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            # Zoom in or out
            delta = event.angleDelta().y()
            if delta > 0:
                # Zoom in
                self.zoomFactor *= 1.1
            elif delta < 0:
                # Zoom out
                self.zoomFactor *= 0.9
            # Redisplay the image with the new zoom factor
            self.displayImage()

    def mousePressEvent(self, event):
        if hasattr(self, 'originalPixmap') and self.imageLabel.geometry().contains(event.pos()):
            pos = self.scrollArea.mapFrom(self, event.pos())

            # Compute the effective scaling factors
            sx = self.imagePixmap.width() / self.originalPixmap.width()
            sy = self.imagePixmap.height() / self.originalPixmap.height()

            # Transform the position of the click into image space
            widget_pos = pos - self.scrollArea.widget().rect().topLeft()
            pos_in_image_space = QPointF(widget_pos.x() / sx, widget_pos.y() / sy)

            # ... rest of the code

            if event.button() == Qt.LeftButton:
                if self.pointsCollected == 0:
                    self.pointsCollected += 1
                    self.lastPoint = pos_in_image_space
                else:
                    self.pointsCollected = 0
                    endPoint = pos_in_image_space

                    # Ask for the real-world distance
                    realWorldDistance, ok = QInputDialog.getDouble(self, "Real-world distance", "Enter the real-world distance for the line (in meters):")
                    if ok:
                        self.referenceLines.append((self.lastPoint, endPoint, realWorldDistance))
                        self.displayImage()

    def drawLineAndText(self, painter, p1, p2, distance):
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.drawLine(p1, p2)

        # Write the distance on the line
        font = QFont()
        font.setPointSize(20)
        painter.setFont(font)
        midPoint = (p1 + p2) / 2
        painter.drawText(midPoint, f"{distance} m")

    def saveSilhouette(self):
        if not hasattr(self, 'originalPixmap'):
            return

        silhouetteName, ok = QInputDialog.getText(self, "Silhouette Name", "Enter a name for the silhouette:")
        if ok and silhouetteName:
            self.silhouettes[silhouetteName] = [(p1.x(), p1.y(), p2.x(), p2.y(), dist) for p1, p2, dist in self.referenceLines]
            self.saveSilhouettes()

    def saveSilhouettes(self):
        with open('silhouettes.json', 'w') as f:
            json.dump(self.silhouettes, f)
            
    def applySilhouette(self, silhouetteName):
        if silhouetteName in self.silhouettes:
            self.referenceLines = self.silhouettes[silhouetteName]
            self.displayImage()

    def loadSilhouettes(self):
        if os.path.exists('silhouettes.json'):
            with open('silhouettes.json', 'r') as f:
                self.silhouettes = {name: [(QPointF(p1x, p1y), QPointF(p2x, p2y), dist) for p1x, p1y, p2x, p2y, dist in lines] for name, lines in json.load(f).items()}

        else:
            self.silhouettes = {}
    def loadSilhouette(self):
        silhouetteName, ok = QInputDialog.getItem(self, "Load Silhouette", "Select a silhouette to load:", list(self.silhouettes.keys()), 0, False)
        if ok and silhouetteName:
            self.applySilhouette(silhouetteName)

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
