import sqlite3, random
from flask import Flask, render_template, request

app = Flask(__name__)

conn = sqlite3.connect('bar.db',check_same_thread=False)
db = conn.cursor()

def bar_closed():
    command = "SELECT * FROM ingredients WHERE stock>0;"
    db.execute(command)
    results = db.fetchall()
    if results != []:
        return False
    else:
        return True
    #conn.close()

def get_questions():
    preferences = {}
    db.execute("SELECT id, question FROM taste;")
    questions = db.fetchall()
    #conn.close()
    return questions

def make_drink(preferences):
    # [u'1', u'2', u'3', u'4', u'5']
    drink = []
    for liked in preferences:
        results = ""
        command = "SELECT name FROM ingredients WHERE taste={} and stock>0;".format(liked[0])
        db.execute(command)
        results = db.fetchall()
        print len(results)
        if len(results) < 1:
            continue
        else:
            if len(results) >=1:
                ingredient_chosen = (random.choice(results[0]))
                drink.append(ingredient_chosen)
            command = "SELECT stock FROM ingredients WHERE name='{}';".format(ingredient_chosen)
            db.execute(command)
            results = db.fetchall()
            print results
            stock=results[0]
            command = "UPDATE ingredients SET stock={} WHERE name='{}';".format((stock[0] - 1), ingredient_chosen)
            db.execute(command)
            conn.commit()
    #conn.close()
    return drink


@app.route('/')
def index():
    question_list = []
    taste_list = []
    if not bar_closed():
        bar = bar_closed()
        questions = get_questions()
        print bar
        stock = ""
        db.execute("SELECT * FROM ingredients;")
        stock = db.fetchall()
        return render_template("index.html", questions=questions, bar=bar, stock=stock)
    else:
        questions = ""
        bar = bar_closed()
        return render_template("index.html", questions=questions, bar=bar)
    #conn.close()




@app.route('/submit',methods=['POST'])
def submit():
    preferences = request.form.getlist('taste')
    drink = make_drink(preferences)
    return render_template("submit.html", preferences=preferences, drink=drink)


if __name__=='__main__':
    app.run(debug=True)
    #conn.close()
