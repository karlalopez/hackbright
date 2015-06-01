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
    """ List all users for admin"""
    print "list_users()"
    (conn, db) = connect_to_db()
    command = "SELECT * FROM users;"
    db.execute(command)
    users_list = db.fetchall()
    conn.close()
    print "list_users(): {}".format(users_list)
    return users_list
    ### Return the list of users


def create_user(username, email, password, realname, avatar):
    """ Create a new user"""
    print "create_user()"
    (conn, db) = connect_to_db()
    q = "'"
    command1 = "SELECT count(*) from users where email={1}{0}{1};".format(email,q)
    command2 = "SELECT count(*) from users where username={1}{0}{1};".format(username,q)
    db.execute(command1)
    results1 = db.fetchall()
    print "create_user() - results 1: {}".format(results1[0][0])
    db.execute(command2)
    results2 = db.fetchall()
    conn.close()
    print "create_user() - results 2: {}".format(results2[0][0])
    print "create_user() - Is there's another user with the same email or password?"
    if results1[0][0] == 0 and results2[0][0] == 0:
        print "create_user() - No. Creating user..."
        (conn, db) = connect_to_db()
        hashed_password = hash_password(password)
        print "create_user() - Entered password: "+password
        print "create_user() - Hashed password: "+hashed_password
        command = "INSERT INTO users (username, email, password, name, avatar) VALUES ({0}{1}{0},{0}{2}{0},{0}{3}{0},{0}{4}{0},{0}{5}{0});".format(q, username, email, hashed_password, realname, avatar)
        print command
        db.execute(command)
        create_user_results = db.fetchall()
        conn.commit()
        conn.close()
        print "create_user() - User created"
        print create_user_results
        return 'success'
    else:
        print "create_user() - Won't create user..."
        if results1[0][0] == 0 and results2 != 0:
            print "create_user() - The username is duplicated"
            return "username duplicated"
        if results2[0][0] == 0 and results1 != 0:
            print "create_user() -  The email is duplicated"
            return "email duplicated"
        if results2[0][0] != 0 and results1 != 0:
            print "create_user() - Both email and username are duplicated"
            return "both duplicated"


def update_user(id, attribute, new_value):
    """ Update user by id. Update atribbute to new value"""
    print "update_user()"
    (conn, db) = connect_to_db()
    ### Update user by setting attribute to new_value
    q = "'"
    command = "UPDATE users SET {1}={3}{2}{3} WHERE id={0};".format(id, attribute, new_value,q)
    print command
    db.execute(command)
    update_results = db.fetchall()
    print "update_user() - Update results: "+str(update_results)
    conn.commit()
    conn.close()
    print "update_user() - True"
    return True

def get_user_by_username(username):
    """ Get all user info by username"""
    print "get_user_by_username()"
    (conn, db) = connect_to_db()
    q = "'"
    command = "SELECT * FROM users WHERE username={1}{0}{1};".format(username,q)
    db.execute(command)
    print command
    results_by_username = db.fetchall()
    conn.commit()
    conn.close()
    print "get_user_by_username() - Update results: "+str(results_by_username)
    return results_by_username

def get_user_by_id(id):
    """ Get all user info by id"""
    print "get_user_by_id()"
    (conn, db) = connect_to_db()
    q = "'"
    command = "SELECT * FROM users WHERE id={1}{0}{1};".format(id,q)
    db.execute(command)
    print command
    results_by_id = db.fetchall()
    conn.commit()
    conn.close()
    print "get_user_by_id() - Update results: "+str(results_by_id)
    return True


def login(username,password):
    """ Login using username and password"""
    print "login()"
    (conn, db) = connect_to_db()
    q = "'"
    command = "SELECT count(*) from users where username={1}{0}{1};".format(username,q)
    print command
    db.execute(command)
    login = db.fetchall()
    print "login() - How many users with this username? "+str(len(login))
    if len(login) == 1:
        command = "SELECT password FROM users WHERE username={0}{1}{0};".format(q, username)
        print "login() - Match password and username"
        print command
        db.execute(command)
        hashed_password = db.fetchall()
        hashed_password = hashed_password[0][0]
        print "login() - Hashed password from the db: "+hashed_password
        if check_password(hashed_password, password):
            print('login() - True You entered the right password')
            command = "SELECT name FROM users WHERE username={0}{1}{0} AND password={0}{2}{0};".format(q, username, hashed_password)
            print command
            db.execute(command)
            name = db.fetchall()
            conn.close()
            return name
        else:
            print('login() - False, I am sorry but the password does not match')
    else:
        return False




def change_password(username, old_password, new_password):
    """ Change password to new password, taking username and old password"""
    print "change_password()"
    (conn, db) = connect_to_db()
    q = "'"
    print "change_password() - Old password: "+old_password
    command = "SELECT password FROM users WHERE username={0}{1}{0};".format(q, username)
    print command
    db.execute(command)
    hashed_password = db.fetchall()
    hashed_password = hashed_password[0][0]
    print "change_password() - Hashed password from the db: "+hashed_password
    if check_password(hashed_password, old_password):
        print('Change password - True You entered the right password')
        command = "SELECT id FROM users WHERE username={0}{1}{0} AND password={0}{2}{0};".format(q, username, hashed_password)
        print command
        db.execute(command)
        id = db.fetchall()
        conn.close()
        password_change = update_user(id[0][0], "password", hash_password(new_password))
        print "change_password() - Password changed: "+str(password_change)
        return 'success'
    else:
        print "change_password() - Password not changed, old password does not match"
        return "password does not match"

def hash_password(password):
    """ Hash a password"""
    print "hash_password()"
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    print "hash_password() - created"
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    """ Check hashed password with user entered password"""
    print "check_password()"
    print "check_password() - Hashed password: "+hashed_password
    print "check_password() - Password entered: "+user_password
    password, salt = hashed_password.split(':')
    print "check_password() - Split password: "+password
    print "check_password() - Hash of the password entered:"+str(hashlib.sha256(salt.encode() + user_password.encode()).hexdigest())
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def confirm_delete(username,password,user_confirmation):
    """ Confirm deletion a and delete an account"""
    print "confirm_delete()"
    (conn, db) = connect_to_db()
    q = "'"
    print "confirm_delete() - Password entered: "+password
    command = "SELECT password FROM users WHERE username={0}{1}{0};".format(q, username)
    print command
    db.execute(command)
    hashed_password = db.fetchall()
    hashed_password = hashed_password[0][0]
    print "confirm_delete() - Hashed password from the db: "+hashed_password
    if check_password(hashed_password, password):
        print "confirm_delete() - Password entered does match"
        system_confirmation = "DELETE "+str(username.upper())
        print "confirm_delete() - System Confirmation: "+str(system_confirmation)
        print "confirm_delete() - User Cofirmation :"+str(user_confirmation)
        if system_confirmation == user_confirmation:
            print "Delete - Delete message does match"
            command = "DELETE FROM users WHERE username={0}{1}{0} AND password={0}{2}{0};".format(q, username,hashed_password)
            print command
            db.execute(command)
            delete_results = db.fetchall()
            print "confirm_delete() - Completed"+str(delete_results)
            conn.commit()
            conn.close()
            return True
        else:
            print "confirm_delete() - Delete message does NOT match"
            conn.commit()
            conn.close()
            return False
