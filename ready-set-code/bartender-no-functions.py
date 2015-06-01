import random

questions = {
    "strong": "Do ye like yer drinks strong?",
    "salty": "Do ye like it with a salty tang?",
    "bitter": "Are ye a lubber who likes it bitter?",
    "sweet": "Would ye like a bit of sweetness with yer poison?",
    "fruity": "Are ye one for a fruity finish?"
}

ingredients = {
    "strong": ["glug of rum", "slug of whisky", "splash of gin"],
    "salty": ["olive on a stick", "salt-dusted rim", "rasher of bacon"],
    "bitter": ["shake of bitters", "splash of tonic", "twist of lemon peel"],
    "sweet": ["sugar cube", "spoonful of honey", "spash of cola"],
    "fruity": ["slice of orange", "dash of cassis", "cherry on top"]
}

# Write a function to ask what style of drink a customer likes.
# The function should ask each of the questions in the questions dictionary, and gather the responses in a new dictionary.
# The new dictionary should contain the type of ingredient (for example "salty", or "sweet"), mapped to a Boolean (True or False) value.
# If the customer answers y or yes to the question then the value should be True, otherwise the value should be False.
# The function should return the new dictionary.

# def ask_questions():

answers = {}
for question in questions:
    answer = raw_input(questions[question]+" (y/n) ")
    if answer == "y" or answer == "yes":
        answers[question] = True
    else:
        answers[question] = False

print answers

# Write a function to construct a drink

# The function should take the preferences dictionary created in the first function as a parameter.
# Inside the function you should create an empty list to represent the drink.
# For each type of ingredient which the customer said they liked you should append a corresponding
# ingredient from the ingredients dictionary to the drink.
# Finally the function should return the drink.
# To choose an ingredient from one of the ingredient lists you can use the random.choice function again.

# def construcr_drink():
drink = []
for preference in answers:
    if answers[preference] == True:
        print preference+" is a yes"
        possible_ingredients = ingredients.get(preference)
        print possible_ingredients
        drink.append(random.choice(possible_ingredients))
    else:
        print preference+" is a no"
#return drink

print "Your drink recommendation:"
for i in drink:
    print "- a "+i
