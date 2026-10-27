# Person은 사람에게 공통으로 필요한 정보를 담는 기본 클래스예요.
class Person:
    # __init__은 새 사람을 만들 때 처음 한 번 실행되는 준비 단계예요.
    # self는 지금 만들고 있는 바로 그 사람을 가리켜요.
    def __init__(self, id, name):
        # id와 name을 이 사람의 주머니에 넣어 둬요.
        self.id = id
        self.name = name

    # 이 사람의 정보를 화면에 보여 주는 메서드예요.
    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}")


# Manager는 Person의 정보를 물려받고, 직책(title)도 하나 더 가져요.
class Manager(Person):
    # Manager를 만들 때 사람 정보와 직책을 함께 받아요.
    def __init__(self, id, name, title):
        # 부모인 Person에게 id와 name을 준비해 달라고 부탁해요.
        super().__init__(id, name)
        # Manager만 가진 직책을 따로 기억해요.
        self.title = title

    # 부모 정보에 직책까지 더해서 보여 줘요.
    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}, Title: {self.title}")


# Employee도 Person의 정보를 물려받고, 기술(skill)을 하나 더 가져요.
class Employee(Person):
    # Employee를 만들 때 사람 정보와 기술을 함께 받아요.
    def __init__(self, id, name, skill):
        # 부모인 Person에게 id와 name을 준비해 달라고 부탁해요.
        super().__init__(id, name)
        # Employee만 가진 기술을 따로 기억해요.
        self.skill = skill

    # 부모 정보에 기술까지 더해서 보여 줘요.
    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}, Skill: {self.skill}")
