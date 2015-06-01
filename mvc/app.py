from flask import Flask, render_template, request, session, redirect
from models import *

app = Flask(__name__)
app.secret_key = 'thisisasecret' #To "log in" a user, first make sure you have imported the session - you'll also need to set up an app secret key.


@app.route('/')
def show_index_page():
    print "Rendering index"
    return render_template("index.html")

@app.route('/signup')
def show_signup_page():
    print "Rendering sign up"
    ### Show the signup page
    return render_template("signup.html")


@app.route('/submit-signup', methods=['POST'])
def submit_signup_form():
    print "Submitting sign up form"
    print request.form
    username = request.form.get('username')
    print "Sign up - Username: "+username
    email = request.form.get('email')
    password = request.form.get('password')
    print "Sign up - Password: "+password
    #password = hash_password(password)
    realname = request.form.get('name')
    avatar = request.form.get('avatar')
    print "Sign up - Calling create_user()"
    create = create_user(username, email, password, realname, avatar)
    print "Sign up - Results from create_user(): {}".format(create)
    if create == "success":
        name=login(username,password)
        if name == False:
            print "Sign up - Sign up successful, login failed"
            message = "You signed up successfuly but your login failed."
            button = "login"
        else:
            session['username'] = username  #this sets a username for the user
            print "Sign up - Sign up successful, login successful"
            ### Redirect to logged-in page
            return redirect('logged-in')
    if create == "email duplicated":
        print "Sign up - Sign up failed, email duplicated"
        message = "The email {} is already in our database. Try login.".format(email)
        button = "login"
    if create == "username duplicated":
        print "Sign up - Sign up failed, username duplicated"
        message = "The username {} is already in our database. Try a new one.".format(username)
        button = "signup"
    if create == "both duplicated":
        print "Sign up - Sign up failed, username and email duplicated"
        message = "Man... Both username and email are already on our database. Try login."
        button = "login"
    print "Sign up - Rendering submit-login, passing message and button"
    return render_template("submit-login.html",message=message, button=button)


@app.route('/login')
def show_login_page():
    ### Show the login page
    print "Rendering login"
    return render_template("login.html")


@app.route('/submit-login', methods=['POST'])
def submit_login_form():
    print "Login - Submitting login form"
    ### Submit the login form
    print request.form
    username = request.form.get('username')
    print "Login - Username: "+username
    password = request.form.get('password')
    print "Login - Password: "+username
    print "Login - Calling login()"
    name=login(username,password)
    print name
    if name:
        print "Login - Login succesful. Creating session"
        session['username'] = username  #this sets a username for the user
        print "login - Redirecting to logged-in"
        ### Redirect to logged-in page
        return redirect('logged-in')
    else:
        print "Login - Login failed, password don't match or not a user yet"
        message = "Sorry, your password doesn't match or you are not a user yet. Try signing up."
        button = "signup"
        print "Login - Rendering submit-login to show sign up button"
        return render_template("submit-login.html",message=message, button=button)


@app.route('/logged-in')
def show_logged_in_page():
    print "Show logged-in page"
    print "Logged-in: Looking for session"
    if session.get('username'): # this will be executed if 'username' is present in the session
        print "Logged-in: Found session"
        username = session['username']
        return render_template("logged-in.html",username=username)
    else:
        print "Logged-in: No session"
        return "You are not logged in"

@app.route('/logout')
def show_logout_page():
    print "User logout"
    print "Logout: Deleting settion"
    del session['username']
    print "Logout: Rendering index"
    return render_template("index.html")



@app.route('/admin')
def admin_page():
    print "Admin"
    print "Admin - Checking if Admin"
    if session.get('username') =="admin": # check if session == admin?
        print "Admin - Okay, it's an Admin"
        print "Admin - Calling list_users()"
        user_list=list_users()
        print user_list
        print "Admin - Rendering admin with users info"
        return render_template("admin.html",user_list=user_list)
    else:
        print "Admin - Not admin"
        return "Sorry, you are not Admin"


