class Person(object):
    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if value < 0: raise Exception('Age out of bounds.')
        self.__age = value

p = Person()
p.age = 14
print p.age
p.age = -34
