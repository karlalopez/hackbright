import sqlite3

conn = sqlite3.connect('bar.db')
db = conn.cursor()

# To run any SQL command, we use db.execute() on it.
db.execute("SELECT id, name, stock FROM ingredients;")

# After calling execute, we have to go ask the cursor to get us the rows which matched
results = db.fetchall()


# Now results has a list of all the rows which matched the last thing executed. We can print them to see what they look like:
#print results

# This is a list, and each row is a tuple (a tuple is just a list whose values you can't change, and has round instead of square brackets to denote this). You can clean the display up with a for loop:
for row in results:
    print row[0], row[1], row[2]

ingredient_id = raw_input("What's the ingredient ID of the ingredient you want to update stock? ")
new_stock = raw_input("What's the new stock? ")

db.execute("UPDATE ingredients SET stock={} WHERE id={};", (new_stock, ingredient_id)) # if you have more than one variable it needs to be a tuple --> inside parenthesis()

conn.commit() # commit the changes to the db

db.execute("SELECT id, name, stock FROM ingredients where id={};",ingredient_id)

results = db.fetchall()

print "Stock updated:"

for row in results:
    print row[0], row[1], row[2]





# Always do this after you are done with everything else.
conn.close()
