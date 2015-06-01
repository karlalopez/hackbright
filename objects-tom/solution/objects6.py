class Animal(object):
    """All creatures great and small"""
    def call(self):
        print self.noise

class Cow(Animal):
    """Good at grazing"""
    noise = 'moo'
    def call(self):
        print 'The cow says',
        super(Cow, self).call()

class Pig(Animal):
    """Cleaner than you'd think"""
    noise = 'oink'
    def call(self):
        print 'The pig says',
        super(Pig, self).call()

bessy = Cow()
petunia = Pig()

bessy.call()
#petunia.call()
