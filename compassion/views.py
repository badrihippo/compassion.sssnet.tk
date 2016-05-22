from flask import render_template, flash, request, url_for, redirect, abort, send_file
from werkzeug import secure_filename
from datetime import datetime
import random
from .app import app
from .auth import login_manager, current_user, login_required
from .models import model_form, User, Pet, Species, ContactUnverifiedEmail, ImageFile, db
from .forms import SignupForm, NewPetForm

# For GridFS
from tempfile import NamedTemporaryFile
from shutil import copyfileobj

from flask_mongoengine.wtf import model_form

@app.route('/')
def index():
    return render_template('index.htm')

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

@app.route('/a/rescue/add/', methods=['GET', 'POST'])
@login_required
def pet_add():
    form = NewPetForm(data={'rescue_time': datetime.now()})
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
        #p.save()

        # form.photo.data.save('uploads/' + filename)
        if form.photo.data:
            i = ImageFile()
            i.filename = secure_filename(form.photo.data.filename)
            i.payload.put(form.photo.data.stream, content_type=form.photo.data.mimetype, filename=i.filename)
            i.save()
            p.photos.append(i)

        p.save()

        msg = '%(name)s was added successfully' % {
            'name': p.name,
            }

        flash(msg)

        return redirect(url_for('pet_profile', petid=p.id))
    return render_template('pets/add_pet.htm', form=form)

@app.route('/image/<string:file_id>')
def show_image(file_id):
    image = ImageFile.objects(id=file_id).first()
    if image:
        tempFileObj = NamedTemporaryFile(mode='w+b',suffix='jpg')
        copyfileobj(image.payload,tempFileObj)
        tempFileObj.seek(0,0)
        return send_file(tempFileObj, mimetype='image')
    else:
        return "404" # might want to return something real here too
