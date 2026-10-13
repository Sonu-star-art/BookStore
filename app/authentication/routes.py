from flask import Flask, Blueprint, render_template, url_for, redirect, request, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from models import User
from . import auth


@auth.route('/login')
def login():
    if 'user_id' in session:
        session.pop('user_id')

    return render_template('login.html')


@auth.route('/login/submit-login', methods=['POST'])
def submit_login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if username == "" or password == "":
            flash(message="something went wrong, please try again")
            return redirect(url_for('auth.login'))

        user : User = User.query.filter_by(username=username).first()  # All usernames SHOULD be unique
        print(user)
        if not user:
            flash(message="Invalid username")
            return redirect(url_for('auth.login'))

        password_valid = check_password_hash(user.password, password)

        if password_valid:
            session['user_id'] = user.user_id
            print("success")
            return redirect(url_for('main.home'))

        print("password not valid")
        flash(message="Invalid password")

    return redirect(url_for('auth.login'))


@auth.route('/register')
def register():
    return render_template('register.html')


@auth.route('/register/submit-register', methods=['POST'])
def submit_register():
    if request.method == 'POST':

        # Try create user from inputs
        try:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            # the checkbox input in html returns either a custom string e.g. 'yes' or it returns Null, so we check if the
            # is_admin is in the form or if it's null (if it's in the form, that means the user checked the box)
            if 'is_admin' in request.form:
                is_admin_bool = True
            else:
                is_admin_bool = False

            # Check for empty inputs
            if username.strip() == "" or password.strip() == "" or email.strip() == "":
                flash(message="Please enter valid details")
                return redirect(url_for('auth.register'))

            # Checks if user already exists
            if User.query.filter_by(username=username).first() is not None:
                flash("username already exists")
                return redirect(url_for("auth.register"))

            # Hash that password
            hashed_password = generate_password_hash(password=password)

            # Create user (phone number and address are just dummy data to make testing easier)
            user : User = User(username=username, password=hashed_password, email=email, is_admin=is_admin_bool,
                               phone_number="12345", address="some street")

        except:
            flash(message="Something went wrong, please try again")
            return redirect(url_for('auth.register'))

        # Add user to database
        db.session.add(user)
        db.session.commit()
        
        flash("Succesfully registered")
        return redirect(url_for('auth.login'))

    return redirect(url_for('auth.register'))







