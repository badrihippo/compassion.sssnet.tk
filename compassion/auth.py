from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import wtforms as wtf
from flask_wtf import Form
from flask import render_template, redirect, url_for, request, flash
from .app import app, db
from .models import User

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid, use_username=False):
    try:
        if use_username:
            user = User.objects.get(username=userid)
        else:
            user = User.objects.get(id=userid)
        return user
    except db.DoesNotExist:
        return None

class LoginForm(Form):
    username = wtf.TextField('Username')
    password = wtf.PasswordField('Password')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        user = load_user(form.username.data, use_username=True)
        if (not user) or (user.password and user.password != form.password.data):
            msg = 'Invalid username or password'
            if form.errors.has_key('password'):
                form.errors['password'].append(msg)
            else:
                form.errors['password'] = [msg]
        else:
		    # All OK. Log in the user.
	        login_user(user)
	
	        return redirect(request.args.get('next') or '/')
	# Default to returning login page        
    return render_template('login.htm', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You are now logged out.')
    
    return redirect(request.args.get('next') or url_for('login'))