@app.route('/user-info')
def get_user_info():
    print "User info"
    print "User info - Looking for session"
    if session.get('username'): # this will be executed if 'username' is present in the session
        print "User info - Found session"
        username = session.get('username')
        print "User info - Username: "+str(username)
        print "Admin - Calling get_user_by_username()"
        user_info=get_user_by_username(username)
        print "User info - List user info:"
        print user_info
        print "User info - Rendering user-info"
        return render_template("user-info.html",user_info=user_info)
    else:
        print "User info - No session"
        return "You are not logged in"

@app.route('/change-password', methods=['POST'])
def change_user_password():
    print "Change user password"
    print "Change user password - Look for session"
    if session.get('username'): # this will be executed if 'username' is present in the session
        print "Change user password - Found session"
        username = session.get('username')
        print "Change user password - Username: "+str(username)
        print request.form
        old_password = request.form.get('old_password')
        print "Change user password - Old Password: "+str(old_password)
        new_password = request.form.get('new_password')
        print "Change user password - New Password: "+str(new_password)
        print "Change user password - Calling change_password()"
        change_password_results = change_password(username, old_password, new_password)
        if change_password_results == "success":
            message = "Your password was sucessfully changed."
            print "Change user password - Password changed"
            username = session.get('username')
            print "Change user password - Calling get_user_by_username():"
            user_info=get_user_by_username(username)
            print user_info
            print "Change user password - Rendering change-password with success message and updated user info"
            return render_template("change-password.html", message=message, user_info=user_info)
        if change_password_results == "password does not match":
            print "Change user password - Password not changed, password does not match"
            message = "Wrong old password"
            username = session.get('username')
            print "Change user password - Calling get_user_by_username():"
            user_info=get_user_by_username(username)
            print user_info
            print "Change user password - Rendering change-password with failure message and updated user info"
            return render_template("change-password.html", message=message, user_info=user_info)
    else:
        print "Change user password - No session"
        return "You are not logged in"

@app.route('/delete-account')
def delete_account():
    print "Delete account"
    print "Delete account - Look for session"
    if session.get('username'): # this will be executed if 'username' is present in the session
        print "Delete account - Session found"
        username = session.get('username')
        print "Delete account - Username: "+str(username)
        print "Delete account - Calling get_user_by_username():"
        user_info=get_user_by_username(username)
        print user_info
        print "Delete account - Rendering delete-account with updated user info"
        return render_template("delete-account.html",user_info=user_info)
    else:
        print "Delete account - No session"
        return "You are not logged in"

@app.route('/submit-delete', methods=['POST'])
def submit_delete_form():
    print "Submit delete"
    print "Submit delete - Look for session"
    if session.get('username'): # this will be executed if 'username' is present in the session
        print "Submit delete - Session found"
        print request.form
        username = request.form.get('username')
        print "Submit delete - Username: "+str(username)
        password = request.form.get('password')
        print "Submit delete - Password: "+str(password)
        confirmation = request.form.get('confirmation')
        print "Submit delete - Confirmation message: "+str(confirmation)
        print "Submit delete - Call confirm_delete()"
        delete_results = confirm_delete(username,password,confirmation)
        print "Submit delete - Results: "+str(delete_results)
        if delete_results == True:
            print "Submit delete - Account deleted"
            print "Submit delete - Delete session"
            del session['username']
            message = "Your account has been deleted."
            button = "signup"
            print "Submit delete - Rendering submit-login with success message and sign up button"
            return render_template("submit-login.html",message=message, button=button)
        else:
            print "Submit delete - Account not deleted"
            del session['username']
            print "Submit delete - Delete session"
            message = "Sorry, your password doesn't match or your delete confirmation was wrong."
            button = "login"
            print "Submit delete - Rendering submit-login with failure message and login button"
            return render_template("submit-login.html",message=message, button=button)
    else:
        return "You are not logged in"





if __name__=='__main__':
    app.run(debug=True)
