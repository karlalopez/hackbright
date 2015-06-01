class Car(object):
    """Represents an automobile"""
    def __init__(self, year, make, model):
        self.make = make
        self.model = model
        self.year = year
    def print_details(self):
        print "{} {} {}".format(self.year, self.make, self.model)

my_car = Car(1985, 'Ford', 'Taurus')
my_car.print_details()
