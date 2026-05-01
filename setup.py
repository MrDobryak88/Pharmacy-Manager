import PyInstaller.__main__
import os
import sys

# Set the working directory to the script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Define base path (project root)
base_path = os.path.abspath(os.path.dirname(__file__))

# Define paths to data files
assets_path = os.path.join(base_path, "assets")
config_path = os.path.join(base_path, "config.json")
db_path = os.path.join(base_path, "pharmacy.db")
csv_path = os.path.join(base_path, "inventory.csv")

# Separator for PyInstaller --add-data (platform-dependent)
sep = os.pathsep

# PyInstaller arguments
PyInstaller.__main__.run([
    "--name=PharmacyManager",
    f"--add-data={os.path.join(assets_path, 'logo.png')}{sep}assets",
    f"--add-data={os.path.join(assets_path, 'styles.qss')}{sep}assets",
    f"--add-data={config_path}{sep}.",
    f"--add-data={db_path}{sep}.",
    f"--add-data={csv_path}{sep}.",
    "--collect-all=PySide6.QtCore",
    "--collect-all=PySide6.QtGui",
    "--collect-all=PySide6.QtWidgets",
    "--hidden-import=matplotlib.backends.backend_qtagg",
    "--hidden-import=numpy.core",
    "--exclude-module=PySide6.Qt3DAnimation",
    "--exclude-module=PySide6.Qt3DCore",
    "--exclude-module=PySide6.Qt3DRender",
    "--exclude-module=PySide6.Qt3DInput",
    "--exclude-module=PySide6.Qt3DLogic",
    "--exclude-module=PySide6.Qt3DExtras",
    "--exclude-module=PySide6.QtAxContainer",
    "--exclude-module=PySide6.QtBluetooth",
    "--exclude-module=PySide6.QtCharts",
    "--exclude-module=PySide6.QtConcurrent",
    "--exclude-module=PySide6.QtDBus",
    "--exclude-module=PySide6.QtDataVisualization",
    "--exclude-module=PySide6.QtDesigner",
    "--exclude-module=PySide6.QtExampleIcons",
    "--exclude-module=PySide6.QtGraphs",
    "--exclude-module=PySide6.QtGraphsWidgets",
    "--exclude-module=PySide6.QtHelp",
    "--exclude-module=PySide6.QtHttpServer",
    "--exclude-module=PySide6.QtLocation",
    "--exclude-module=PySide6.QtMultimedia",
    "--exclude-module=PySide6.QtMultimediaWidgets",
    "--exclude-module=PySide6.QtNetworkAuth",
    "--exclude-module=PySide6.QtNfc",
    "--exclude-module=PySide6.QtOpenGL",
    "--exclude-module=PySide6.QtOpenGLWidgets",
    "--exclude-module=PySide6.QtPdf",
    "--exclude-module=PySide6.QtPdfWidgets",
    "--exclude-module=PySide6.QtPositioning",
    "--exclude-module=PySide6.QtPrintSupport",
    "--exclude-module=PySide6.QtQuick",
    "--exclude-module=PySide6.QtQuickControls2",
    "--exclude-module=PySide6.QtQuickTest",
    "--exclude-module=PySide6.QtQuickWidgets",
    "--exclude-module=PySide6.QtRemoteObjects",
    "--exclude-module=PySide6.QtScxml",
    "--exclude-module=PySide6.QtSensors",
    "--exclude-module=PySide6.QtSerialBus",
    "--exclude-module=PySide6.QtSerialPort",
    "--exclude-module=PySide6.QtSpatialAudio",
    "--exclude-module=PySide6.QtSql",
    "--exclude-module=PySide6.QtStateMachine",
    "--exclude-module=PySide6.QtSvg",
    "--exclude-module=PySide6.QtSvgWidgets",
    "--exclude-module=PySide6.QtTest",
    "--exclude-module=PySide6.QtTextToSpeech",
    "--exclude-module=PySide6.QtUiTools",
    "--exclude-module=PySide6.QtWebChannel",
    "--exclude-module=PySide6.QtWebEngineCore",
    "--exclude-module=PySide6.QtWebEngineQuick",
    "--exclude-module=PySide6.QtWebEngineWidgets",
    "--exclude-module=PySide6.QtWebSockets",
    "--exclude-module=PySide6.QtWebView",
    "--exclude-module=PySide6.QtXml",
    "--exclude-module=matplotlib.tests",
    "--exclude-module=numpy.f2py.tests",
    "--exclude-module=pygame",
    "--noconfirm",
    "--noconsole",
    os.path.join(base_path, "main.py")
])