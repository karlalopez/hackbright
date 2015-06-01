import sqlite3
import uuid
import hashlib
import string


DBFILE = 'users.db'  # This defines which file on disc to look in

def connect_to_db():
    """ Get a connection and a cursor. """
    conn = sqlite3.connect(DBFILE)
    db = conn.cursor()
    return (conn, db)


def list_users():
    (conn, db) = connect_to_db()
    command = "SELECT * FROM users;"
    db.execute(command)
    results = db.fetchall()
    conn.close()
    print "List users: {}".format(results)
    return results
    ### Return the list of users


def create_user(username, email, password, realname, avatar):
    print "Create_user Function"
    (conn, db) = connect_to_db()
    q = "'"
    command1 = "SELECT count(*) from users where email={1}{0}{1};".format(email,q)
    command2 = "SELECT count(*) from users where username={1}{0}{1};".format(username,q)
    db.execute(command1)
    results1 = db.fetchall()
    print "results 1: {}".format(results1[0][0])
    db.execute(command2)
    results2 = db.fetchall()
    conn.close()
    print "results 2: {}".format(results2[0][0])
    if results1[0][0] == 0 and results2[0][0] == 0:
        print "Creating user"
        (conn, db) = connect_to_db()
        hashed_password = hash_password(password)
        print "Password: "+password
        print "Hashed password: "+hashed_password
        command = "INSERT INTO users (username, email, password, name, avatar) VALUES ({0}{1}{0},{0}{2}{0},{0}{3}{0},{0}{4}{0},{0}{5}{0});".format(q, username, email, hashed_password, realname, avatar)
        print command
        db.execute(command)
        results = db.fetchall()
        conn.commit()
        conn.close()
        print "User created"
        print results
        return 'success'
    else:
        print "Won't create user"
        if results1[0][0] == 0 and results2 != 0:
            print "username duplicated"
            return "username duplicated"
        if results2[0][0] == 0 and results1 != 0:
            print "email duplicated"
            return "email duplicated"
        if results2[0][0] != 0 and results1 != 0:
            print "both email and username duplicated"
            return "both duplicated"


def update_user(id, attribute, new_value):
    (conn, db) = connect_to_db()
    ### Update user by setting attribute to new_value
    q = "'"
    command = "UPDATE users SET {1}={3}{2}{3} WHERE id={0};".format(id, attribute, new_value,q)
    print command
    db.execute(command)
    results = db.fetchall()
    conn.commit()
    conn.close()
    return 'success'

def get_user_by_username(username):
    (conn, db) = connect_to_db()
    q = "'"
    command = "SELECT * FROM users WHERE username={1}{0}{1};".format(username,q)
    db.execute(command)
    print command
    results = db.fetchall()
    print results
    conn.commit()
    conn.close()
    return results

def get_user_by_id(id):
    (conn, db) = connect_to_db()
    q = "'"
    command = "select * FROM users WHERE id={1}{0}{1};".format(id,q)
    db.execute(command)
    print command
    results = db.fetchall()
    print results
    conn.commit()
    conn.close()
    return 'success'


def login(username,password):
    print "Login Function"
    (conn, db) = connect_to_db()
    q = "'"
    command = "SELECT count(*) from users where username={1}{0}{1};".format(username,q)
    print command
    db.execute(command)
    login = db.fetchall()
    print "How many users? "+str(len(login))
    if len(login) == 1:
        command = "SELECT password FROM users WHERE username={0}{1}{0};".format(q, username)
        print command
        db.execute(command)
        hashed_password = db.fetchall()
        hashed_password = hashed_password[0][0]
        print "Hashed password from the db: "+hashed_password
        if check_password(hashed_password, password):
            print(' True You entered the right password')
            command = "SELECT name FROM users WHERE username={0}{1}{0} AND password={0}{2}{0};".format(q, username, hashed_password)
            print command
            db.execute(command)
            name = db.fetchall()
            conn.close()
            return name
        else:
            print(' False I am sorry but the password does not match')
    else:
        return False




def change_password(username, old_password, new_password):
    (conn, db) = connect_to_db()
    q = "'"
    print "Old password: "+old_password
    command = "SELECT password FROM users WHERE username={0}{1}{0};".format(q, username)
    print command
    db.execute(command)
    hashed_password = db.fetchall()
    hashed_password = hashed_password[0][0]
    print "Hashed password from the db: "+hashed_password
    if check_password(hashed_password, old_password):
        print(' True You entered the right password')
        command = "SELECT id FROM users WHERE username={0}{1}{0} AND password={0}{2}{0};".format(q, username, hashed_password)
        print command
        db.execute(command)
        id = db.fetchall()
        conn.close()
        password_change = update_user(id[0][0], "password", hash_password(new_password))
        print "Password changed: "+password_change
        return 'success'
    else:
        print "Password not changed, old password does not match"
        return "password does not match"

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    print "Check - Hashed password: "+hashed_password
    print "Check - Password entered: "+user_password
    password, salt = hashed_password.split(':')
    print "Check - Split password: "+password
    print "Check - Hassh of the password entered:"+str(hashlib.sha256(salt.encode() + user_password.encode()).hexdigest())
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def confirm_delete(username,password,user_confirmation):
    (conn, db) = connect_to_db()
    q = "'"
    print "Delete - Password entered: "+password
    command = "SELECT password FROM users WHERE username={0}{1}{0};".format(q, username)
    print command
    db.execute(command)
    hashed_password = db.fetchall()
    hashed_password = hashed_password[0][0]
    print "Delete - Hashed password from the db: "+hashed_password
    if check_password(hashed_password, password):
        print "Delete - Password entered does match"
        system_confirmation = "DELETE "+str(username.upper())
        print "Delete - System Confirmation: "+str(system_confirmation)
        print "Delete - User Cofirmation :"+str(user_confirmation)
        if system_confirmation == user_confirmation:
            print "Delete - Delete message does match"
            command = "DELETE FROM users WHERE username={0}{1}{0} AND password={0}{2}{0};".format(q, username,hashed_password)
            print command
            db.execute(command)
            delete_results = db.fetchall()
            print "Delete - Completed"+str(delete_results)
            conn.commit()
            conn.close()
            return True
        else:
            print "Delete - Delete message does NOT match"
            conn.commit()
            conn.close()
            return False
