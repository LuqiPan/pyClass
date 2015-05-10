class MyClass:
    def f1(self):
        print self.i

    f = f1

o = MyClass()
o.i = 54321
meth = o.f
meth()
