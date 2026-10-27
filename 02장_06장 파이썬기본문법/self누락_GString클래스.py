#전역변수
strName = "Not Class Member"

class DemoString:
    def __init__(self):
        #인스턴스(가 사용하는) 멤버 변수
        self.strName = "" 
    def set(self, msg):
        self.strName = msg
    def print(self):
        #버그 발생
        print(self.strName)

d = DemoString()
d.set("First Message")
d.print()


'''이름 숨기기(변경)
__name, __get_value 처럼 밑줄 2개 쓰면
name mangling(이름 변경)되어 외부에서 접근 불가
_클래스명_속성명으로 변환됨
__init__, __str__, __reper__, __len__m __add__, __sub__는 특수 메서드로 이름 변경되지 않음

'''