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
print(func2(1))


