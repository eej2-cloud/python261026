#db1.py

import sqlite3

#연결객체 생성(임시로 메모리에 작업)
conn = sqlite3.connect(":memory:")
#커서객체 생성
cur = conn.cursor()
#테이블 구조(스키마) 생성
cur.execute("create table PhoneBook(name text, phone text);")

#1건 입력
cur.execute(
    "insert into PhoneBook(name, phone) values(?, ?);", ("Alice", "010-1234-5678"))
#입력 파라미터 처리
name = "전우치"
phone = "010-9876-5432"
cur.execute("insert into PhoneBook(name, phone) values(?, ?);", (name, phone))
#여러 건 입력
datalist = (("홍길동", "010-1111-2222"), ("임꺽정", "010-3333-4444"))
cur.executemany("insert into PhoneBook(name, phone) values(?, ?);", datalist)

#검색
cur.execute("select * from PhoneBook;")
#주석처리: ctrl + /
# for row in cur:
#     print(row)
print("---fetchone()---")
print(cur.fetchone())
print("---fetchmany(2)---")
print(cur.fetchmany(2))
print("---fetchall()---")
cur.execute("select * from PhoneBook;")
print(cur.fetchall())

conn.close()








