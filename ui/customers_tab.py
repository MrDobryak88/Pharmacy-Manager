import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QFormLayout, QDialog, QLineEdit, QHBoxLayout, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from core.database import Database

class CustomersTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Поиск
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по имени...")
        self.search_input.setObjectName("search-input")
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Имя", "Контакт", "Адрес"])
        self.table.setObjectName("data-table")
        layout.addWidget(self.table)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить клиента")
        self.edit_btn = QPushButton("Редактировать")
        self.delete_btn = QPushButton("Удалить")
        for btn in [self.add_btn, self.edit_btn, self.delete_btn]:
            btn.setObjectName("action-btn")
            buttons_layout.addWidget(btn)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.load_customers()
        self.add_btn.clicked.connect(self.show_add_dialog)
        self.edit_btn.clicked.connect(self.show_edit_dialog)
        self.delete_btn.clicked.connect(self.delete_customer)
        self.search_input.textChanged.connect(self.filter_customers)

    def load_customers(self):
        db = Database()
        customers = db.get_all_customers()
        self.table.setRowCount(len(customers))
        for row, customer in enumerate(customers):
            self.table.setItem(row, 0, QTableWidgetItem(str(customer[0])))
            self.table.setItem(row, 1, QTableWidgetItem(customer[1]))
            self.table.setItem(row, 2, QTableWidgetItem(customer[2]))
            self.table.setItem(row, 3, QTableWidgetItem(customer[3]))

    def filter_customers(self):
        search_text = self.search_input.text().lower()
        db = Database()
        customers = db.get_all_customers()
        filtered_customers = [c for c in customers if search_text in c[1].lower()]
        self.table.setRowCount(len(filtered_customers))
        for row, customer in enumerate(filtered_customers):
            self.table.setItem(row, 0, QTableWidgetItem(str(customer[0])))
            self.table.setItem(row, 1, QTableWidgetItem(customer[1]))
            self.table.setItem(row, 2, QTableWidgetItem(customer[2]))
            self.table.setItem(row, 3, QTableWidgetItem(customer[3]))

    def show_add_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить клиента")
        dialog.setObjectName("dialog")
        layout = QFormLayout()

        name_edit = QLineEdit()
        contact_edit = QLineEdit()
        address_edit = QLineEdit()
        layout.addRow("Имя:", name_edit)
        layout.addRow("Контакт:", contact_edit)
        layout.addRow("Адрес:", address_edit)

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

        ok_btn.clicked.connect(lambda: self.add_customer(
            name_edit.text(),
            contact_edit.text(),
            address_edit.text(),
            dialog))
        dialog.exec()

    def add_customer(self, name, contact, address, dialog):
        try:
            if not name:
                raise ValueError("Имя не может быть пустым.")
            db = Database()
            db.add_customer(name, contact, address)
            QMessageBox.information(self, "Успех", "Клиент добавлен!")
            dialog.accept()
            self.load_customers()
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def show_edit_dialog(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите клиента для редактирования.")
            return

        customer_id = int(self.table.item(selected, 0).text())
        db = Database()
        customer = db.get_customer(customer_id)

        dialog = QDialog(self)
        dialog.setWindowTitle("Редактировать клиента")
        dialog.setObjectName("dialog")
        layout = QFormLayout()

        name_edit = QLineEdit(customer[1])
        contact_edit = QLineEdit(customer[2])
        address_edit = QLineEdit(customer[3])
        layout.addRow("Имя:", name_edit)
        layout.addRow("Контакт:", contact_edit)
        layout.addRow("Адрес:", address_edit)

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

        ok_btn.clicked.connect(lambda: self.edit_customer(customer_id, name_edit.text(), contact_edit.text(), address_edit.text(), dialog))
        dialog.exec()

    def edit_customer(self, customer_id, name, contact, address, dialog):
        try:
            if not name:
                raise ValueError("Имя не может быть пустым.")
            db = Database()
            db.update_customer(customer_id, name, contact, address)
            QMessageBox.information(self, "Успех", "Клиент обновлён!")
            dialog.accept()
            self.load_customers()
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def delete_customer(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите клиента для удаления.")
            return

        customer_id = int(self.table.item(selected, 0).text())
        reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить этого клиента?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            db = Database()
            db.delete_customer(customer_id)
            QMessageBox.information(self, "Успех", "Клиент удалён!")
            self.load_customers()

    def update_language(self, language):
        translations = self.get_translations()
        self.current_language = language
        self.search_input.setPlaceholderText(translations[language]["Поиск по имени..."])
        self.table.setHorizontalHeaderLabels([
            translations[language]["ID"],
            translations[language]["Имя"],
            translations[language]["Телефон"],
            translations[language]["Email"]
        ])
        self.add_btn.setText(translations[language]["Добавить клиента"])
        self.edit_btn.setText(translations[language]["Редактировать"])
        self.delete_btn.setText(translations[language]["Удалить"])

    def get_translations(self):
        return {
            "Русский": {
                "Поиск по имени...": "Поиск по имени...",
                "ID": "ID", "Имя": "Имя", "Телефон": "Телефон", "Email": "Email",
                "Добавить клиента": "Добавить клиента", "Редактировать": "Редактировать", "Удалить": "Удалить",
                "Успех": "Успех", "Клиент добавлен!": "Клиент добавлен!", "Клиент обновлён!": "Клиент обновлён!",
                "Клиент удалён!": "Клиент удалён!", "Ошибка": "Ошибка",
                "Выберите клиента для редактирования.": "Выберите клиента для редактирования.",
                "Выберите клиента для удаления.": "Выберите клиента для удаления.",
                "Подтверждение": "Подтверждение",
                "Вы уверены, что хотите удалить этого клиента?": "Вы уверены, что хотите удалить этого клиента?"
            },
            "English": {
                "Поиск по имени...": "Search by name...",
                "ID": "ID", "Имя": "Name", "Телефон": "Phone", "Email": "Email",
                "Добавить клиента": "Add Customer", "Редактировать": "Edit", "Удалить": "Delete",
                "Успех": "Success", "Клиент добавлен!": "Customer added!", "Клиент обновлён!": "Customer updated!",
                "Клиент удалён!": "Customer deleted!", "Ошибка": "Error",
                "Выберите клиента для редактирования.": "Select a customer to edit.",
                "Выберите клиента для удаления.": "Select a customer to delete.",
                "Подтверждение": "Confirmation",
                "Вы уверены, что хотите удалить этого клиента?": "Are you sure you want to delete this customer?"
            }
        }