import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QFormLayout, QDialog, QLineEdit, \
    QHBoxLayout, QTableWidgetItem, QMessageBox, QComboBox, QLabel
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from core.database import Database


class SalesTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Поиск
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по дате...")
        self.search_input.setObjectName("search-input")
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "ID-Товара", "ID-Клиента", "Количество", "Дата"])
        self.table.setObjectName("data-table")
        layout.addWidget(self.table)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить продажу")
        self.add_btn.setObjectName("action-btn")
        buttons_layout.addWidget(self.add_btn)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Инициализируем текущий язык
        self.current_language = "Русский"

        self.load_sales()
        self.add_btn.clicked.connect(self.show_add_dialog)
        self.search_input.textChanged.connect(self.filter_sales)

    def load_sales(self):
        db = Database()
        sales = db.get_all_sales()
        self.table.setRowCount(len(sales))
        for row, sale in enumerate(sales):
            self.table.setItem(row, 0, QTableWidgetItem(str(sale[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(sale[1])))
            self.table.setItem(row, 2, QTableWidgetItem(str(sale[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(sale[3])))
            self.table.setItem(row, 4, QTableWidgetItem(sale[4]))

    def filter_sales(self):
        search_text = self.search_input.text().lower()
        db = Database()
        sales = db.get_all_sales()
        filtered_sales = [s for s in sales if search_text in s[4].lower()]
        self.table.setRowCount(len(filtered_sales))
        for row, sale in enumerate(filtered_sales):
            self.table.setItem(row, 0, QTableWidgetItem(str(sale[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(sale[1])))
            self.table.setItem(row, 2, QTableWidgetItem(str(sale[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(sale[3])))
            self.table.setItem(row, 4, QTableWidgetItem(sale[4]))

    def show_add_dialog(self):
        dialog = QDialog(self)
        translations = self.get_translations()
        dialog.setWindowTitle(translations[self.current_language]["Добавить продажу"])
        dialog.setObjectName("dialog")
        layout = QFormLayout()

        # Выпадающий список для товаров
        product_label = QLabel(translations[self.current_language]["Товар:"])
        product_combo = QComboBox()
        db = Database()
        products = db.get_all_products()
        for product in products:
            product_combo.addItem(f"ID: {product[0]} - {product[1]}", product[0])
        layout.addRow(product_label, product_combo)

        # Выпадающий список для клиентов
        customer_label = QLabel(translations[self.current_language]["Клиент:"])
        customer_combo = QComboBox()
        customers = db.get_all_customers()
        for customer in customers:
            customer_combo.addItem(f"ID: {customer[0]} - {customer[1]}", customer[0])
        layout.addRow(customer_label, customer_combo)

        # Поле для количества
        quantity_label = QLabel(translations[self.current_language]["Количество:"])
        quantity_edit = QLineEdit()
        layout.addRow(quantity_label, quantity_edit)

        ok_btn = QPushButton(translations[self.current_language]["Добавить"])
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

        ok_btn.clicked.connect(lambda: self.add_sale(
            product_combo.currentData(),
            customer_combo.currentData(),
            quantity_edit.text(),
            dialog))
        dialog.exec()

    def add_sale(self, product_id, customer_id, quantity, dialog):
        translations = self.get_translations()
        try:
            if not product_id or not customer_id or not quantity:
                raise ValueError(translations[self.current_language]["Все поля должны быть заполнены."])
            product_id = int(product_id)
            customer_id = int(customer_id)
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError(translations[self.current_language]["Количество должно быть больше 0."])
            db = Database()
            product = db.get_product(product_id)
            if not product:
                raise ValueError(translations[self.current_language]["Товар с ID не найден"].format(product_id))
            customer = db.get_customer(customer_id)
            if not customer:
                raise ValueError(translations[self.current_language]["Клиент с ID не найден"].format(customer_id))
            if product[2] < quantity:
                raise ValueError(translations[self.current_language]["Недостаточно товара на складе"].format(product[2]))
            total_price = product[3] * quantity
            db.add_sale(product_id, customer_id, quantity, total_price)
            QMessageBox.information(self, translations[self.current_language]["Успех"],
                                    translations[self.current_language]["Продажа добавлена!"])
            dialog.accept()
            self.load_sales()
        except ValueError as e:
            QMessageBox.warning(self, translations[self.current_language]["Ошибка"], str(e))
        except Exception as e:
            QMessageBox.critical(self, translations[self.current_language]["Ошибка"],
                                 translations[self.current_language]["Произошла ошибка"].format(str(e)))

    def update_language(self, language):
        translations = self.get_translations()
        self.current_language = language
        self.search_input.setPlaceholderText(translations[language]["Поиск по дате..."])
        self.table.setHorizontalHeaderLabels([
            translations[language]["ID"],
            translations[language]["ID-Товара"],
            translations[language]["ID-Клиента"],
            translations[language]["Количество"],
            translations[language]["Дата"]
        ])
        self.add_btn.setText(translations[language]["Добавить продажу"])

    def get_translations(self):
        return {
            "Русский": {
                "Поиск по дате...": "Поиск по дате...",
                "ID": "ID",
                "ID-Товара": "ID-Товара",
                "ID-Клиента": "ID-Клиента",
                "Количество": "Количество",
                "Дата": "Дата",
                "Добавить продажу": "Добавить продажу",
                "Добавить": "Добавить",
                "Товар:": "Товар:",
                "Клиент:": "Клиент:",
                "Количество:": "Количество:",
                "Успех": "Успех",
                "Продажа добавлена!": "Продажа добавлена!",
                "Ошибка": "Ошибка",
                "Произошла ошибка": "Произошла ошибка: {}",
                "Все поля должны быть заполнены.": "Все поля должны быть заполнены.",
                "Количество должно быть больше 0.": "Количество должно быть больше 0.",
                "Товар с ID не найден": "Товар с ID {} не найден.",
                "Клиент с ID не найден": "Клиент с ID {} не найден.",
                "Недостаточно товара на складе": "Недостаточно товара на складе. Доступно: {}"
            },
            "English": {
                "Поиск по дате...": "Search by date...",
                "ID": "ID",
                "ID-Товара": "Product ID",
                "ID-Клиента": "Customer ID",
                "Количество": "Quantity",
                "Дата": "Date",
                "Добавить продажу": "Add Sale",
                "Добавить": "Add",
                "Товар:": "Product:",
                "Клиент:": "Customer:",
                "Количество:": "Quantity:",
                "Успех": "Success",
                "Продажа добавлена!": "Sale added!",
                "Ошибка": "Error",
                "Произошла ошибка": "An error occurred: {}",
                "Все поля должны быть заполнены.": "All fields must be filled.",
                "Количество должно быть больше 0.": "Quantity must be greater than 0.",
                "Товар с ID не найден": "Product with ID {} not found.",
                "Клиент с ID не найден": "Customer with ID {} not found.",
                "Недостаточно товара на складе": "Not enough product in stock. Available: {}"
            }
        }