#함수연습.py


#1. 함수를 정의
def times(a, b):
    return a+b, a*b
#2. 함수 호출
result = times(3, 4)
print(result)
#3. 함수 정의
def setValue(newValue):
    #지역변수
    x = newValue
    print("지역변수:", x)
#호출
result = setValue(5)
print(result)

#함수 내부에서 이름 해석 LGB
x = 10
def func(a):
    return a + x
print(func(1))
def func2(a):
    #지역변수
    x = 5
    return a + x
#호출
print(func2(1))

#기본값 명시
def times(a = 10, b = 20):
    return a * b

#호출
print(times()) 
print(times(5))
print(times(5, 6))

#키워드인자
def connectURI(server, port):
    return "http://" + server + ":" + port
#호출
print(connectURI("localhost", "8080 "))
print(connectURI(port = "8080", server = "localhost"))

#가변인자
def union(*ar):
    result = []
    for item in ar:
        for x in item:
            if x not in result:
                result.append(x)
    return result


#호출
print(union("HAM", "EGG")) 
print(union("HAM", "EGG", "SPAM"))

#람다함수
g = lambda x, y: x * y
print(g(3, 4))
#즉시 실행 람다함수
print((lambda x: x * x)(3))

print(dir())
print(globals())

#필터링하는 코드
lst = [10, 25,30]
iterL = filter(None, lst)
for item in iterL:
    print(item)

#필터링하는 함수 정의
def getBiggerthan20(n):
    return n > 20
print("---필터링 함수 사용--- ")
iterL = filter(getBiggerthan20, lst)
for item in iterL:
    print(item) 

print("---람다 함수 사용--- ")
iterL = filter(lambda x: x > 20, lst)
for item in iterL:
    print(item)


print("---매핑하는 함수 사용--- ")
for item in map(lambda x: x * 2, lst):
    print(item)
