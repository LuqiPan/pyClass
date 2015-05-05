class Dog:
    #tricks = []
    def __init__(self):
        self.tricks = []

    def add_trick(self, trick):
        self.tricks.append(trick)

d = Dog()
e = Dog()
d.add_trick('roll over')
e.add_trick('play dead')

print d.tricks
print e.tricks
print Dog.tricks
