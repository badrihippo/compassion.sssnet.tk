import wtforms as wtf
from flask_wtf import Form, RecaptchaField
from .models import GENDER_CHOICES

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

    recaptcha = RecaptchaField()

    def validate_password(form, field):
        if field.data != form.confirm_password.data:
            raise wtf.ValidationError('Passwords do not match')

# TODO: Use model_form to make it DRY

class NewPetForm(Form):
    rescue_time = wtf.DateTimeField(validators=[wtf.validators.required()])
    name = wtf.StringField(validators=[wtf.validators.required()])
    species = wtf.StringField(validators=[wtf.validators.required()])
    gender = wtf.SelectField(choices=GENDER_CHOICES)
    description = wtf.TextAreaField(validators=[wtf.validators.required()])
    photo = wtf.FileField(u'Image File')
