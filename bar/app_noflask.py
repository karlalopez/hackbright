import sqlite3, random
from flask import Flask, render_template

app = Flask(__name__)

conn = sqlite3.connect('bar.db')
db = conn.cursor()

def bar_closed():
    command = "SELECT * FROM ingredients WHERE stock>0;"
    db.execute(command)
    results = db.fetchall()
    if results != []:
        return False
    else:
        return True


def find_preferences():
    preferences = {}
    db.execute("SELECT id, question FROM taste;")
    questions = db.fetchall()
    print questions
    for taste, question in questions:
         print question
         preferences[taste] = raw_input().lower() in ["y", "yes"]
    return preferences

def make_drink(preferences):
    drink = []
    for ingredient_type, liked in preferences.iteritems():
        results = ""
        if not liked:
            continue
        print ingredient_type
        command = "SELECT name FROM ingredients WHERE taste={} and stock>0;".format(ingredient_type)
        db.execute(command)
        results = db.fetchall()
        ingredient_chosen = (random.choice(results[0]))
        drink.append(ingredient_chosen)
        print ingredient_chosen
        command = "SELECT stock FROM ingredients WHERE name='{}';".format(ingredient_chosen)
        db.execute(command)
        results = db.fetchall()
        print results
        stock=results[0]
        command = "UPDATE ingredients SET stock={} WHERE name='{}';".format((stock[0] - 1), ingredient_chosen)
        db.execute(command)
        conn.commit()
    print drink




if __name__ == "__main__":
    if not bar_closed():
        preferences = find_preferences()
        drink = make_drink(preferences)
        conn.close()

        # if drink == []
