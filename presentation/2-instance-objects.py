class MyClass:
    i = 12345
    def f(self):
        return 'hello world'

x = MyClass()
#print x.counter
x.counter = 1
while x.counter < 42:
    x.counter = x.counter + 1
print x.counter
del x.counter
print x.counter
