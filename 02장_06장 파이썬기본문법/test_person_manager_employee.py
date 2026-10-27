# unittest는 파이썬에 들어 있는 테스트 도구예요.
import unittest
# 화면에 찍힌 글자를 잠시 모아 두는 도구예요.
from contextlib import redirect_stdout
# 화면 대신 글자를 담아 둘 작은 상자예요.
from io import StringIO

# 우리가 만든 세 가지 클래스를 가져와요.
from person_manager_employee import Employee, Manager, Person


# 이 상자 안의 확인 항목들은 하나씩 자동으로 실행돼요.
class PersonManagerEmployeeTests(unittest.TestCase):
    # 첫 번째 확인: Person이 받은 id를 잘 기억하는지 살펴봐요.
    def test_person_keeps_id(self):
        person = Person(1, "민지")
        self.assertEqual(person.id, 1)

    # 두 번째 확인: Person이 받은 이름을 잘 기억하는지 살펴봐요.
    def test_person_keeps_name(self):
        person = Person(1, "민지")
        self.assertEqual(person.name, "민지")

    # 세 번째 확인: Person이 id와 이름을 보기 좋게 출력하는지 살펴봐요.
    def test_person_prints_id_and_name(self):
        person = Person(1, "민지")
        output = StringIO()
        with redirect_stdout(output):
            person.printInfo()
        self.assertEqual(output.getvalue(), "ID: 1, Name: 민지\n")

    # 네 번째 확인: Manager가 Person의 자식 클래스인지 살펴봐요.
    def test_manager_inherits_from_person(self):
        self.assertTrue(issubclass(Manager, Person))

    # 다섯 번째 확인: Manager가 직책을 잘 기억하는지 살펴봐요.
    def test_manager_keeps_title(self):
        manager = Manager(2, "준호", "팀장")
        self.assertEqual(manager.title, "팀장")

    # 여섯 번째 확인: Manager가 사람 정보와 직책을 모두 출력하는지 살펴봐요.
    def test_manager_prints_all_information(self):
        manager = Manager(2, "준호", "팀장")
        output = StringIO()
        with redirect_stdout(output):
            manager.printInfo()
        self.assertEqual(output.getvalue(), "ID: 2, Name: 준호, Title: 팀장\n")

    # 일곱 번째 확인: Employee가 Person의 자식 클래스인지 살펴봐요.
    def test_employee_inherits_from_person(self):
        self.assertTrue(issubclass(Employee, Person))

    # 여덟 번째 확인: Employee가 기술을 잘 기억하는지 살펴봐요.
    def test_employee_keeps_skill(self):
        employee = Employee(3, "서연", "그림 그리기")
        self.assertEqual(employee.skill, "그림 그리기")

    # 아홉 번째 확인: Employee가 사람 정보와 기술을 모두 출력하는지 살펴봐요.
    def test_employee_prints_all_information(self):
        employee = Employee(3, "서연", "그림 그리기")
        output = StringIO()
        with redirect_stdout(output):
            employee.printInfo()
        self.assertEqual(
            output.getvalue(),
            "ID: 3, Name: 서연, Skill: 그림 그리기\n",
        )

    # 열 번째 확인: 서로 다른 사람은 각자 다른 정보를 가지는지 살펴봐요.
    def test_people_keep_their_own_information(self):
        manager = Manager(4, "하늘", "부장")
        employee = Employee(5, "바다", "코딩")
        self.assertEqual(manager.id, 4)
        self.assertEqual(employee.id, 5)
        self.assertNotEqual(manager.name, employee.name)


# 이 파일을 직접 실행했을 때에만 테스트를 시작해요.
if __name__ == "__main__":
    unittest.main()
