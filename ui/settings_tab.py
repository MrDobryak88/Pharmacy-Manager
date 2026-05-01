import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QColorDialog, QComboBox, QLabel
from core.config import Config

class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout()

        # Переключение темы
        self.theme_label = QLabel("Тема приложения:")  # Явно определяем атрибут
        layout.addWidget(self.theme_label)
        self.theme_btn = QPushButton("Переключить тему")
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)

        # Выбор цвета фона
        self.color_label = QLabel("Цвет фона:")  # Явно определяем атрибут
        layout.addWidget(self.color_label)
        self.color_btn = QPushButton("Выбрать цвет фона")
        self.color_btn.clicked.connect(self.show_color_picker)
        layout.addWidget(self.color_btn)

        # Выбор размера шрифта
        self.font_size_label = QLabel("Размер шрифта:")  # Явно определяем атрибут
        layout.addWidget(self.font_size_label)
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["12px", "14px", "16px"])
        self.font_size_combo.currentTextChanged.connect(self.change_font_size)
        layout.addWidget(self.font_size_combo)

        # Выбор стиля кнопок
        self.button_style_label = QLabel("Стиль кнопок:")  # Явно определяем атрибут
        layout.addWidget(self.button_style_label)
        self.button_style_combo = QComboBox()
        self.button_style_combo.addItems(["Плоский", "С тенями"])
        self.button_style_combo.currentTextChanged.connect(self.change_button_style)
        layout.addWidget(self.button_style_combo)

        # Выбор языка
        self.language_label = QLabel("Язык интерфейса:")  # Явно определяем атрибут
        layout.addWidget(self.language_label)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Русский", "English"])
        self.language_combo.currentTextChanged.connect(self.change_language)
        layout.addWidget(self.language_combo)

        # Сброс настроек
        self.reset_btn = QPushButton("Сбросить настройки")
        self.reset_btn.clicked.connect(self.reset_settings)
        layout.addWidget(self.reset_btn)

        self.setLayout(layout)
        self.config = Config()

        # Инициализируем текущий язык
        self.current_language = "Русский"

        # Загружаем сохранённые настройки
        self.load_settings()

    def load_settings(self):
        # Устанавливаем сохранённый размер шрифта
        font_size = self.config.get("font_size", "14px")
        self.font_size_combo.setCurrentText(font_size)

        # Устанавливаем сохранённый стиль кнопок
        button_style = self.config.get("button_style", "С тенями")
        self.button_style_combo.setCurrentText(button_style)

        # Устанавливаем сохранённый язык
        language = self.config.get("language", "Русский")
        self.language_combo.setCurrentText(language)
        self.current_language = language
        self.update_language(language)  # Обновляем текст при загрузке

    def toggle_theme(self):
        current_theme = self.config.get("theme", "light")
        new_theme = "dark" if current_theme == "light" else "light"
        self.config.set("theme", new_theme)
        self.parent.update_style()
        translations = self.get_translations()
        QMessageBox.information(self, translations[self.current_language]["Успех"],
                                translations[self.current_language]["Тема изменена на"].format(new_theme))

    def show_color_picker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.config.set("bg_color", color.name())
            self.parent.update_style()
            translations = self.get_translations()
            QMessageBox.information(self, translations[self.current_language]["Успех"],
                                    translations[self.current_language]["Цвет фона изменён"])

    def change_font_size(self, font_size):
        self.config.set("font_size", font_size)
        self.parent.update_style()
        translations = self.get_translations()
        QMessageBox.information(self, translations[self.current_language]["Успех"],
                                translations[self.current_language]["Размер шрифта изменён на"].format(font_size))

    def change_button_style(self, style):
        self.config.set("button_style", style)
        self.parent.update_style()
        translations = self.get_translations()
        QMessageBox.information(self, translations[self.current_language]["Успех"],
                                translations[self.current_language]["Стиль кнопок изменён на"].format(style))

    def change_language(self, language):
        self.config.set("language", language)
        self.current_language = language
        self.parent.update_language()
        translations = self.get_translations()
        QMessageBox.information(self, translations[self.current_language]["Успех"],
                                translations[self.current_language]["Язык изменён на"].format(language))

    def reset_settings(self):
        self.config.set("theme", "light")
        self.config.set("bg_color", "#F5F7FA")
        self.config.set("font_size", "14px")
        self.config.set("button_style", "С тенями")
        self.config.set("language", "Русский")
        self.font_size_combo.setCurrentText("14px")
        self.button_style_combo.setCurrentText("С тенями")
        self.language_combo.setCurrentText("Русский")
        self.current_language = "Русский"
        self.parent.update_style()
        self.parent.update_language()
        translations = self.get_translations()
        QMessageBox.information(self, translations[self.current_language]["Успех"],
                                translations[self.current_language]["Настройки сброшены"])

    def update_language(self, language):
        translations = self.get_translations()
        self.current_language = language
        self.theme_label.setText(translations[language]["Тема приложения:"])
        self.theme_btn.setText(translations[language]["Переключить тему"])
        self.color_label.setText(translations[language]["Цвет фона:"])
        self.color_btn.setText(translations[language]["Выбрать цвет фона"])
        self.font_size_label.setText(translations[language]["Размер шрифта:"])
        self.button_style_label.setText(translations[language]["Стиль кнопок:"])
        self.language_label.setText(translations[language]["Язык интерфейса:"])
        self.reset_btn.setText(translations[language]["Сбросить настройки"])

    def get_translations(self):
        return {
            "Русский": {
                "Тема приложения:": "Тема приложения:",
                "Переключить тему": "Переключить тему",
                "Цвет фона:": "Цвет фона:",
                "Выбрать цвет фона": "Выбрать цвет фона",
                "Размер шрифта:": "Размер шрифта:",
                "Стиль кнопок:": "Стиль кнопок:",
                "Язык интерфейса:": "Язык интерфейса:",
                "Сбросить настройки": "Сбросить настройки",
                "Успех": "Успех",
                "Тема изменена на": "Тема изменена на {}",
                "Цвет фона изменён": "Цвет фона изменён",
                "Размер шрифта изменён на": "Размер шрифта изменён на {}",
                "Стиль кнопок изменён на": "Стиль кнопок изменён на {}",
                "Язык изменён на": "Язык изменён на {}",
                "Настройки сброшены": "Настройки сброшены",
            },
            "English": {
                "Тема приложения:": "Application Theme:",
                "Переключить тему": "Toggle Theme",
                "Цвет фона:": "Background Color:",
                "Выбрать цвет фона": "Choose Background Color",
                "Размер шрифта:": "Font Size:",
                "Стиль кнопок:": "Button Style:",
                "Язык интерфейса:": "Interface Language:",
                "Сбросить настройки": "Reset Settings",
                "Успех": "Success",
                "Тема изменена на": "Theme changed to {}",
                "Цвет фона изменён": "Background color changed",
                "Размер шрифта изменён на": "Font size changed to {}",
                "Стиль кнопок изменён на": "Button style changed to {}",
                "Язык изменён на": "Language changed to {}",
                "Настройки сброшены": "Settings reset",
            }
        }