from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__, template_folder='templetes' )

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('index.html', error=error)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
