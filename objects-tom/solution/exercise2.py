class Test(object):
    def __init__(self, score):
        self.score = score

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if value < 0 or value > 100:
            raise Exception('Score out of range')
        self.__score = value

class Student(object):
    def __init__(self, name, tests=None):
        if tests is None:
            tests = []
        self.tests = tests
        self.name = name

    def test_average(self):
        return reduce(lambda x, y: x + y.score, self.tests, 0) / len(self.tests)

class Cohort(object):
    def __init__(self, students=None):
        if students is None:
            students = []
        self.students = students

    def print_grades(self):
        for student in self.students:
            print "{} {}".format(student.name, student.test_average())

my_cohort = Cohort([Student('Jerry', [Test(100), Test(50)]), Student('Carol', [Test(75), Test(67)])])
my_cohort.print_grades()
