from getpass import getpass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


LOGIN_URL = (
    "https://nid.naver.com/nidlogin.login?"
    "mode=number&url=https%3A%2F%2Fwww.naver.com%2F&locale=ko_KR&svctype=1"
)

driver = webdriver.Chrome()

try:
    driver.get(LOGIN_URL)

    one_time_number = getpass("네이버 앱에서 확인한 일회용 로그인 번호를 입력하세요: ").strip()
    if not one_time_number or not one_time_number.isdigit():
        raise ValueError("일회용 로그인 번호는 숫자로 입력해야 합니다.")

    wait = WebDriverWait(driver, 20)
    number_field = wait.until(
        EC.visibility_of_element_located((By.ID, "OnetimeCode"))
    )
    number_field.send_keys(one_time_number)

    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, "otnlog.login"))
    )
    login_button.click()

    input("로그인 결과를 확인한 후 Enter를 누르면 브라우저를 종료합니다.")
finally:
    driver.quit()
