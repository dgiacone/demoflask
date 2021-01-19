from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import validators
from wtforms import HiddenField
from wtforms import PasswordField
import email_validator

def lenght_honeypot(form, field):
    if len(field.data)>0:
        raise validators.ValidationError(' El campo debe estar vacio')

class CommentForm(Form):
    username=StringField('username', 
                         [validators.required(message=' El usuario es requerido'),
                         validators.length(min=4, max=25,message='Usuario invalido')
                         ])
    email=EmailField('Correo Electronico',[validators.required(message=' El campo es requerido'),
                                           validators.Email(message='Debe ingresar un email valido')])
    comment=TextField('Comentario')
    honeypot=HiddenField('',[lenght_honeypot])

class loginForm(Form):
    username=StringField('username', 
                         [validators.required(message=' El usuario es requerido'),
                         validators.length(min=4, max=25,message='Usuario invalido')
                         ])
    password=PasswordField("Password",
                            [
                                validators.Required(message="La clave es requerida")
                            ])
    