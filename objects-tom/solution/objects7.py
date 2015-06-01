class Person(object):
    """For human beings"""
    def __init__(self, name=None):
        self.name = name

class Student(Person):
    """For student records"""
    def __init__(self, name=None, gpa=None):
        super(Student, self).__init__(name)
        self.gpa = gpa

jenny = Student('Jenny', 4.0)

print jenny.name
print jenny.gpa
