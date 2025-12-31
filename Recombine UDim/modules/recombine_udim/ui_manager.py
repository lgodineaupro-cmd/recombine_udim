from PySide2 import QtWidgets
from substance_painter import ui
from .recombine_manager import RecombineManager

_window = None
_manager = None

def start():
    global _window, _manager
    if _window is None:
        _manager = RecombineManager()
        _window = QtWidgets.QWidget()
        _window.setWindowTitle("Recombine UDim")
        layout = QtWidgets.QVBoxLayout(_window)
        btn_export = QtWidgets.QPushButton("Run export + recombine")
        layout.addWidget(btn_export)
        btn_export.clicked.connect(_on_run)
        ui.add_dock_widget(_window, "Recombine UDim")
    _window.show()

def close():
    global _window
    if _window is not None:
        _window.close()
        _window = None

def _on_run():
    # Minimal interaction: open a file dialog for JSON config (user will implement)
    dlg = QtWidgets.QFileDialog()
    path, _ = dlg.getOpenFileName(None, "Select export JSON config", "", "JSON Files (*.json);;All Files (*)")
    if not path:
        return
    # Load JSON and call manager (left as exercise)
    QtWidgets.QMessageBox.information(None, "Recombine UDim", "Selected: {}\nImplementation pending.".format(path))
