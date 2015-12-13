from flask import render_template, flash, request, url_for, redirect, abort
from app import app
from auth import login_manager, current_user
from models import User, Pet, GENDER_CHOICES, ContactUnverifiedEmail
import wtforms as wtf
from flask_wtf import Form
import random

from flask_mongoengine.wtf import model_form

@app.route('/')
def index():
    return render_template('index.htm')

class SignupForm(Form):
    first_name = wtf.StringField(validators=[wtf.validators.required()])
    last_name = wtf.StringField(validators=[wtf.validators.required()])
    gender = wtf.SelectField(choices=GENDER_CHOICES)
    email = wtf.StringField(u'Email',
        validators=[wtf.validators.required(), wtf.validators.email()])
    username = wtf.StringField(validators=[wtf.validators.required(),
        wtf.validators.Length(min=4, max=25,
            message=u'Username must be between 4 and 25 characters long')])
    password = wtf.PasswordField(validators=[wtf.validators.required()])
    confirm_password = wtf.PasswordField(validators=[wtf.validators.required()])

    def validate_password(form, field):
        if field.data != form.confirm_password.data:
            raise wtf.ValidationError('Passwords do not match')

@app.route('/accounts/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate():
        u = User()
        u.username = form.username.data
        u.password = form.password.data #TODO: Hash this!
        u.first_name = form.first_name.data
        u.last_name = form.last_name.data
        u.gender = form.gender.data

        c = ContactUnverifiedEmail()
        c.email = form.email.data
        # 6-digit verification code
        c.verification_code = ''.join(random.choice(c.allowed_letters) for x in range(6))

        u.unverified_emails.append(c)
        u.save()

        msg = 'A verification email has been sent to %(email)s. Please check your inbox for instructions' % {
            'email': form.email.data,
            }

        flash(msg)

        return redirect(url_for('login'))
    else:
        return render_template('accounts/signup.htm', form=form)
    return redirect(url_for('index'))

@app.route('/u/<username>/')
def user_profile(username):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        abort(404)
    p = Pet.objects.filter(rescuer=u)
    return render_template('accounts/user_profile.htm', user=u, pets=p)

@app.route('/p/<petid>/')
def pet_profile(petid):
    try:
        p = Pet.objects.get(id=petid)
    except Pet.DoesNotExist:
        abort(404)
    return render_template('pets/pet_profile.htm', pet=p)
