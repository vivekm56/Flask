from flask import Flask, jsonify, request, make_response
from functools import wraps
from pymongo import MongoClient
from email.message import EmailMessage

import datetime, jwt, smtplib, imghdr, os



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisthesecretkey'
client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.myMongodb #select the database
user_collection = db.users #select the collection name

# function for token verification
def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped



# email functionality added here
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

contacts = ['tahiley542@aprimail.com', 'xorogan715@ximtyl.com']

msg = EmailMessage()
msg['Subject'] = 'New Password'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'bibiy60021@etoymail.com','xorogan715@ximtyl.com'

msg.set_content('This is a plain text email')

msg.add_alternative("""\
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;"><a href="http://www.google.com">click here</a></h1>
    </body>
</html>
""", subtype='html')







@app.route('/')
def index():
   return "It is working"


# user register
@app.route('/register', methods=['POST'])
def register():
    if request.form["username"] == "" or request.form["password"] == "" or request.form['email_id'] == "" or request.form['address'] == "" :
        return jsonify({"error": "Please fill all fields"})

    user = user_collection.find({'name' : request.form['username']})
    mail = user_collection.find({'email_id' : request.form['email_id']})

    if (user.count() != 0):
        return jsonify({'error': 'username already exist '})
    
    elif (mail.count() != 0):
        return jsonify({'error': 'email already exist '})
# """To add an item to the database. its a post request and we use databasename.insert()"""

    user_collection.insert({
       'name':request.form['username'],
       'password':request.form['password'],
       'email_id':request.form['email_id'],
       'address':request.form['address']
   }) 
    return "you are registered successfully"
   


# user login
@app.route('/login', methods=['POST'])
def login():
    if request.form["username"] == "" or request.form["password"] == "":
        return jsonify({"error": "Please provide username and password"})
    login_user = user_collection.find({'name' : request.form['username']})

    if (login_user.count() == 0):
        return jsonify({'error': 'no username exist '})

    if request.form['password'] ==  login_user[0]['password']:
        token = jwt.encode({
            'user': request.form['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        },
        app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "login required"'})

# user details
@app.route('/user_details')
@check_for_token
def authorised():
    content = {'You are at the home page': 'coming soon.....',
        'Copyright': '©2018 to 2021'} 
    return jsonify({'message': 'Success'},content), 200
    
# forget_password
@app.route('/forget_password', methods = ['POST'])
def forget_password():
    mail = user_collection.find({'email_id' : request.form['email_id']})
    if request.form['email_id'] == '':
        return jsonify({'error': 'please enter your registered email id'})

    if (mail.count() == 0):
        return jsonify({'error': 'this email id does not exist '})
    
    elif (mail.count() != 0):

        token = jwt.encode({
            'user': request.form['email_id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        },
        app.config['SECRET_KEY'])
        mail_body_content = jsonify({'token': token.decode('utf-8')})
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        return jsonify({'success': 'a link has been sent to your email id, check your email and click on that link to create a new password'},{'token': token.decode('utf-8')})
    return 'your password has been changed'
    



if __name__ == "__main__":
    app.run(debug=True, port=3000)
