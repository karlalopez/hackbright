# Write a class for a school test called Test
#
# * have a property called score
# * throw an exception if score is less than 0 or greater than 100
#

class Test(object):
     def __init__(self, score):
        self.score = score     
        if score < 0 or score > 100: 
            raise Exception("Score not valid")

x = 50
if Test(x):
    print x

# Write a class for a student called Student
#
# * the student should have a name and a list of tests
# * write a method called test_average that returns the student's average grade
#

class Student(object):
    def __init__(self,name,tests):
        self.name = name
        self.tests = tests
    def test_average(self):
        sum = 0
        tests = self.tests
        n_tests = len(tests)
        for n in tests:
            sum = sum + n
        average = sum / n_tests
        return average


## malia = Student("Malia", [50,100])
## print malia.test_average()

# Write a class for a group of students called Cohort
#
# * write a method called print_grades that prints the list of student names and grades:
#
#   Jessie 100
#   Cora 78
#   Betty 59
#

class Cohort(object):
    def __init__(self,student_list):
        self.student_list = student_list
    def print_grades(self):
        for s,test_list in self.student_list:
            student = Student(s, [100,50])
            print "{} {}".format(student.name,student.test_average())


# Write a program that does:
#
# Create a new Cohort
# Create 2 students and add them to the cohort
# Create 2 tests for each student
# Print the list of students

