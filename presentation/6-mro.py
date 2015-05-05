class X(object):
    pass

class Y(object):
    pass

class A(X,Y):
    def greet(self):
        print "I'm A"

class B(Y,X):
    def greet(self):
        print "I'm B"

class C(A,B):
    pass

#o = C()
#o.greet() #what happens here?
