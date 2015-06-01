from flask import Flask, render_template, request, session, redirect
from models import *

app = Flask(__name__)
app.secret_key = 'thisisasecret' #To "log in" a user, first make sure you have imported the session - you'll also need to set up an app secret key.


@app.route('/')
def show_index_page():
    return render_template("index.html")

@app.route('/signup')
def show_signup_page():
    ### Show the signup page
    return render_template("signup.html")


@app.route('/submit-signup', methods=['POST'])
def submit_signup_form():
    print request.form
    username = request.form.get('username')
    print username
    email = request.form.get('email')
    password = request.form.get('password')
    realname = request.form.get('name')
    avatar = request.form.get('avatar')
    create = create_user(username, email, password, realname, avatar)
    print "create results in app.py: {}".format(create)
    if create == "success":
        name=login(username,password)
        if name == False:
            message = "You signed up successfuly but your login failed."
            button = "login"
        else:
            session['username'] = username  #this sets a username for the user
            ### Redirect to logged-in page
            return redirect('logged-in')
    if create == "email duplicated":
        message = "The email {} is already in our database. Try login.".format(email)
        button = "login"
    if create == "username duplicated":
        message = "The username {} is already in our database. Try a new one.".format(username)
        button = "signup"
    if create == "both duplicated":
        message = "Man... Both username and email are already on our database. Try login."
        button = "login"
    return render_template("submit-login.html",message=message, button=button)


@app.route('/login')
def show_login_page():
    ### Show the login page
    return render_template("login.html")


@app.route('/submit-login', methods=['POST'])
def submit_login_form():
    ### Submit the login form
    print request.form
    username = request.form.get('username')
    password = request.form.get('password')
    name=login(username,password)
    print name
    if name:
        session['username'] = username  #this sets a username for the user
        ### Redirect to logged-in page
        return redirect('logged-in')
    else:
        message = "Sorry, your password doesn't match or you are not a user yet. Try signing up."
        button = "signup"
        return render_template("submit-login.html",message=message, button=button)


@app.route('/logged-in')
def show_logged_in_page():
    if session.get('username'): # this will be executed if 'username' is present in the session
        username = session['username']
        return render_template("logged-in.html",username=username)
    else:
        return "You are not logged in"

@app.route('/logout')
def show_logout_page():
    del session['username']
    return render_template("index.html")



@app.route('/admin')
def list_all_users():
    # check if session == admin?
    user_list=list_users()
    print user_list
    return render_template("admin.html",user_list=user_list)

@app.route('/user-info')
def get_user_info():
    if session.get('username'): # this will be executed if 'username' is present in the session
        username = session.get('username')
        user_info=get_user_by_username(username)
        print user_info
        return render_template("user-info.html",user_info=user_info)
    else:
        return "You are not logged in"

@app.route('/change-password', methods=['POST'])
def change_user_password():
    if session.get('username'): # this will be executed if 'username' is present in the session
        username = session.get('username')
        print username
        print request.form
        old_password = request.form.get('old_password')
        print old_password
        new_password = request.form.get('new_password')
        print new_password
        result = change_password(username, old_password, new_password)
        if result == "success":
            message = "Your password was sucessfully changed."
            username = session.get('username')
            user_info=get_user_by_username(username)
            print user_info
            return render_template("change-password.html", message=message, user_info=user_info)
        if result == "password does not match":
            message = "Wrong old password"
            username = session.get('username')
            user_info=get_user_by_username(username)
            print user_info
            return render_template("change-password.html", message=message, user_info=user_info)
    else:
        return "You are not logged in"



if __name__=='__main__':
    app.run(debug=True)
