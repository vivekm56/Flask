from flask import Flask, jsonify, request, render_template, session, flash, make_response
from functools import wraps
import jwt
import datetime


app = Flask(__name__, template_folder='templetes')

app.config['SECRET_KEY'] = 'Thisisthesecretkey'

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
    if not session.get('logged_in'):
        return render_template('index.html', now = datetime.datetime.utcnow())
    else:
        return 'Currntly logged in'



@app.route('/public')
def public():
    return 'Anyone can view this'

@app.route('/auth')
@check_for_token
def authorised():
   content = {'You are at the home page': 'coming soon.....',
             'Copyright': '©2018 to 2021'} 
   return jsonify({'message': 'Success'},content), 200

@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        },
        app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "login required"'})



if __name__ == "__main__":
    app.run(debug=True, port= 3000)
