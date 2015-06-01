import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('spreadsheet_credentials.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)

sh = gc.open("Simple Sheet")
worksheet = sh.sheet1

for row in worksheet.get_all_values():
    # print row
    # print row[0]
    # print row [1]
    hero = row[0]
    dessert = row[1]
    print "{} loves {}.".format(hero, dessert)
