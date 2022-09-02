import PyQt5
import open3d as o3d
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from gui_viewer import Ui_MainWindow
import sys
import os
import ctypes
import win32gui
import sys

myappid = 'viewer3d-gui' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        widget = QtWidgets.QWidget()

        self.pcd = o3d.io.read_point_cloud("datasets/chair.ply")
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(self.pcd)

        hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")
        self.window = QtGui.QWindow.fromWinId(hwnd)
        self.windowcontainer = self.createWindowContainer(self.window, widget)
        self.layout_o3d.addWidget(self.windowcontainer, 0)

        self.btn_load_ply.clicked.connect(self.load_ply)
        self.btn_load_male.clicked.connect(self.load_male)
        self.btn_load_chair.clicked.connect(self.load_chair)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_vis)
        timer.start(1)

    def load_ply(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open a PLY file", "../examples-med3dsim/datasets",
                                                  "All Files (*);;Polygon File Format (*.ply)", options=options)
        if fileName:
            print(fileName)
            self.vis.remove_geometry(self.pcd)
            test_path="../examples-med3dsim/datasets/male/frozenCT.ply"
            self.pcd = o3d.io.read_point_cloud(fileName)
            self.vis.add_geometry(self.pcd)


    def load_male(self):
        self.vis.remove_geometry(self.pcd)
        self.pcd = o3d.io.read_point_cloud("datasets/male.ply")
        self.vis.add_geometry(self.pcd)
        # self.update_vis()
        # QMessageBox.information(self,"Tips","Loaded!")

    def load_chair(self):
        self.vis.remove_geometry(self.pcd)
        self.pcd = o3d.io.read_point_cloud("datasets/chair.ply")
        self.vis.add_geometry(self.pcd)
        # self.update_vis()
        # QMessageBox.information(self,"Tips","Loaded!")

    def update_vis(self):
        #self.vis.update_geometry()
        self.vis.poll_events()
        self.vis.update_renderer()


def main():
    app = QApplication(sys.argv)

    myWin = MyMainForm()
    myWin.show()
    try:
        r = app.exec_()
    except Exception as err:
        print(err)

if __name__ == "__main__":
   main()
