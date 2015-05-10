def f1(self):
    print self.i
    print 5

class C:
    f = f1

    def g1(self):
        print self.i
        print 10

    g = g1

o = C()
o.i = 12345
o.f()
o.g()
