from flask import Flask

app = Flask(__name__)

@app.route('/<name>', methods=['GET']) #put any name at the end of the url ex:- http://127.0.0.1:5000/name
def hello_world(name):
	return 'Hello %s!' % name

app.run(debug = True) #defaults to false. If set to true, provides a debug information. We can also use host, port, options app.run(debug, host, port,options)
