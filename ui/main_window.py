import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QTabWidget, QPushButton, QLabel, QApplication
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from ui.inventory_tab import InventoryTab
from ui.sales_tab import SalesTab
from ui.customers_tab import CustomersTab
from ui.settings_tab import SettingsTab
from ui.analytics_tab import AnalyticsTab
from core.config import Config

def resource_path(relative_path):
    """Получает абсолютный путь к ресурсу, работает как в разработке, так и в EXE"""
    if hasattr(sys, '_MEIPASS'):
        # Если запущено из EXE, используем временную папку PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Если запущено из исходного кода, используем относительный путь
        return os.path.join(os.path.abspath("."), relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер аптеки")
        self.setMinimumSize(1000, 600)

        self.config = Config()

        # Основной контейнер
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Боковая панель
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = QLabel("Менеджер аптеки")
        self.title.setObjectName("sidebar-title")
        sidebar_layout.addWidget(self.title)

        self.inventory_btn = QPushButton("Запасы")
        self.sales_btn = QPushButton("Продажи")
        self.customers_btn = QPushButton("Клиенты")
        self.analytics_btn = QPushButton("Аналитика")
        self.settings_btn = QPushButton("Настройки")

        for btn in [self.inventory_btn, self.sales_btn, self.customers_btn, self.analytics_btn, self.settings_btn]:
            btn.setObjectName("sidebar-btn")
            sidebar_layout.addWidget(btn)

        main_layout.addWidget(sidebar, 1)

        # Основная область с вкладками
        self.tabs = QTabWidget()
        self.tabs.setObjectName("main-tabs")
        self.inventory_tab = InventoryTab()
        self.sales_tab = SalesTab()
        self.customers_tab = CustomersTab()
        self.analytics_tab = AnalyticsTab()
        self.settings_tab = SettingsTab(parent=self)

        self.tabs.addTab(self.inventory_tab, "Запасы")
        self.tabs.addTab(self.sales_tab, "Продажи")
        self.tabs.addTab(self.customers_tab, "Клиенты")
        self.tabs.addTab(self.analytics_tab, "Аналитика")
        self.tabs.addTab(self.settings_tab, "Настройки")

        main_layout.addWidget(self.tabs, 4)

        # Подключение кнопок боковой панели
        self.inventory_btn.clicked.connect(lambda: self.switch_tab(0))
        self.sales_btn.clicked.connect(lambda: self.switch_tab(1))
        self.customers_btn.clicked.connect(lambda: self.switch_tab(2))
        self.analytics_btn.clicked.connect(lambda: self.switch_tab(3))
        self.settings_btn.clicked.connect(lambda: self.switch_tab(4))

        # Загрузка начальных стилей и языка
        self.update_style()
        self.update_language()

    def switch_tab(self, index):
        self.tabs.setCurrentIndex(index)
        # Анимация перехода
        animation = QPropertyAnimation(self.tabs, b"windowOpacity")
        animation.setDuration(300)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()

    def update_style(self):
        # Базовые стили (заглушка на случай ошибки)
        style = """
        QWidget {
            font-family: Arial, sans-serif;
        }
        #sidebar {
            background-color: #4A90E2;
        }
        #sidebar-title {
            font-size: 18px;
            font-weight: bold;
            color: #FFFFFF;
            padding: 10px;
        }
        #sidebar-btn {
            background-color: #4A90E2;
            color: #FFFFFF;
            padding: 10px;
            border: none;
            margin: 5px;
        }
        #sidebar-btn:hover {
            background-color: #6AB0FF;
        }
        """

        # Попытка загрузить стили из файла
        try:
            style_path = resource_path("assets/styles.qss")
            with open(style_path, "r", encoding="utf-8") as f:
                style += f.read()
        except FileNotFoundError:
            print("Предупреждение: styles.qss не найден, используются стили по умолчанию.")
        except Exception as e:
            print(f"Ошибка загрузки styles.qss: {str(e)}")

        # Получаем настройки
        theme = self.config.get("theme", "light")
        bg_color = self.config.get("bg_color", "#F5F7FA")
        font_size = self.config.get("font_size", "14px")
        button_style = self.config.get("button_style", "С тенями")

        # Применяем тему
        if theme == "dark":
            style += """
            QMainWindow {
                background-color: #1E2A44;
            }
            #sidebar {
                background-color: #2A3F6D;
            }
            #data-table {
                background-color: #2A3F6D;
            }
            #action-btn {
                background-color: #6AB0FF;
            }
            #search-input {
                background-color: #2A3F6D;
                color: #FFFFFF;
            }
            QComboBox {
                background-color: #2A3F6D;
                color: #FFFFFF;
            }
            QTabBar::tab {
                background-color: #2A3F6D;
                color: #FFFFFF;
            }
            QTabBar::tab:selected {
                background-color: #6AB0FF;
                color: #FFFFFF;
            }
            """
        else:
            style += """
            QMainWindow {
                background-color: #F5F7FA;
            }
            #sidebar {
                background-color: #4A90E2;
            }
            #data-table {
                background-color: #FFFFFF;
            }
            #action-btn {
                background-color: #4A90E2;
            }
            #search-input {
                background-color: #FFFFFF;
                color: #333333;
            }
            QComboBox {
                background-color: #FFFFFF;
                color: #333333;
            }
            QTabBar::tab {
                background-color: #D1D5DB;
                color: #333333;
            }
            QTabBar::tab:selected {
                background-color: #4A90E2;
                color: #FFFFFF;
            }
            """

        # Применяем цвет фона
        style += f"""
        QMainWindow {{
            background-color: {bg_color};
        }}
        """

        # Применяем размер шрифта
        style += f"""
        QWidget {{
            font-size: {font_size};
        }}
        QTabBar::tab {{
            font-size: {font_size};
        }}
        QComboBox {{
            font-size: {font_size};
        }}
        QPushButton {{
            font-size: {font_size};
        }}
        QLabel {{
            font-size: {font_size};
        }}
        QLineEdit {{
            font-size: {font_size};
        }}
        """

        # Применяем стиль кнопок
        if button_style == "Плоский":
            style += """
            #action-btn {
                box-shadow: none;
            }
            """
        else:
            style += """
            #action-btn {
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            }
            """

        # Применяем стили ко всему приложению
        self.setStyleSheet(style)

        # Принудительно обновляем интерфейс
        self.update()
        for tab in [self.inventory_tab, self.sales_tab, self.customers_tab, self.analytics_tab, self.settings_tab]:
            tab.update()
        QApplication.processEvents()

    def update_language(self):
        language = self.config.get("language", "Русский")
        if language == "Русский":
            self.setWindowTitle("Менеджер аптеки")
            self.title.setText("Менеджер аптеки")
            self.inventory_btn.setText("Запасы")
            self.sales_btn.setText("Продажи")
            self.customers_btn.setText("Клиенты")
            self.analytics_btn.setText("Аналитика")
            self.settings_btn.setText("Настройки")
            self.tabs.setTabText(0, "Запасы")
            self.tabs.setTabText(1, "Продажи")
            self.tabs.setTabText(2, "Клиенты")
            self.tabs.setTabText(3, "Аналитика")
            self.tabs.setTabText(4, "Настройки")
            # Обновляем текст в дочерних вкладках
            self.inventory_tab.search_input.setPlaceholderText("Поиск по названию...")
            self.sales_tab.search_input.setPlaceholderText("Поиск по дате...")
            self.customers_tab.search_input.setPlaceholderText("Поиск по имени...")
        else:
            self.setWindowTitle("Pharmacy Manager")
            self.title.setText("Pharmacy Manager")
            self.inventory_btn.setText("Inventory")
            self.sales_btn.setText("Sales")
            self.customers_btn.setText("Customers")
            self.analytics_btn.setText("Analytics")
            self.settings_btn.setText("Settings")
            self.tabs.setTabText(0, "Inventory")
            self.tabs.setTabText(1, "Sales")
            self.tabs.setTabText(2, "Customers")
            self.tabs.setTabText(3, "Analytics")
            self.tabs.setTabText(4, "Settings")
            # Обновляем текст в дочерних вкладках
            self.inventory_tab.search_input.setPlaceholderText("Search by name...")
            self.sales_tab.search_input.setPlaceholderText("Search by date...")
            self.customers_tab.search_input.setPlaceholderText("Search by name...")

        # Вызываем update_language для всех вкладок
        for tab in [self.inventory_tab, self.sales_tab, self.customers_tab, self.analytics_tab, self.settings_tab]:
            if hasattr(tab, 'update_language'):
                tab.update_language(language)
            tab.update()

        # Принудительно обновляем интерфейс
        self.update()
        QApplication.processEvents()