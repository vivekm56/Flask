from flask import Flask, jsonify, request, make_response
from functools import wraps
from pymongo import MongoClient
import datetime, jwt



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisthesecretkey'
client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.myMongodb #select the database
user_collection = db.users #select the collection name


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





@app.route('/')
def index():
   return "It is working"



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


@app.route('/user_details')
@check_for_token
def authorised():
    content = {'You are at the home page': 'coming soon.....',
        'Copyright': '©2018 to 2021'} 
    return jsonify({'message': 'Success'},content), 200
    
    
    



if __name__ == "__main__":
    app.run(debug=True, port=3000)
