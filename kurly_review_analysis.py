"""마켓컬리 상품 후기 300개를 수집하고 키워드 기반 감성을 시각화합니다."""

import re
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


PRODUCT_URL = "https://www.kurly.com/goods/5026468?collectionCode=hotkeyword15"
REVIEW_LIMIT = 300
PAGE_DELAY_SECONDS = 0.5

POSITIVE_KEYWORDS = (
    "맛있", "만족", "좋아요", "좋았", "좋은", "좋다", "좋습니다", "좋네요",
    "좋고", "좋아", "추천", "재구매", "부드럽", "깔끔", "진하", "깊은 맛",
    "간편", "편리", "든든", "푸짐", "최고", "훌륭", "신선", "맛나",
    "감칠맛", "담백", "넉넉", "잘 먹",
)
NEGATIVE_KEYWORDS = (
    "맛없", "맛이 없", "아쉽", "별로", "불만", "실망", "불편", "부족",
    "비싸", "질기", "너무 짜", "짜요", "짜서", "짠맛", "싱겁", "느끼",
    "냄새", "잡내", "퍽퍽", "딱딱", "양이 적", "고기가 적", "녹아",
    "터졌", "상했", "재구매 안", "다시는", "추천하지", "못 먹", "후회",
    "최악", "배송 지연", "배송이 늦",
)
NEGATION_AFTER_KEYWORD = re.compile(
    r"^\s*(?:[가이은는도]\s*)?(?:없|안|않|지\s*않|하지\s*않)"
)
SENTIMENT_ORDER = ("긍정", "부정", "중립")
OUTPUT_DIR = Path(__file__).resolve().parent


def _has_unnegated_keyword(text: str, keyword: str) -> bool:
    """키워드 바로 뒤의 대표적인 부정 표현은 감성 점수에서 제외합니다."""
    start = 0
    while (index := text.find(keyword, start)) != -1:
        suffix = text[index + len(keyword) : index + len(keyword) + 10]
        if not NEGATION_AFTER_KEYWORD.match(suffix):
            return True
        start = index + len(keyword)
    return False


def classify_sentiment(text: str) -> tuple[int, int, str]:
    """긍정·부정 키워드 수를 비교해 후기의 감성을 분류합니다."""
    positive_score = sum(
        _has_unnegated_keyword(text, keyword) for keyword in POSITIVE_KEYWORDS
    )
    negative_score = sum(
        _has_unnegated_keyword(text, keyword) for keyword in NEGATIVE_KEYWORDS
    )

    if positive_score > negative_score:
        sentiment = "긍정"
    elif negative_score > positive_score:
        sentiment = "부정"
    else:
        sentiment = "중립"
    return positive_score, negative_score, sentiment


def _review_section(driver: webdriver.Chrome):
    return driver.find_element(
        By.XPATH, '//section[.//h2[normalize-space()="상품 후기"]]'
    )


def _read_current_page(driver: webdriver.Chrome) -> list[dict[str, str]]:
    try:
        reviews = []
        for article in _review_section(driver).find_elements(
            By.CSS_SELECTOR, "article"
        ):
            titles = article.find_elements(By.CSS_SELECTOR, "h3")
            bodies = article.find_elements(By.CSS_SELECTOR, "p")
            if not titles or not bodies:
                continue

            title = titles[0].text.strip()
            text = bodies[0].text.strip()
            if text:
                reviews.append({"review_title": title, "review_text": text})
        return reviews
    except StaleElementReferenceException:
        return []


def _page_changed(
    driver: webdriver.Chrome, previous_signature: tuple[str, ...]
) -> bool:
    reviews = _read_current_page(driver)
    signature = tuple(review["review_text"] for review in reviews)
    return bool(signature) and signature != previous_signature


def collect_reviews(limit: int = REVIEW_LIMIT) -> list[dict[str, str]]:
    """상품 후기 탭을 페이지 이동하며 공개된 후기 본문을 수집합니다."""
    if limit < 1:
        raise ValueError("수집 개수는 1 이상이어야 합니다.")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1200")
    options.add_argument("--lang=ko-KR")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(PRODUCT_URL)
        wait = WebDriverWait(driver, 20)
        wait.until(lambda current_driver: bool(_read_current_page(current_driver)))

        collected: list[dict[str, str]] = []
        seen_page_signatures: set[tuple[str, ...]] = set()

        while len(collected) < limit:
            page_reviews = _read_current_page(driver)
            if not page_reviews:
                break

            signature = tuple(review["review_text"] for review in page_reviews)
            if signature in seen_page_signatures:
                raise RuntimeError("후기 페이지가 반복되어 수집을 중단했습니다.")
            seen_page_signatures.add(signature)

            collected.extend(page_reviews[: limit - len(collected)])
            if len(collected) >= limit:
                break

            section = _review_section(driver)
            next_buttons = section.find_elements(
                By.XPATH, './/button[normalize-space()="다음"]'
            )
            if not next_buttons or next_buttons[0].get_attribute("disabled"):
                break

            next_buttons[0].click()
            wait.until(lambda current_driver: _page_changed(current_driver, signature))
            time.sleep(PAGE_DELAY_SECONDS)

        if len(collected) != limit:
            raise RuntimeError(
                f"요청한 {limit}개 중 {len(collected)}개만 수집했습니다. "
                "상품 후기 페이지 상태를 확인해 주세요."
            )
        return collected
    finally:
        driver.quit()


def analyze_reviews(reviews: list[dict[str, str]]) -> pd.DataFrame:
    """후기를 분류하고 분석 결과를 담은 DataFrame을 반환합니다."""
    if not reviews:
        raise ValueError("분석할 후기가 없습니다.")

    data = pd.DataFrame(reviews)
    scores = data["review_text"].map(classify_sentiment)
    data[["positive_score", "negative_score", "sentiment"]] = pd.DataFrame(
        scores.tolist(), index=data.index
    )
    return data


def plot_sentiment(data: pd.DataFrame, output_path: Path) -> None:
    """긍정·부정·중립 후기 수를 막대그래프로 저장하고 표시합니다."""
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    counts = data["sentiment"].value_counts().reindex(SENTIMENT_ORDER, fill_value=0)
    colors = ["#4c956c", "#e76f51", "#9aa0a6"]
    fig, axis = plt.subplots(figsize=(8, 5))
    bars = axis.bar(counts.index, counts.values, color=colors)
    axis.bar_label(bars, padding=3)
    axis.set_title("마켓컬리 [사미헌] 갈비탕 후기 감성 분석")
    axis.set_xlabel("감성 분류")
    axis.set_ylabel("후기 수")
    axis.set_ylim(0, max(1, float(counts.max()) * 1.15))
    axis.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.show()


def main() -> None:
    reviews = collect_reviews(REVIEW_LIMIT)
    data = analyze_reviews(reviews)

    csv_path = OUTPUT_DIR / "kurly_5026468_reviews.csv"
    chart_path = OUTPUT_DIR / "kurly_5026468_sentiment.png"
    data.to_csv(csv_path, index=False, encoding="utf-8-sig")
    plot_sentiment(data, chart_path)

    print(f"수집 후기 수: {len(data)}")
    print(data["sentiment"].value_counts().reindex(SENTIMENT_ORDER, fill_value=0))
    print(f"\nCSV 저장: {csv_path}")
    print(f"그래프 저장: {chart_path}")
    print("분류는 한국어 키워드 기반의 간이 분석이며 문맥을 완벽히 판별하지 않습니다.")


if __name__ == "__main__":
    main()
