from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password1')
    # TODO: Implement login validation and logic

    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(username) < 6:
            flash('Username must be at least 6 characters, try again!', category='failure')
        elif password1 != password2:
            flash('Passwords must be equal, try again!', category='failure')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters long, try again!', category='failure')
        else:
            flash('Success', category='success')
            return redirect(url_for('main'))
    return render_template('auth/register.html')

@app.route('/main')
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)