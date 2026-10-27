#클래스 연습.py

#1. 클래스 정의
class Person:
    def __init__(self):
        self.name = "default name"
    def printInfo(self):
        #기존
        print("My name is {0}".format(self.name))
        #f-string 사용
        print(f"My name is {self.name}")

#2. 인스턴스 생성
p1 = Person()
p1.name = "전우치"
p2 = Person()

#3. 메서드 호출
p1.printInfo()
p2.printInfo()
