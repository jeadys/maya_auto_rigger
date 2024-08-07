from maya import OpenMayaUI
from shiboken2 import wrapInstance
from PySide2 import QtCore, QtWidgets

from ui.widgets.combobox import create_combobox
from ui.widgets.spinbox import create_spinbox

from utilities.unload_packages import unload_packages

from ui.actions.build_rig import build_rig
from ui.actions.build_blueprint import build_blueprint
from ui.actions.tree_view import tree_view, node_widget, segment_widget, connect_button, delete_button

from data.write_data import export_rig_data
from data.read_data import import_rig_data


class MayaUITemplate(QtWidgets.QWidget):
    window = None

    def __init__(self, parent=None):
        super(MayaUITemplate, self).__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.resize(750, 500)

        main_layout = QtWidgets.QHBoxLayout(self)

        hierarchy_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(hierarchy_layout)
        hierarchy_layout.addWidget(tree_view)

        settings_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(settings_layout)

        module_group = QtWidgets.QGroupBox("modules")
        module_layout = QtWidgets.QVBoxLayout()
        module_group.setLayout(module_layout)
        settings_layout.addWidget(module_group)

        limb_modules: list[str] = ["arm", "leg", "spine", "front_leg", "rear_leg", "quadrupled_spine", "arachne_leg",
                                   "wing", "head", "hand", "face", "thumb_finger", "index_finger", "middle_finger",
                                   "ring_finger", "pinky_finger", "index_toe", "middle_toe", "ring_toe", "pinky_toe"]
        limb_module_widget, self.limb_module_combobox = create_combobox(name="Module", items=limb_modules)
        # self.limb_module_combobox.currentTextChanged.connect(self.limb_changed)
        module_layout.addWidget(limb_module_widget)

        # self.finger_count_widget, self.finger_count_slider = create_slider(name="finger count", value=5, minimum=1,
        #                                                                    maximum=5)
        # module_layout.addWidget(self.finger_count_widget)
        #
        # self.spine_count_widget, self.spine_count_slider = create_slider(name="spine count", value=5, minimum=5,
        #                                                                  maximum=10)
        # self.spine_count_widget.setVisible(False)
        # module_layout.addWidget(self.spine_count_widget)

        offset_layout = QtWidgets.QVBoxLayout()

        offset_layout.addWidget(node_widget)
        offset_layout.addWidget(segment_widget)

        self.x_offset_widget, self.x_offset_spinbox = create_spinbox(name="x offset", value=0, minimum=-100,
                                                                     maximum=100)
        self.y_offset_widget, self.y_offset_spinbox = create_spinbox(name="y offset", value=0, minimum=-100,
                                                                     maximum=100)
        self.z_offset_widget, self.z_offset_spinbox = create_spinbox(name="z offset", value=0, minimum=-100,
                                                                     maximum=100)
        offset_layout.addWidget(self.x_offset_widget)
        offset_layout.addWidget(self.y_offset_widget)
        offset_layout.addWidget(self.z_offset_widget)
        module_layout.addLayout(offset_layout)

        # orientation_group = QtWidgets.QGroupBox("orientations")
        # orientation_layout = QtWidgets.QVBoxLayout()
        # orientation_group.setLayout(orientation_layout)
        # main_layout.addWidget(orientation_group)
        #
        # rotation_orders: list[str] = ["XYZ", "YZX", "ZXY", "ZYX", "YXZ", "XZY"]
        # rotation_order_widget, self.rotation_order_combobox = create_combobox(name="rotation order",
        #                                                                       items=rotation_orders)
        # orientation_layout.addWidget(rotation_order_widget)
        #
        # joint_orientations: list[str] = ["yzx - zup"]
        # joint_orientation_widget, self.joint_orientation_combobox = create_combobox(name="joint orientation",
        #                                                                             items=joint_orientations)
        # orientation_layout.addWidget(joint_orientation_widget)

        # mechanism_group = QtWidgets.QGroupBox("kinematics")
        # mechanism_layout = QtWidgets.QVBoxLayout()
        # mechanism_group.setLayout(mechanism_layout)
        # main_layout.addWidget(mechanism_group)
        #
        # twist_widget, self.twist_checkbox = create_checkbox(name="twist", is_checked=True)
        # mechanism_layout.addWidget(twist_widget)
        #
        # stretch_widget, self.stretch_checkbox = create_checkbox(name="stretch", is_checked=True)
        # mechanism_layout.addWidget(stretch_widget)

        operation_group = QtWidgets.QGroupBox("operations")
        operation_layout = QtWidgets.QVBoxLayout()
        operation_group.setLayout(operation_layout)
        settings_layout.addWidget(operation_group)

        export_rig_button = QtWidgets.QPushButton("export rig")
        export_rig_button.clicked.connect(export_rig_data)
        operation_layout.addWidget(export_rig_button)

        import_rig_button = QtWidgets.QPushButton("import rig")
        import_rig_button.clicked.connect(import_rig_data)
        operation_layout.addWidget(import_rig_button)

        blueprint_button = QtWidgets.QPushButton("build blueprint")
        blueprint_button.clicked.connect(lambda: build_blueprint(self.limb_module_combobox.currentText()))
        operation_layout.addWidget(blueprint_button)

        rig_button = QtWidgets.QPushButton("build rig")
        rig_button.clicked.connect(build_rig)
        operation_layout.addWidget(rig_button)

        operation_layout.addWidget(connect_button)
        operation_layout.addWidget(delete_button)

    def limb_changed(self):
        if self.limb_module_combobox.currentText() == "arm":
            self.finger_count_widget.setVisible(True)
            self.spine_count_widget.setVisible(False)
        elif self.limb_module_combobox.currentText() == "spine":
            self.spine_count_widget.setVisible(True)
            self.finger_count_widget.setVisible(False)
        else:
            self.spine_count_widget.setVisible(False)
            self.finger_count_widget.setVisible(False)


def open_window():
    if QtWidgets.QApplication.instance():
        for win in (QtWidgets.QApplication.allWindows()):
            if 'auto_rig' in win.objectName():
                win.destroy()

    maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)
    MayaUITemplate.window = MayaUITemplate(parent=maya_main_window)
    MayaUITemplate.window.setObjectName('auto_rig')
    MayaUITemplate.window.setWindowTitle('Maya Auto Rig')
    MayaUITemplate.window.show()


if __name__ == "__main__":
    DEBUG = True
    if DEBUG:
        unload_packages(silent=False,
                        packages=["segments", "joints", "rig", "kinematics", "kinematics", "utilities", "ui",
                                  "rig", "helpers", "data"])
    open_window()
