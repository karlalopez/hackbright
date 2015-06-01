from flask import Flask, render_template, request
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=['POST'])
def submit():
    json_key = json.load(open('spreadsheet_credentials.json'))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    gc = gspread.authorize(credentials)

    sh = gc.open("Simple Sheet")
    worksheet = sh.sheet1

    print request.form
    term = request.form.getlist('hero')
    find_hero = term[0]
    print find_hero
    message = ""
    for row in worksheet.get_all_values():
        if find_hero == row[0]:
            hero = row[0]
            dessert = row[1]
            message = "{} loves {}.".format(hero, dessert)
    if message == "":
        message = "Sorry, hero not found."

    return render_template("submit.html", message=message )

if __name__=='__main__':
    app.run(debug=True)
