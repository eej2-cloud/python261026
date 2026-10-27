
#부모 클래스 정의
class Person:
    def __init__(self, name, phoneNumber):
        self.name = name
        self.phoneNumber = phoneNumber

    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1})".format(self.name, self.phoneNumber))

#자식 클래스 정의
class Student(Person):
    #재정의(override)
    def __init__(self, name, phoneNumber, subject, studentID):
        #부모의 초기화 메서드 호출
        super().__init__(name, phoneNumber)
        self.subject = subject
        self.studentID = studentID
    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1}, 학과: {2}, 학번: {3})".format(self.name, self.phoneNumber, self.subject, self.studentID))

p = Person("전우치", "010-222-1234")
s = Student("이순신", "010-111-1234", "컴공", "991122")

#메서드 호출
p.printInfo()
s.printInfo()   

print(p.__dict__)
print(s.__dict__)


