class Car(object):
    def __init__(self,maker=None, model=None,year=None):
        self.maker = maker
        self.year = year
        self.model = model
    def details(self):
        print "{0} {1} {2}".format(self.year,self.maker,self.model)




my_car = Car("Honda", "Fit", "2012")

print my_car.maker
print my_car.model
print my_car.year

my_car.details()
