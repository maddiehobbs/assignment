from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            flash("logged in successfully!", category='success')
            login_user(user, remember=True)
            return redirect(url_for('main'))
        flash("Invalid username or password, try again!", category='failure')
    return render_template('auth/login.html')

def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        is_admin = bool(request.form.get('admin'))

        user_exists = User.query.filter_by(username=username).first()

        if user_exists:
            flash('Username already exists, try again!', category='failure')

        elif len(username) < 6:
            flash('Username must be at least 6 characters, try again!', category='failure')
        elif password1 != password2:
            flash('Passwords must be equal, try again!', category='failure')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters long, try again!', category='failure')
        else:
            new_user = User(username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'), admin=is_admin)
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created successfully', category='success')
                return redirect(url_for('main'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred.'+ str(e) + 'Please try again.', category='failure')
    return render_template('auth/register.html')

def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('login_page'))