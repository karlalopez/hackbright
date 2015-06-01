class Student(object):
    """For student records"""
    def __init__(self, name=None):
        # This special method is called a "constructor"
        self.name = name
    def print_name(self):
        print self.name

jenny = Student('Jenny')
jenny.print_name()     # prints 'Jenny'

### Exercise Time ###

bill = Student()
bill.print_name()
