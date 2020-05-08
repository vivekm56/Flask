from flask import Flask



app = Flask(__name__)



@app.route('/<name>', methods=['GET'])
def hello_world(name):
	return 'Hello %s!' % name


app.run(debug = True)
