from threading import Thread

import PyQt5
import open3d as o3d
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from medsim3d.gui.gui_human_viewer import Ui_MainWindow
import sys
import os
import ctypes
import win32gui
import sys
from medsim3d.netlogo.simulator3d import *
from medsim3d.models.mat_converter import MatConverter
from medsim3d.models.point_csv_reader import PointCSVReader
from medsim3d.models.viewer3d import Viewer3D
from medsim3d.vhp.model_builder import *
from medsim3d.vhp.model_builder_color import ModelBuilderWithColor

myappid = 'human-viewer3d-gui' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, win, model_file):
        super().__init__()
        self.win=win
        self.model_file=model_file

    def run(self):
        """Long-running task."""
        self.win.vis.remove_geometry(self.win.pcd)
        self.win.pcd = o3d.io.read_point_cloud(self.model_file)
        self.win.vis.add_geometry(self.win.pcd)
        self.finished.emit()


class GUIHumanViewer3D(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(GUIHumanViewer3D, self).__init__(parent)
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

        self.btn_load.clicked.connect(self.load_model)
        self.btn_browse.clicked.connect(self.browse_dataset_root)

        # add items
        self.sex_list = ["Male", "Female"]
        self.cb_sex.addItems(self.sex_list)
        self.body_parts = ["head", "abdomen", "legs", "pelvis", "thighs", "thorax", "normalCT(full body)", "frozenCT(full body)"]
        self.cb_body_part.addItems(self.body_parts)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_vis)
        timer.start(1)
        self.statusbar.showMessage("Started!")
        self.dataset_root="../examples-med3dsim/datasets"
        self.edit_dataset_root.setText(self.dataset_root)

        # human model
        self.MalePNGRangeDict={
            "abdomen":[1455,1997],
            "head":[1001,1377],
            "legs":[2265,2878],
            "pelvis":[1732,2028],
            "thighs":[1732,2411],
            "thorax":[1280,1688]
        }
        self.FemalePNGRangeDict={
            "abdomen": [1432, 1909],
            "head": [1001, 1285],
            "legs": [2200, 2730],
            "pelvis": [1703, 1953],
            "thighs": [1703, 2300],
            "thorax": [1262, 1488]
        }

        self.MalePNGPrefix="a_vm"
        self.FeMalePNGPrefix="avf"
        # PNG radiological data
        self.MaleRadioRangeDict={
            "frozenCT":[1006,2882],
            "mri":[1005,7625],
            "normalCT":[1012,2832],
            "scoutCT":[2001,2004],
        }
        self.FemaleRadioRangeDict = {
           # "frozenCT": [1006, 2882],
            "mri": [1014, 7584],
            "normalCT": [1001, 2734],
           # "scoutCT": [2001, 2004],
        }

        self.slider_min.setMinimum(1000)
        self.slider_min.setMaximum(3000)
        self.slider_max.setMinimum(1000)
        self.slider_max.setMaximum(3000)

        self.slider_min.valueChanged.connect(self.updated_change)
        self.slider_max.valueChanged.connect(self.updated_change)

        self.btn_load_slices.clicked.connect(self.load_slices)

    def load_slices(self):
        sex = self.sex_list[self.cb_sex.currentIndex()]
        body_part = self.body_parts[self.cb_body_part.currentIndex()]

        if body_part.startswith("normalCT"):
            body_part = "normalCT"
        if body_part.startswith("frozenCT"):
            body_part = "frozenCT"

        self.slice_min_value = self.slider_min.value()
        self.slice_max_value = self.slider_max.value()

        if self.slice_min_value>self.slice_max_value:
            QMessageBox.information(self,"Error","the minimum value of the slider should not be larger than the maximum one.")
            return
        prefix = ""
        affix = ""
        if "CT" in body_part:
            current_range = self.MaleRadioRangeDict
            prefix="cvm"
            affix = "f"
            if sex == "Female":
                prefix = "cvf"
                current_range = self.FemaleRadioRangeDict
                affix="f"
            rr = current_range[body_part]
            min_v = rr[0]
            max_v = rr[1]
        else:
            prefix = self.MalePNGPrefix
            affix=""
            if sex == "Female":
                prefix = self.FeMalePNGPrefix
                affix="a"
            current_range = self.MalePNGRangeDict
            if sex == "Female":
                current_range = self.FemalePNGRangeDict
            rr = current_range[body_part]
            min_v = rr[0]
            max_v = rr[1]



        mb = ModelBuilder()

        root_path = self.dataset_root + f"/{sex}/{body_part}"

        print(self.slice_min_value, self.slice_max_value)

        # 3. show the normal CT of female
        '''
        list_points = mb.build(
            gender=sex,
            ct_type=body_part,
            converted_folder=root_path + "/normalCT_converted",
            edge_folder=root_path + "/normalCT_edges",
            detected_folder=root_path + "/normalCT_detected",
            output_model_path="",
            save_csv=False,
            start_v=min_v,
            end_v=max_v
        )
        '''

        if not ("CT" in body_part):
            ec_pg = ModelBuilderWithColor(
                polygon_file=f'{self.dataset_root}/{sex}/{body_part}_polygon_area.pickle',
                dataset_folder=f'{self.dataset_root}/{sex}/{body_part}',
                use_color=True
            )

            list_points=ec_pg.build(body_part=body_part,
                        save_edges_folder=f'{self.dataset_root}/{sex}/{body_part}_edges',
                        save_detected_folder=f'{self.dataset_root}/{sex}/{body_part}_edges_detected',
                        gender=sex,
                        output_model_file=f"{self.dataset_root}/{sex}/{body_part}-sliced.csv",
                                    start_v=self.slice_min_value,
                                    end_v=self.slice_max_value,
                                    save_csv=False
                        )
        else: # CT
            list_points = mb.build(
                gender=sex,
                ct_type=body_part,
                converted_folder=f'{self.dataset_root}/{sex}' + f"/{body_part}_converted",
                edge_folder=f'{self.dataset_root}/{sex}' + f"/{body_part}_edges",
                detected_folder=f'{self.dataset_root}/{sex}' + f"/{body_part}_edges_detected",
                output_model_path="",
                save_csv=False,
                start_v=self.slice_min_value,
                end_v=self.slice_max_value
            )


        self.vis.remove_geometry(self.pcd)
        self.pcd = PointCSVReader("").create_point_cloud_by_points(list_points)
        self.vis.add_geometry(self.pcd)
        # for slice_id in range(self.slice_min_value,self.slice_max_value+1):
        #     image_file = self.dataset_root+ f"/{sex}/{body_part}/{prefix}{slice_id}{affix}.png"


    def browse_dataset_root(self):
        # open select folder dialog
        fname = QFileDialog.getExistingDirectory(
            self, 'Select a directory', "")
        print(fname)
        if fname:
            self.dataset_root=fname
            self.edit_dataset_root.setText(self.dataset_root)

    def load_model(self):
        # self.statusbar.showMessage(message="Loading Model...")
        sex=self.sex_list[self.cb_sex.currentIndex()]
        body_part=self.body_parts[self.cb_body_part.currentIndex()]

        if body_part.startswith("normalCT"):
            body_part="normalCT"
        if body_part.startswith("frozenCT"):
            body_part="frozenCT"



        model_file = self.dataset_root+ f"/{sex}/{body_part}.ply"
        if not os.path.exists(model_file):
            QMessageBox.information(self,"Error","File does not exist!")
            return

        # find min and max values


        if "CT" in body_part:
            gender = "Male"
            current_range = self.MaleRadioRangeDict
            if gender == "Female":
                prefix = "cvf"
                current_range = self.FemaleRadioRangeDict
            rr = current_range[body_part]
            min_v = rr[0]
            max_v = rr[1]
        else:
            gender = "Male"
            prefix = self.MalePNGPrefix
            if gender == "Female":
                prefix = self.FeMalePNGPrefix
            current_range = self.MalePNGRangeDict
            if gender == "Female":
                current_range = self.FemalePNGRangeDict
            rr = current_range[body_part]
            min_v = rr[0]
            max_v = rr[1]

        self.slider_min.setMinimum(min_v)
        self.slider_min.setMaximum(max_v)
        self.slider_max.setMinimum(min_v)
        self.slider_max.setMaximum(max_v)


        self.slider_min.setValue(min_v)
        self.slider_max.setValue(max_v)


        self.vis.remove_geometry(self.pcd)
        self.pcd = o3d.io.read_point_cloud(model_file)
        self.vis.add_geometry(self.pcd)
        # self.update_vis()
        # QMessageBox.information(self,"Tips","Loaded!")



        # t1 = Thread(target=self.Operation)
        # t1.start()

    def updated_change(self):
        self.slice_min_value=self.slider_min.value()
        self.slice_max_value=self.slider_max.value()
        self.lb_range.setText(f"[{self.slice_min_value}, {self.slice_max_value}]")

    def Operation(self):
        self.statusbar.showMessage(message="Loaded Model!")


    def update_vis(self):
        #self.vis.update_geometry()
        self.vis.poll_events()
        self.vis.update_renderer()

def GUIHuman3DViewerApp():
    app = QApplication(sys.argv)

    myWin = GUIHumanViewer3D()
    myWin.show()
    try:
        r = app.exec_()
    except Exception as err:
        print(err)

if __name__ == "__main__":
   GUIHuman3DViewerApp()
