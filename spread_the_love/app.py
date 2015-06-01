from flask import Flask, render_template, request
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

app = Flask(__name__)



def get_spreadsheet_data():
    json_key = json.load(open('spreadsheet_credentials.json'))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    gc = gspread.authorize(credentials)

    sh = gc.open("Simple Sheet")
    worksheet = sh.sheet1
    data = worksheet.get_all_values()
    return data


@app.route("/")
def index():
    data = get_spreadsheet_data()
    heroes_list = []
    print data
    for row in data:
        hero = row[0]
        heroes_list.append(hero)
    print heroes_list
    return render_template("index.html", heroes_list=heroes_list)


@app.route("/submit", methods=['POST'])
def submit():
    data = get_spreadsheet_data()
    print request.form
    term = request.form.getlist('hero')
    find_hero = term[0]
    print find_hero
    message = ""
    for row in data:
        if find_hero == row[0]:
            hero = row[0]
            dessert = row[1]
            message = "{} loves {}.".format(hero, dessert)
    if message == "":
        message = "Sorry, hero not found."

    return render_template("submit.html", message=message )

if __name__=='__main__':
    app.run(debug=True)
