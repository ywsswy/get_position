import sys
import PyQt5.QtWidgets
import PyQt5.QtGui
import PyQt5.QtCore
from system_hotkey import SystemHotkey
import threading

class YGlobal(object):
    inter = 0.08
    dis_flag = False
    s_x = 0
    s_y = 0

def CalDis():
    YGlobal.dis_flag = not YGlobal.dis_flag
    if YGlobal.dis_flag:
        YGlobal.s_x = PyQt5.QtGui.QCursor.pos().x()
        YGlobal.s_y = PyQt5.QtGui.QCursor.pos().y()
    else:
        YGlobal.s_x = 0
        YGlobal.s_y = 0

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

app = PyQt5.QtWidgets.QApplication(sys.argv)
win = MyWin()
win.setWindowTitle("yws_title")
win.resize(1200, 500)
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
win.show()

def Refresh():
    win.update()
    threading.Timer(YGlobal.inter, Refresh).start()

threading.Timer(YGlobal.inter, Refresh).start()
sys.exit(app.exec_())
