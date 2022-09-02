import PyQt5
import open3d as o3d
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from gui_viewer import Ui_MainWindow
import sys
import os
import ctypes
import win32gui
import sys
from medsim3d.netlogo.simulator3d import *
from medsim3d.models.mat_converter import MatConverter
from medsim3d.models.point_csv_reader import PointCSVReader
from medsim3d.models.viewer3d import Viewer3D

myappid = 'viewer3d-gui' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class GUIViewer3D(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(GUIViewer3D, self).__init__(parent)
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

        self.btn_load_ply.clicked.connect(self.load_ply)
        self.btn_load_male.clicked.connect(self.load_male)
        self.btn_load_chair.clicked.connect(self.load_chair)
        self.btn_start_netlogo.clicked.connect(self.start_netlogo)
        self.btn_close_netlogo.clicked.connect(self.close_netlogo)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_vis)
        timer.start(1)

        self.sim3d=None
        self.rel_path="datasets/chair.ply"

    def start_netlogo(self):

        if not os.path.exists(self.rel_path):
            QMessageBox.information(self,"Tip","Please select a valid model file and display it into the screen. ")
            return

        # model_file = '../examples-med3dsim/datasets/Female/pelvis.ply'

        self.sim3d = NetLogo3DSim(netlogo_model_name="MedSim3D-0.0.1a2.nlogo3d")

        abs_path = os.path.abspath(self.rel_path)
        abs_path = abs_path.replace("\\", "/")

        config_model = self.sim3d.predict_3dworld_size(model_path=abs_path)

        # print(config_model)

        config_model["world-min-z"] = -5
        config_model["world-max-z"] = 5

        self.sim3d.run_model(model_path=abs_path,
                        scale=config_model["scale"],
                        size_scale=config_model["size-scale"],
                        sample_rate=config_model["sample-rate"],
                        offset_x=config_model["offset-x"],
                        offset_y=config_model["offset-y"],
                        offset_z=config_model["offset-z"],
                        world_min_x=config_model["world-min-x"],
                        world_max_x=config_model["world-max-x"],
                        world_min_y=config_model["world-min-y"],
                        world_max_y=config_model["world-max-y"],
                        world_min_z=config_model["world-min-z"],
                        world_max_z=config_model["world-max-z"],
                        auto_world_resize=True
                        )

    def close_netlogo(self):
        if self.sim3d!=None:
            self.sim3d.close()

    def load_ply(self):
        root_path="datasets"
        if not  os.path.exists(root_path):
            root_path=""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Open a PLY file", root_path,
                                                  "All Files (*);;Polygon File Format (*.ply);CSV Format (*.csv);Object File Format (*.off);Wavefront Object (*.obj)", options=options)

        if file_path:
            file_name = os.path.basename(file_path)
            print(root_path+"/"+file_name)
            if root_path!="":
                self.rel_path=root_path+"/"+file_name
            else:
                self.rel_path=file_name

            self.vis.remove_geometry(self.pcd)
            if self.pcd!=None:
                self.vis.remove_geometry(self.pcd)
            if file_name.endswith(".csv"):

                self.pcd=PointCSVReader(model_file=self.rel_path).read_to_colored_point_cloud()
                self.vis.add_geometry(self.pcd)
            elif file_name.endswith(".mat"):

                self.pcd=MatConverter(mat_path=self.rel_path).to_mesh_obj()
                self.vis.add_geometry(self.pcd)
            elif file_name.endswith(".off"):

                self.pcd = o3d.io.read_triangle_mesh(self.rel_path)
                self.vis.add_geometry(self.pcd)
            elif file_name.endswith(".obj"):

                self.pcd = o3d.io.read_triangle_mesh(self.rel_path)
                self.vis.add_geometry(self.pcd)
            elif file_name.endswith(".ply"):

                self.pcd = o3d.io.read_point_cloud(self.rel_path)
                self.vis.add_geometry(self.pcd)
            else:
                QMessageBox.information(self,"Tips","The selected file type is not supported!")

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

    myWin = GUIViewer3D()
    myWin.show()
    try:
        r = app.exec_()
    except Exception as err:
        print(err)

if __name__ == "__main__":
   main()
