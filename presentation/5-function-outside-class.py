def f1(self):
    print self.g
    print 'function defined outside of the class definition'

class C:
    f = f1

    def g1(self):
        print 'function defined inside of the class definition'

    g = g1

o = C()
o.f()
o.g()
