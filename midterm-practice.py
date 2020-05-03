#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In the example, we draw randomly 1000 red points
on the window.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""
#http://zetcode.com/gui/pyqt5/painting/
#https://doc.qt.io/qtforpython/PySide2/QtGui/QCursor.html

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QPainterPath
from PyQt5.QtCore import Qt
import sys, random, pygame, numpy as np



class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Curves')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        self.controlPoints(qp)
        self.drawBezierCurve(qp)
        qp.end()

    def drawPoints(self, qp):
        qp.setPen(Qt.black)
        size = self.size()
        qp.drawPoint(100, 100)

    def controlPoints(self, qp):
        qp.setPen(Qt.red)
        size = self.size()
        qp.drawPoint(200,150)

    def drawBezierCurve(self, qp):
        path = QPainterPath()
        path.moveTo(30, 30)
        path.cubicTo(30, 30, 200, 150, 350, 30)
        qp.drawPath(path)

    def lagrange(self, qp):
        curve = np.arange(0, 3, 1)
        for t in np.arange(0, 2, 0.001):
            px = [0.0, 0.0]
            for i in curve:
                xn, xd = 1, 1
                for j in np.arange(0, 3, 1):
                    if j != i:
                        xn = xn * (t - j)
                        xd = xd * (i - j)
                px = px + np.dot(pts[i], (xn) / (xd))
            px = px.astype(int)
            qp.drawPoint(px, color, thick=1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())