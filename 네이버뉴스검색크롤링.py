import csv
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


SEARCH_URL = "https://search.naver.com/search.naver"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def get_news_items(keyword):
    params = urlencode(
        {
            "where": "news",
            "ie": "utf8",
            "sm": "nws_hty",
            "query": keyword,
        }
    )
    request = Request(f"{SEARCH_URL}?{params}", headers=HEADERS)

    with urlopen(request, timeout=10) as response:
        html = response.read()

    soup = BeautifulSoup(html, "html.parser")
    title_links = [
        (link, link.get_text(" ", strip=True))
        for link in soup.select("a.news_tit")
    ]
    for headline in soup.select("span.sds-comps-text-type-headline1"):
        link = headline.find_parent("a")
        if link:
            title_links.append((link, headline.get_text(" ", strip=True)))

    news_items = []
    seen_urls = set()

    for title_link, title in title_links:
        link = title_link.get("href", "")
        if not title or not link or link in seen_urls:
            continue
        seen_urls.add(link)

        card = title_link.find_parent("div", class_="news_area")
        if not card:
            card = title_link.find_parent(
                "div", class_="sds-comps-vertical-layout"
            )
            while card and not card.select_one(
                ".sds-comps-profile-info-title-text"
            ):
                card = card.find_parent(
                    "div", class_="sds-comps-vertical-layout"
                )
        card = card or title_link.parent
        summary_tag = card.select_one(
            ".news_dsc, .sds-comps-text-type-body1"
        )
        press_tag = card.select_one(
            ".info_group .press, .sds-comps-profile-info-title-text"
        )
        date_tag = card.select_one(
            ".info_group .info, .sds-comps-profile-info-subtext"
        )

        news_items.append(
            {
                "title": title,
                "press": (
                    press_tag.get_text(" ", strip=True)
                    .replace("새 창 열림", "")
                    .strip()
                    if press_tag
                    else ""
                ),
                "date": (
                    date_tag.get_text(" ", strip=True)
                    if date_tag and "새 창 열림" not in date_tag.get_text()
                    else ""
                ),
                "summary": (
                    summary_tag.get_text(" ", strip=True) if summary_tag else ""
                ),
                "link": link,
            }
        )

    return news_items


def save_as_csv(news_items, filename):
    fieldnames = ["title", "press", "date", "summary", "link"]
    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(news_items)


if __name__ == "__main__":
    keyword = input("검색어를 입력하세요 (기본값: 반도체): ").strip() or "반도체"
    items = get_news_items(keyword)

    if not items:
        raise RuntimeError(
            "검색 결과를 찾지 못했습니다. 네이버 페이지 구조가 변경되었는지 "
            "확인해 주세요."
        )

    for index, item in enumerate(items, start=1):
        print(f"\n[{index}] {item['title']}")
        print(f"언론사: {item['press']} / 날짜: {item['date']}")
        print(f"요약: {item['summary']}")
        print(f"링크: {item['link']}")

    output_file = "naver_news_results.csv"
    save_as_csv(items, output_file)
    print(f"\n총 {len(items)}건을 {output_file} 파일에 저장했습니다.")
