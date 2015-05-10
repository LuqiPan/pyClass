class MyClass:
    i = 12345

o1 = MyClass()
o2 = MyClass()
print o1.i
print o2.i

o2.i = 54321
print o1.i
print o2.i
