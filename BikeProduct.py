import sys
import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from BikeManager import BikeManager


class BikeProduct(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("자전거 용품 관리")
        self.resize(640, 480)
        self.bike_manager = BikeManager()

        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setPlaceholderText("자동 생성")
        self.name_input = QLineEdit()
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("숫자만 입력")

        form = QFormLayout()
        form.addRow("ID:", self.id_input)
        form.addRow("용품명:", self.name_input)
        form.addRow("가격:", self.price_input)

        self.add_button = QPushButton("입력")
        self.update_button = QPushButton("수정")
        self.delete_button = QPushButton("삭제")
        self.search_button = QPushButton("검색")

        buttons = QHBoxLayout()
        for button in (
            self.add_button,
            self.update_button,
            self.delete_button,
            self.search_button,
        ):
            buttons.addWidget(button)

        self.product_table = QTableWidget(0, 3)
        self.product_table.setHorizontalHeaderLabels(["ID", "용품명", "가격"])
        self.product_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.product_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.product_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.product_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.product_table.itemDoubleClicked.connect(self._select_product)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addWidget(QLabel("자전거 용품 목록"))
        layout.addWidget(self.product_table)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.statusBar().showMessage("용품명을 입력해 검색할 수 있습니다.")

        self.add_button.clicked.connect(self.add_product)
        self.update_button.clicked.connect(self.update_product)
        self.delete_button.clicked.connect(self.delete_product)
        self.search_button.clicked.connect(self.search_products)

        self._refresh_products()

    def _product_values(self) -> tuple[str, int] | None:
        name = self.name_input.text().strip()
        price_text = self.price_input.text().strip()

        if not name:
            QMessageBox.warning(self, "입력 확인", "용품명을 입력해 주세요.")
            self.name_input.setFocus()
            return None

        try:
            price = int(price_text)
        except ValueError:
            QMessageBox.warning(self, "입력 확인", "가격은 숫자로 입력해 주세요.")
            self.price_input.setFocus()
            return None

        if price < 0:
            QMessageBox.warning(self, "입력 확인", "가격은 0 이상이어야 합니다.")
            self.price_input.setFocus()
            return None

        return name, price

    def _product_id(self) -> int | None:
        try:
            return int(self.id_input.text())
        except ValueError:
            QMessageBox.warning(self, "선택 확인", "목록에서 용품을 선택해 주세요.")
            return None

    def _refresh_products(self, name_filter: str = "") -> None:
        try:
            products = self.bike_manager.select_products(name_filter)
        except sqlite3.Error as error:
            QMessageBox.critical(self, "데이터베이스 오류", str(error))
            return

        self.product_table.setRowCount(len(products))
        for row, (product_id, name, price) in enumerate(products):
            id_item = QTableWidgetItem(str(product_id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            price_item = QTableWidgetItem(f"{price:,}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.product_table.setItem(row, 0, id_item)
            self.product_table.setItem(row, 1, QTableWidgetItem(name))
            self.product_table.setItem(row, 2, price_item)

        self.statusBar().showMessage(f"{len(products)}개 용품을 표시합니다.")

    def add_product(self) -> None:
        values = self._product_values()
        if values is None:
            return

        try:
            self.bike_manager.insert_product(*values)
        except sqlite3.Error as error:
            QMessageBox.critical(self, "데이터베이스 오류", str(error))
            return

        self._clear_form()
        self._refresh_products()

    def update_product(self) -> None:
        product_id = self._product_id()
        if product_id is None:
            return

        values = self._product_values()
        if values is None:
            return

        try:
            row_count = self.bike_manager.update_product(product_id, *values)
        except sqlite3.Error as error:
            QMessageBox.critical(self, "데이터베이스 오류", str(error))
            return

        if row_count == 0:
            QMessageBox.information(self, "검색 결과", "해당 ID의 용품이 없습니다.")
            return

        self._clear_form()
        self._refresh_products()

    def delete_product(self) -> None:
        product_id = self._product_id()
        if product_id is None:
            return

        answer = QMessageBox.question(
            self,
            "삭제 확인",
            "선택한 용품을 삭제하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            row_count = self.bike_manager.delete_product(product_id)
        except sqlite3.Error as error:
            QMessageBox.critical(self, "데이터베이스 오류", str(error))
            return

        if row_count == 0:
            QMessageBox.information(self, "검색 결과", "해당 ID의 용품이 없습니다.")

        self._clear_form()
        self._refresh_products()

    def search_products(self) -> None:
        self._refresh_products(self.name_input.text().strip())

    def _select_product(self, item: QTableWidgetItem) -> None:
        row = item.row()
        self.id_input.setText(self.product_table.item(row, 0).text())
        self.name_input.setText(self.product_table.item(row, 1).text())
        self.price_input.setText(
            self.product_table.item(row, 2).text().replace(",", "")
        )

    def _clear_form(self) -> None:
        self.id_input.clear()
        self.name_input.clear()
        self.price_input.clear()

    def closeEvent(self, event) -> None:
        self.bike_manager.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BikeProduct()
    window.show()
    sys.exit(app.exec())
