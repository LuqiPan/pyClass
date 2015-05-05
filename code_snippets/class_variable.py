class Dog:
    kind = 'canine'

d = Dog
print(d.kind)
Dog.kind = 'chiwawa'
print(d.kind)
d.kind = 'canine'
print(Dog.kind)
