#문자열처리연습.py

strA = """이 문자열은
다중 라인으로
저장되어 있습니다.
"""

strB = "python is very powerful" 

#디버깅 할 때 중단점
print(strA)
print(strB)
print(len(strB))


print(strB[0])
print(strB[0:6])
print(strB[:6])
print(strB[-1])
print(strB[-3:])

#특수문자 표기:\
print("c:\work\test.txt")
print("c:\\work\\test.txt")

#raw string notation: 소문자 r을 붙여서 사용
print(r"c:\work\test.txt")
print("c:/work/test.txt")


#리스트 연습
colors = ["red", "blue", "green"]
print(len(colors))
print(colors[0])
#입력(append)
colors.append("purple")
print(colors)
colors.insert(1, "black")
print(colors)
#삭제(remove)
colors.remove("blue")
print(colors)
for item in colors:
    print(item)

#정렬
colors.extend(["white", "pink", "orange"])
colors.sort()
print(colors)
colors.reverse()
print(colors)


#방 번호와 개수
print(colors.index("white"))
print(colors.count("pink"))

#세트형식
a = {1, 2, 3, 3}
b = {3, 4, 4, 5}
print(a)
print(len(a))
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))

#튜플형식
tp = (100, 200, 300)
print(type(tp))
print(len(tp))
print(tp[0])
print(tp.index(300))
print(tp.count(300))

#함수 정의
def times(a, b):
    return a+b, a*b
#함수 호출
result = times(3, 4)
print(result)
print("id:%s, name:%s" % (" kim", " 김유신"))

''' 감초함수
1. list(): 리스트로 타입캐스팅
2. int(): 정수로 바꿔줘
3. str(): 문자열로 바꿔줘
4. range(): 
'''
a = set((1, 2, 3, 3))
b = list(a)
c = tuple(b)
print("a", "b", "c")
print(int("10")+1)
print(str(3.14))
print(list("abc"))

args = (5, 6)
print(times(*args))
