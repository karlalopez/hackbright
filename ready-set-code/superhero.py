import string
import random

heroes = []

random_heroes = []

name = raw_input("What's your name? ")

letter = name[0].upper()
#print letter

uppers = string.uppercase
#print uppers

position = uppers.find(letter)
#print position


with open('names.txt') as f:
    for line in f:
        heroes.append(line.strip())


print "Your super heroe name is: "+heroes[position]

for i in heroes:
    random_heroes.append(i.split())


first_name = random.choice(random_heroes)
last_name = random.choice(random_heroes)

while True:
    if first_name != last_name:
        print "Your random super heroe name is: {} {}".format(first_name[0],last_name[1])
        break
