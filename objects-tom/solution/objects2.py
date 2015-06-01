class MyClass(object):
    """A simple example class"""
    i = 12345
    def f(self):
        print 'hello world'

my_instance = MyClass()

print my_instance.i
my_instance.f()

object2 = MyClass()
object2.i = 3
print object2.i
print my_instance.i
