# Recombine UDim - plugin entry
import substance_painter.plugins as plugins
from modules.recombine_udim import ui_manager

def start_plugin():
    ui_manager.start()

def close_plugin():
    ui_manager.close()

# For reload convenience
def reload_plugin():
    close_plugin()
    start_plugin()
