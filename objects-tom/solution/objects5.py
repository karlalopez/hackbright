class Animal(object):
    """All creatures great and small"""
    def call(self):
        print self.noise

class Cow(Animal):
    """Good at grazing"""
    noise = 'moo'

class Pig(Animal):
    """Cleaner than you'd think"""
    noise = 'oink'

bessy = Cow()
petunia = Pig()

print 'The cow says',
bessy.call()
print 'The pig says',
petunia.call()
