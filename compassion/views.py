from flask import render_template, flash, request, url_for, redirect, abort
from app import app
from auth import login_manager, current_user, login_required
from models import model_form, User, Pet, Species, GENDER_CHOICES, ContactUnverifiedEmail
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

@app.route('/p/list')
def pet_list():
    pets = Pet.objects()
    return render_template('pets/pet_list.htm', pets=pets)

# TODO: Use model_form to make it DRY

class NewPetForm(Form):
    rescue_time = wtf.DateTimeField(validators=[wtf.validators.required()])
    name = wtf.StringField(validators=[wtf.validators.required()])
    species = wtf.StringField(validators=[wtf.validators.required()])
    gender = wtf.SelectField(choices=GENDER_CHOICES)
    description = wtf.TextAreaField(validators=[wtf.validators.required()])
    # TODO: photos

@app.route('/a/rescue/add/', methods=['GET', 'POST'])
@login_required
def pet_add():
    form = NewPetForm()
    if request.method == 'POST' and form.validate():
        try:
            s = Species.objects.get(name=form.species.data)
        except Species.DoesNotExist:
            try:
                s = Species.objects.get(scientific_name=form.species.data)
            except Species.DoesNotExist:
                s = Species(name=form.species.data)
                s.save()

        p = Pet()
        p.rescuer = User.objects.get(username=current_user.username)
        p.name = form.name.data
        p.species = s
        pgender = form.gender.data
        prescue_time = form.rescue_time.data
        p.description = form.description.data
        # TODO: p.photos
        p.save()

        msg = '%(name)s was added successfully' % {
            'name': p.name,
            }

        flash(msg)

        return redirect(url_for('pet_profile', petid=p.id))
    return render_template('pets/add_pet.htm', form=form)
