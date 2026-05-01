import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from core.database import Database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
import numpy as np

class AnalyticsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Общая выручка
        self.revenue_label = QLabel("Общая выручка: 0")
        layout.addWidget(self.revenue_label)

        # График продаж
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Таблица топ-5 товаров
        self.top_products_table = QTableWidget()
        self.top_products_table.setColumnCount(3)
        self.top_products_table.setHorizontalHeaderLabels(["ID товара", "Название", "Количество продаж"])
        self.top_products_table.setObjectName("data-table")
        layout.addWidget(self.top_products_table)

        self.setLayout(layout)

        # Загружаем данные
        self.load_analytics()

    def load_analytics(self):
        db = Database()
        sales = db.get_all_sales()

        # Общая выручка
        total_revenue = sum(sale[5] for sale in sales)  # total_price находится в 6-м столбце (индекс 5)
        self.revenue_label.setText(f"Общая выручка: {total_revenue:.2f}")

        # График продаж по дням
        if sales:
            dates = [datetime.strptime(sale[4], "%Y-%m-%d %H:%M:%S").date() for sale in sales]
            amounts = [sale[5] for sale in sales]

            # Группируем по дням
            unique_dates = sorted(set(dates))
            daily_totals = [sum(amount for date, amount in zip(dates, amounts) if date == d) for d in unique_dates]

            self.ax.clear()
            self.ax.plot(unique_dates, daily_totals, marker='o', color='#4A90E2')
            self.ax.set_title("Продажи по дням")
            self.ax.set_xlabel("Дата")
            self.ax.set_ylabel("Выручка")
            plt.xticks(rotation=45)
            self.ax.grid(True)
            self.figure.tight_layout()
            self.canvas.draw()

        # Топ-5 товаров
        product_sales = {}
        for sale in sales:
            product_id = sale[1]  # product_id
            quantity = sale[3]  # quantity
            if product_id in product_sales:
                product_sales[product_id] += quantity
            else:
                product_sales[product_id] = quantity

        # Получаем названия товаров
        products = db.get_all_products()
        product_names = {p[0]: p[1] for p in products}  # {id: name}

        # Сортируем по количеству продаж
        top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]

        # Заполняем таблицу
        self.top_products_table.setRowCount(len(top_products))
        for row, (product_id, quantity) in enumerate(top_products):
            self.top_products_table.setItem(row, 0, QTableWidgetItem(str(product_id)))
            self.top_products_table.setItem(row, 1, QTableWidgetItem(product_names.get(product_id, "Неизвестно")))
            self.top_products_table.setItem(row, 2, QTableWidgetItem(str(quantity)))

    def update_language(self, language):
        translations = self.get_translations()
        self.current_language = language
        self.revenue_label.setText(translations[language]["Общая выручка"])

    def get_translations(self):
        return {
            "Русский": {
                "Общая выручка": "Общая выручка",
                "Самый продаваемый товар": "Самый продаваемый товар"
            },
            "English": {
                "Общая выручка": "Total Revenue",
                "Самый продаваемый товар": "Top Selling Product"
            }
        }