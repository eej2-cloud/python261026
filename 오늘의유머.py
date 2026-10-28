#web2.py
#웹크롤링을 위한 선언
from bs4 import BeautifulSoup
#웹서버에 요청
import urllib.request
#정규표현식
import re

#파일에 저장(wt = write text)
#오
f = open("todayhumor.txt", "wt", encoding="utf-8")
#헤더
hdr = {'User-Agent': 'Mozilla/5.0'}
#페이징 처리
for i in range(1, 11):
    url = "https://www.todayhumor.co.kr/board/list.php?kind=total&table=total&page=" + str(i)
    print(url)
    #요청객체 생성
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')

    #매물 정보 추출
    items = soup.find_all("td", attrs={'class': 'subject'})
    for item in items:
        title = item.find("a").text.strip()
        if re.search("한국", title):
            print(title)
            f.write(title + "\n")

#파일 닫기
f.close()

#<td class="subject">
#<td class="subject"><a href="/board/view.php?table=bestofbest&amp;no=483780&amp;s_no=483780&amp;page=10" target="_top">내 예산 안에서 최고의 휴가지를 추천해줘</a><span class="list_memo_count_span"> [19]</span>  <span style="margin-left:4px;"><img src="//www.todayhumor.co.kr/board/images/list_icon_photo.gif" style="vertical-align:middle; margin-bottom:1px;"> </span><img src="//www.todayhumor.co.kr/board/images/list_icon_shovel.gif?2" alt="펌글" style="margin-right:3px;top:2px;position:relative"> </td>
