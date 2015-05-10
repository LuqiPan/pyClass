def g1(self):
    print 5

class MyClass:
    g = g1

o = MyClass()
o.g()
