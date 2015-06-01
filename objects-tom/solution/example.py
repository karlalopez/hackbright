from pprint import *
def print_list(list=['cat', 'dog']):
    list.append('fish')
    pprint(list)

print_list()
print_list([1, 2, 3])
print_list()
print_list()
