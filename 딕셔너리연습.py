#딕셔너리연습.py

d = {"apple":"red", "banana":"yellow"}
print(len(d))
#search
print(d["apple"])
#append
d["kiwi"] = "green"
print(d)
#fix
d["apple"] = "green"
print(d)
#delete
del d["apple"]
print(d)
for item in d.items():
    print(item)

#Boolean
isRight = True
print(type(isRight))
print(1 < 2)
print(1 > 2)
x = 5
y = 6
print(x == y)
print( x != y)
print(not isRight)
print( True and True and True)
print( True and True and False)
print( True or False or False)

# 연산자
print(5 / 2)
print(5 // 2)
print(5 % 2)
print(5 ** 2)




