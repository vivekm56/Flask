from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__, template_folder='templetes')

@app.route('/')
def home():
    return render_template('home.html', now = datetime.utcnow())

app.run(debug=True, port=3000)
