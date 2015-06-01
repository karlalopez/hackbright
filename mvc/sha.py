import uuid
import hashlib

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    print "== Hash_ Salt: "+salt
    print "== Hash_:"+hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    print "== Hash_ hash+salt: "+hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    print "== Check_ hashed password: "+hashed_password
    print "== Check_ salt: "+salt
    print "== Check_ password: "+password
    print "== Check: =="+ hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
    if password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest():
        print "True"
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
    else:
        print "False"

new_pass = raw_input('Please enter a password: ')
print "new_pass: "+new_pass
hashed_password = hash_password(new_pass)
print "hash+password: "+hashed_password
print('The string to store in the db is: ' + hashed_password)
old_pass = raw_input('Now please enter the password again to check: ')
print "old_pass: "+old_pass
print "check_password(hashed_password, old_pass):"
if check_password(hashed_password, old_pass):
    print(' True You entered the right password')
else:
    print(' False I am sorry but the password does not match')
