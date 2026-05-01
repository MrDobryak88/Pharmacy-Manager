import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QFormLayout, QDialog, QLineEdit, QHBoxLayout, QTableWidgetItem, QMessageBox, QFileDialog
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from core.database import Database
import csv

class InventoryTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Поиск
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию...")
        self.search_input.setObjectName("search-input")
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Количество", "Цена"])
        self.table.setObjectName("data-table")
        layout.addWidget(self.table)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить товар")
        self.edit_btn = QPushButton("Редактировать")
        self.delete_btn = QPushButton("Удалить")
        self.export_btn = QPushButton("Экспорт в CSV")
        for btn in [self.add_btn, self.edit_btn, self.delete_btn, self.export_btn]:
            btn.setObjectName("action-btn")
            buttons_layout.addWidget(btn)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Подключение событий
        self.load_inventory()
        self.add_btn.clicked.connect(self.show_add_dialog)
        self.edit_btn.clicked.connect(self.show_edit_dialog)
        self.delete_btn.clicked.connect(self.delete_product)
        self.export_btn.clicked.connect(self.export_to_csv)
        self.search_input.textChanged.connect(self.filter_inventory)

    def load_inventory(self):
        db = Database()
        products = db.get_all_products()
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product[0])))
            self.table.setItem(row, 1, QTableWidgetItem(product[1]))
            self.table.setItem(row, 2, QTableWidgetItem(str(product[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(product[3])))
            if product[2] < 10:
                for col in range(4):
                    item = self.table.item(row, col)
                    item.setForeground(Qt.red)

    def filter_inventory(self):
        search_text = self.search_input.text().lower()
        db = Database()
        products = db.get_all_products()
        filtered_products = [p for p in products if search_text in p[1].lower()]
        self.table.setRowCount(len(filtered_products))
        for row, product in enumerate(filtered_products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product[0])))
            self.table.setItem(row, 1, QTableWidgetItem(product[1]))
            self.table.setItem(row, 2, QTableWidgetItem(str(product[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(product[3])))
            if product[2] < 10:
                for col in range(4):
                    item = self.table.item(row, col)
                    item.setForeground(Qt.red)

    def show_add_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить товар")
        dialog.setObjectName("dialog")
        layout = QFormLayout()

        name_edit = QLineEdit()
        quantity_edit = QLineEdit()
        price_edit = QLineEdit()
        layout.addRow("Название:", name_edit)
        layout.addRow("Количество:", quantity_edit)
        layout.addRow("Цена:", price_edit)

        ok_btn = QPushButton("Добавить")
        ok_btn.setObjectName("action-btn")
        layout.addWidget(ok_btn)

        dialog.setLayout(layout)

        # Анимация появления
        dialog.setWindowOpacity(0)
        animation = QPropertyAnimation(dialog, b"windowOpacity")
        animation.setDuration(300)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()

        ok_btn.clicked.connect(lambda: self.add_product(name_edit.text(), quantity_edit.text(), price_edit.text(), dialog))
        dialog.exec()

    def add_product(self, name, quantity, price, dialog):
        try:
            quantity = int(quantity)
            price = float(price)
            if not name:
                raise ValueError("Название не может быть пустым.")
            db = Database()
            db.add_product(name, quantity, price)
            QMessageBox.information(self, "Успех", "Товар добавлен!")
            dialog.accept()
            self.load_inventory()
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить товар: {str(e)}")

    def show_edit_dialog(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для редактирования.")
            return

        product_id = int(self.table.item(selected, 0).text())
        db = Database()
        product = db.get_product(product_id)

        dialog = QDialog(self)
        dialog.setWindowTitle("Редактировать товар")
        dialog.setObjectName("dialog")
        layout = QFormLayout()

        name_edit = QLineEdit(product[1])
        quantity_edit = QLineEdit(str(product[2]))
        price_edit = QLineEdit(str(product[3]))
        layout.addRow("Название:", name_edit)
        layout.addRow("Количество:", quantity_edit)
        layout.addRow("Цена:", price_edit)

        ok_btn = QPushButton("Сохранить")
        ok_btn.setObjectName("action-btn")
        layout.addWidget(ok_btn)

        dialog.setLayout(layout)

        # Анимация появления
        dialog.setWindowOpacity(0)
        animation = QPropertyAnimation(dialog, b"windowOpacity")
        animation.setDuration(300)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()

        ok_btn.clicked.connect(lambda: self.edit_product(product_id, name_edit.text(), quantity_edit.text(), price_edit.text(), dialog))
        dialog.exec()

    def edit_product(self, product_id, name, quantity, price, dialog):
        try:
            quantity = int(quantity)
            price = float(price)
            if not name:
                raise ValueError("Название не может быть пустым.")
            db = Database()
            db.update_product(product_id, name, quantity, price)
            QMessageBox.information(self, "Успех", "Товар обновлён!")
            dialog.accept()
            self.load_inventory()
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить товар: {str(e)}")

    def delete_product(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для удаления.")
            return

        product_id = int(self.table.item(selected, 0).text())
        reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить этот товар?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                db = Database()
                db.delete_product(product_id)
                QMessageBox.information(self, "Успех", "Товар удалён!")
                self.load_inventory()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить товар: {str(e)}")

    def update_language(self, language):
        translations = self.get_translations()
        self.search_input.setPlaceholderText(translations[language]["Поиск по названию..."])
        self.table.setHorizontalHeaderLabels([
            translations[language]["ID"],
            translations[language]["Название"],
            translations[language]["Количество"],
            translations[language]["Цена"]
        ])
        self.add_btn.setText(translations[language]["Добавить товар"])
        self.edit_btn.setText(translations[language]["Редактировать"])
        self.delete_btn.setText(translations[language]["Удалить"])
        self.export_btn.setText(translations[language]["Экспорт в CSV"])

        # Обновляем текст в диалогах (динамически)
        self.current_language = language  # Сохраняем текущий язык для диалогов

    def get_translations(self):
        return {
            "Русский": {
                "Поиск по названию...": "Поиск по названию...",
                "ID": "ID",
                "Название": "Название",
                "Количество": "Количество",
                "Цена": "Цена",
                "Добавить товар": "Добавить товар",
                "Редактировать": "Редактировать",
                "Удалить": "Удалить",
                "Экспорт в CSV": "Экспорт в CSV",
                "Название не может быть пустым.": "Название не может быть пустым.",
                "Успех": "Успех",
                "Товар добавлен!": "Товар добавлен!",
                "Ошибка": "Ошибка",
                "Выберите товар для редактирования.": "Выберите товар для редактирования.",
                "Добавить": "Добавить",
                "Сохранить": "Сохранить",
                "Товар обновлён!": "Товар обновлён!",
                "Выберите товар для удаления.": "Выберите товар для удаления.",
                "Подтверждение": "Подтверждение",
                "Вы уверены, что хотите удалить этот товар?": "Вы уверены, что хотите удалить этот товар?",
                "Товар удалён!": "Товар удалён!",
                "Данные экспортированы": "Данные экспортированы в {}",
            },
            "English": {
                "Поиск по названию...": "Search by name...",
                "ID": "ID",
                "Название": "Name",
                "Количество": "Quantity",
                "Цена": "Price",
                "Добавить товар": "Add Product",
                "Редактировать": "Edit",
                "Удалить": "Delete",
                "Экспорт в CSV": "Export to CSV",
                "Название не может быть пустым.": "Name cannot be empty.",
                "Успех": "Success",
                "Товар добавлен!": "Product added!",
                "Ошибка": "Error",
                "Выберите товар для редактирования.": "Select a product to edit.",
                "Добавить": "Add",
                "Сохранить": "Save",
                "Товар обновлён!": "Product updated!",
                "Выберите товар для удаления.": "Select a product to delete.",
                "Подтверждение": "Confirmation",
                "Вы уверены, что хотите удалить этот товар?": "Are you sure you want to delete this product?",
                "Товар удалён!": "Product deleted!",
                "Данные экспортированы": "Data exported to {}",
            }
        }

    def export_to_csv(self):
        db = Database()
        products = db.get_all_products()
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Название", "Количество", "Цена"])
                    for product in products:
                        writer.writerow(product)
                translations = self.get_translations()
                QMessageBox.information(self, translations[self.current_language]["Успех"],
                                        translations[self.current_language]["Данные экспортированы"].format(file_path))
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать данные: {str(e)}")