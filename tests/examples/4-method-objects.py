class MyClass:
    def f(self):
        print self.i

o = MyClass()
o.i = 12345
meth = o.f
meth()
