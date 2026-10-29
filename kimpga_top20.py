"""김프가 첫 화면의 코인 표에서 처음 20개 행을 가져와 표시합니다.

준비: pip install PyQt6 selenium
Chrome 브라우저가 설치되어 있어야 합니다.
"""

import csv
import re
import sys
from pathlib import Path

from PyQt6.QtCore import QThread, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QHeaderView,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


URL = "https://kimpga.com/"
LIMIT = 20
OUTPUT_FILE = Path(__file__).with_name("kimpga_top20.csv")
FIELD_NAMES = [
    "순위",
    "이름/티커",
    "현재가(기준/비교)",
    "김프(김프율/가격차이)",
    "전일대비(등락률/변동액)",
    "고가대비(전일)(등락률/고가)",
    "저가대비(전일)(등락률/저가)",
    "등급",
    "RD 스코어",
    "거래액(기준/비교)",
]


def wait_for_coin_rows(driver: WebDriver) -> list[WebElement] | bool:
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
    if len(rows) >= LIMIT + 1:
        return rows
    return False


def fetch_coin_rows() -> list[list[str]]:
    driver = webdriver.Chrome()
    try:
        driver.get(URL)
        rows = WebDriverWait(driver, 30).until(wait_for_coin_rows)

        records = []
        for rank, row in enumerate(rows[1 : LIMIT + 1], start=1):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) != len(FIELD_NAMES) - 1:
                raise RuntimeError(
                    "코인 표의 열 구성이 예상과 다릅니다. "
                    "사이트의 표 구조가 변경되었는지 확인해 주세요."
                )

            values = []
            for cell in cells:
                text = " / ".join(
                    part.strip() for part in cell.text.splitlines() if part.strip()
                )
                values.append(re.sub(r"(?<=%)(?=[+-]?\d)", " / ", text))
            records.append([str(rank), *values])

        return records
    finally:
        driver.quit()


def save_as_csv(records: list[list[str]]) -> None:
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(FIELD_NAMES)
        writer.writerows(records)


class CrawlerThread(QThread):
    succeeded = pyqtSignal(list)
    failed = pyqtSignal(str)

    def run(self) -> None:
        try:
            self.succeeded.emit(fetch_coin_rows())
        except Exception as error:
            self.failed.emit(str(error))


class KimpgaWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("김프가 상위 20개 코인")
        self.resize(1400, 620)
        self.worker: CrawlerThread | None = None

        self.refresh_button = QPushButton("새로고침")
        self.refresh_button.clicked.connect(self.load_coins)

        self.coin_table = QTableWidget(0, len(FIELD_NAMES))
        self.coin_table.setHorizontalHeaderLabels(FIELD_NAMES)
        self.coin_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.coin_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.coin_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.coin_table.setAlternatingRowColors(True)
        self.coin_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.coin_table.horizontalHeader().setStretchLastSection(True)

        layout = QVBoxLayout()
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.coin_table)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.statusBar().showMessage("코인 정보를 불러오는 중입니다...")
        self.load_coins()

    def load_coins(self) -> None:
        if self.worker is not None and self.worker.isRunning():
            return

        self.refresh_button.setEnabled(False)
        self.statusBar().showMessage("코인 정보를 불러오는 중입니다...")
        self.worker = CrawlerThread(self)
        self.worker.succeeded.connect(self.show_coins)
        self.worker.failed.connect(self.show_error)
        self.worker.finished.connect(lambda: self.refresh_button.setEnabled(True))
        self.worker.start()

    def show_coins(self, records: list[list[str]]) -> None:
        self.coin_table.setRowCount(len(records))
        for row_index, record in enumerate(records):
            for column_index, value in enumerate(record):
                item = QTableWidgetItem(value)
                if column_index == 0:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )
                self.coin_table.setItem(row_index, column_index, item)

        try:
            save_as_csv(records)
        except OSError as error:
            QMessageBox.warning(
                self,
                "CSV 저장 오류",
                f"표는 표시했지만 CSV 파일을 저장하지 못했습니다.\n{error}",
            )
            self.statusBar().showMessage(f"{len(records)}개 코인 정보를 표시합니다.")
            return

        self.statusBar().showMessage(
            f"{len(records)}개 코인 정보를 표시했습니다. CSV 저장 위치: {OUTPUT_FILE}"
        )

    def show_error(self, message: str) -> None:
        self.statusBar().showMessage("코인 정보를 불러오지 못했습니다.")
        QMessageBox.critical(
            self,
            "크롤링 오류",
            f"코인 정보를 불러오지 못했습니다.\n{message}",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KimpgaWindow()
    window.show()
    sys.exit(app.exec())
