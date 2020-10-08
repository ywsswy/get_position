import sys
import PyQt5.QtWidgets
import PyQt5.QtGui
import PyQt5.QtCore
from system_hotkey import SystemHotkey
import threading

print("Ctrl + 2:    开始画线/清空画线")

class YGlobal(object):
    inter = 0.08
    dis_flag = False
    s_x = 0
    s_y = 0
    line_flag = False
    line_end_flag = False
    line_s_x = 0
    line_s_y = 0
    pen1 = PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(255, 0, 255), 1, PyQt5.QtCore.Qt.CustomDashLine)
    pen1.setDashPattern([1, 5])
    pen2 = PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(255, 0, 255), 25, PyQt5.QtCore.Qt.CustomDashLine)
    pen2.setDashPattern([1, 0])

def Align():
    x0 = 100
    y0 = 100
    x1 = 0
    y1 = 100
    x2 = 100
    y2 = 0
    k = ((x0 - x1) * (x2 - x1) + (y0 - y1) * (y2 - y1)) / ((x2 - x1) ** 2 + (y2 - y1) ** 2)
    x = x1 + k*(x2 - x1)
    y = y1 + k*(y2 - y1)
    print("{},{}".format(x, y))

def CalDis():
    YGlobal.dis_flag = not YGlobal.dis_flag
    if YGlobal.dis_flag:
        YGlobal.s_x = PyQt5.QtGui.QCursor.pos().x()
        YGlobal.s_y = PyQt5.QtGui.QCursor.pos().y()
    else:
        YGlobal.s_x = 0
        YGlobal.s_y = 0

def StartLine():
    YGlobal.line_flag = not YGlobal.line_flag
    if YGlobal.line_flag:
        YGlobal.line_s_x = PyQt5.QtGui.QCursor.pos().x()
        YGlobal.line_s_y = PyQt5.QtGui.QCursor.pos().y()
    else:
        YGlobal.line_end_flag = False

def EndLine():
    YGlobal.line_end_flag = not YGlobal.line_end_flag
    YGlobal.line_e_x = PyQt5.QtGui.QCursor.pos().x()
    YGlobal.line_e_y = PyQt5.QtGui.QCursor.pos().y()

class MyWin(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)

    def paintEvent(self, event):
        label1.setText("{},{}".format(PyQt5.QtGui.QCursor.pos().x() - YGlobal.s_x,
                                      PyQt5.QtGui.QCursor.pos().y() - YGlobal.s_y))
        label2.setText("{},{}".format(PyQt5.QtGui.QCursor.pos().x() - YGlobal.s_x,
                                      PyQt5.QtGui.QCursor.pos().y() - YGlobal.s_y))
        dis = (PyQt5.QtGui.QCursor.pos().x() - YGlobal.s_x) ** 2 \
               + (PyQt5.QtGui.QCursor.pos().y() - YGlobal.s_y) ** 2;
        dis = dis ** (0.5)
        label3.setText("{}".format(dis))
        if YGlobal.line_flag:
            qp = PyQt5.QtGui.QPainter()
            qp.begin(self)
            winps = self.mapFromGlobal(PyQt5.QtCore.QPoint(YGlobal.line_s_x,
                                                           YGlobal.line_s_y))
            if YGlobal.line_end_flag:
                qp.setPen(YGlobal.pen1)
                winpe = self.mapFromGlobal(PyQt5.QtCore.QPoint(YGlobal.line_e_x,
                                                               YGlobal.line_e_y))
            else:
                qp.setPen(YGlobal.pen2)
                winpe = self.mapFromGlobal(PyQt5.QtCore.QPoint(PyQt5.QtGui.QCursor.pos().x(),
                                                               PyQt5.QtGui.QCursor.pos().y()))
            qp.drawLine(winps.x(), winps.y(), winpe.x(), winpe.y())
            qp.end()

app = PyQt5.QtWidgets.QApplication(sys.argv)
win = MyWin()
win.setWindowTitle("yws_title")
win.resize(1300, 700)
win.setWindowFlags(PyQt5.QtCore.Qt.WindowStaysOnTopHint
                   | PyQt5.QtCore.Qt.FramelessWindowHint)
win.setAttribute(PyQt5.QtCore.Qt.WA_TranslucentBackground)

palette1 = PyQt5.QtGui.QPalette()
palette1.setColor(PyQt5.QtGui.QPalette.WindowText, PyQt5.QtGui.QColor(0, 0, 255))
palette2 = PyQt5.QtGui.QPalette()
palette2.setColor(PyQt5.QtGui.QPalette.WindowText, PyQt5.QtGui.QColor(255, 0, 0))
palette3 = PyQt5.QtGui.QPalette()
palette3.setColor(PyQt5.QtGui.QPalette.WindowText, PyQt5.QtGui.QColor(0, 255, 0))

label1 = PyQt5.QtWidgets.QLabel(win)
label1.setText("hello")
label1.setFont(PyQt5.QtGui.QFont("Roman times", 13))
label1.setGeometry(0,0,200,18)
label1.setPalette(palette1);

label2 = PyQt5.QtWidgets.QLabel(win)
label2.setText("hello")
label2.setFont(PyQt5.QtGui.QFont("Roman times", 13))
label2.setGeometry(0,18,200,18)
label2.setPalette(palette2);

label3 = PyQt5.QtWidgets.QLabel(win)
label3.setText("world")
label3.setFont(PyQt5.QtGui.QFont("Roman times", 13))
label3.setGeometry(0,36,200,18)
label3.setPalette(palette3);

hk_stop = SystemHotkey()
hk_stop.register(('control', '1'), callback=lambda x: CalDis())
hk_stop.register(('control', '2'), callback=lambda x: StartLine())
hk_stop.register(('control', '3'), callback=lambda x: EndLine())
#hk_stop.register(('control', '4'), callback=lambda x: Align())
win.show()

def Refresh():
    win.update()
    threading.Timer(YGlobal.inter, Refresh).start()

threading.Timer(YGlobal.inter, Refresh).start()
sys.exit(app.exec_())
