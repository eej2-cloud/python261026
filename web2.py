#web2.py
#웹크롤링을 위한 선언
from bs4 import BeautifulSoup
#웹서버에 요청
import urllib.request
#정규표현식
import re

#파일에 저장(wt = write text)
f = open("clien.txt", "wt", encoding="utf-8")
#헤더
hdr = {'User-Agent': 'Mozilla/5.0'}
#페이징 처리
for i in range(0, 10):
    url = "https://www.clien.net/service/board/sold?&od=T31&category=0&po=" + str(i)
    print(url)
    #요청객체 생성
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')

    #매물 정보 추출
    items = soup.find_all("span", attrs={'data-role': 'list-title-text'})
    for item in items:
        title = item.text.strip()
        if re.search("아이패드", title):
            print(title)
            f.write(title + "\n")

#파일 닫기
f.close

'''<span class="subject_fixed" data-role="list-title-text" title="레노버 샤오신 패드 2024 태블릿 글로벌 롬 8G 128G 퍼플">
							레노버 샤오신 패드 2024 태블릿 글로벌 롬 8G 128G 퍼플
						</span>'''