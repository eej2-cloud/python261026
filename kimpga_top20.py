"""김프가 첫 화면의 코인 표에서 처음 20개 행을 CSV로 저장합니다.

준비: pip install selenium
Chrome 브라우저가 설치되어 있어야 합니다.
"""

import csv
import re
import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


URL = "https://kimpga.com/"
LIMIT = 20
OUTPUT_FILE = Path(__file__).with_name("kimpga_top20.csv")
CSV_FIELDS = [
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


def wait_for_coin_rows(driver: WebDriver):
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
    if len(rows) >= LIMIT + 1:
        return rows
    return False


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    driver = webdriver.Chrome()
    try:
        driver.get(URL)
        rows = WebDriverWait(driver, 30).until(wait_for_coin_rows)

        coin_rows = rows[1 : LIMIT + 1]
        records = []
        for rank, row in enumerate(coin_rows, start=1):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) != len(CSV_FIELDS) - 1:
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
            records.append(dict(zip(CSV_FIELDS, [rank, *values])))
    finally:
        driver.quit()

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(records)

    print(f"총 {len(records)}개 코인 정보를 저장했습니다: {OUTPUT_FILE}")
    for record in records:
        print(
            f"{record['순위']}. {record['이름/티커']} | "
            f"현재가: {record['현재가(기준/비교)']} | "
            f"김프: {record['김프(김프율/가격차이)']}"
        )


if __name__ == "__main__":
    main()
