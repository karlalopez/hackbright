import string
import random

heroes = []

random_heroes = []

with open('mysuperheronames.txt') as f:
    for line in f:
        heroes.append(line.strip())
#print heroes


for i in heroes:
    random_heroes.append(i.split())
#print random_heroes

first_name = random.choice(random_heroes)
last_name = random.choice(random_heroes)


if first_name != last_name:
    print "Your random super heroe name is: {} {}".format(first_name[0],last_name[1])
