import os
from threading import Thread

import PyQt5
import open3d as o3d
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, QThread, QStringListModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from gui_human_body_shape_viewer import Ui_MainWindow
import ctypes
import win32gui
import sys
from medsim3d.datasets.ieee_ic_3dbp import IEEE_IC_3DBP_Dataset
from medsim3d.models.viewer3d import Viewer3D

myappid = 'human-body-shape-viewer3d-gui' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class GUIHumanBodyShapeViewer3D(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(GUIHumanBodyShapeViewer3D, self).__init__(parent)
        self.setupUi(self)
        widget = QtWidgets.QWidget()

        # self.pcd = o3d.io.read_point_cloud("datasets/chair.ply")
        self.pcd=None
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        # self.vis.add_geometry(self.pcd)

        hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")
        self.window = QtGui.QWindow.fromWinId(hwnd)
        self.windowcontainer = self.createWindowContainer(self.window, widget)
        self.layout_o3d.addWidget(self.windowcontainer, 0)

        self.btn_browse.clicked.connect(self.browse)
        self.btn_load.clicked.connect(self.load_model)
        self.btn_left.clicked.connect(self.left_load)
        self.btn_right.clicked.connect(self.right_load)
        self.dataset_root="../examples-med3dsim/datasets/human_body_shapes"
        self.edit_dataset_root.setText(self.dataset_root)

        self.read_datasets()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_vis)
        timer.start(1)

    def read_datasets(self):
        if os.path.exists(self.dataset_root):
            list_c=self.read_category()
            if len(list_c)!=0:
                self.read_models(list_c[0])

    def read_category(self):
        list_category=[]
        for file in os.listdir(self.dataset_root):
            list_category.append(file)
        self.cb_category.addItems(list_category)
        return list_category

    def read_models(self,category):
        list_model=[]
        for file in os.listdir(self.dataset_root+"/"+category+"/models"):
            model_name=file.replace(".obj","")
            list_model.append(model_name)
        self.cb_model.addItems(list_model)


    def browse(self):
        # open select folder dialog
        fname = QFileDialog.getExistingDirectory(
            self, 'Select a directory', "")
        print(fname)
        if fname:
            self.dataset_root = fname
            self.edit_dataset_root.setText(self.dataset_root)
            self.cb_category.clear()
            self.cb_model.clear()
            self.read_datasets()

    def load_model(self):
        self.load_model_common(self.cb_category.currentText(),self.cb_model.currentText())

    def load_model_common(self,category,model_name):
        model_path = self.dataset_root + "/" + category+ "/models/" + model_name + ".obj"
        print(model_path)
        if os.path.exists(model_path):
            if self.pcd != None:
                self.vis.remove_geometry(self.pcd)
            self.pcd = o3d.io.read_triangle_mesh(model_path)
            self.vis.add_geometry(self.pcd)

            subject=model_name[:9]

            # read basic info
            human_body_datasets = IEEE_IC_3DBP_Dataset(dataset_folder=self.dataset_root)


            basic_info = human_body_datasets.get_subject_info(category=f'{category}', subject=f'{subject}')
            print(basic_info)

            # show list view
            self.lw_info.clear()
            list_kv=[]
            for key in basic_info:
                list_kv.append(f"{key} = {basic_info[key]}")

            self.lw_info.addItems(list_kv)

            rep_no=model_name.split("_")[2].replace("R","")

            measurement1 = human_body_datasets.get_subject_measurement(category=category, subject=subject,
                                                                       repetition_no=int(rep_no))
            print(measurement1)

            self.lw_measure.clear()
            list_kv = []
            for key in measurement1:
                list_kv.append(f"{key} = {measurement1[key]}")

            self.lw_measure.addItems(list_kv)



        else:
            QMessageBox.information(self, "Error", "This model does not exist!")
            return





    def left_load(self):
        index=self.cb_model.currentIndex()
        index=index-1

        if index<0:
            index=0
            QMessageBox.information(self,"Tip","Already first one!")
        model_name=self.cb_model.itemText(index)
        self.cb_model.setCurrentIndex(index)
        self.load_model_common(self.cb_category.currentText(),model_name)


    def right_load(self):
        index = self.cb_model.currentIndex()
        index = index + 1
        if index > self.cb_model.count()-1:
            index = self.cb_model.count()-1
            QMessageBox.information(self, "Tip", "Already last one!")
        model_name = self.cb_model.itemText(index)
        self.cb_model.setCurrentIndex(index)
        self.load_model_common(self.cb_category.currentText(), model_name)

    def update_vis(self):
        #self.vis.update_geometry()
        self.vis.poll_events()
        self.vis.update_renderer()



def GUIHumanBodyShapeViewerApp():
    app = QApplication(sys.argv)

    myWin = GUIHumanBodyShapeViewer3D()
    myWin.show()
    try:
        r = app.exec_()
    except Exception as err:
        print(err)

if __name__ == "__main__":
   GUIHumanBodyShapeViewerApp()
