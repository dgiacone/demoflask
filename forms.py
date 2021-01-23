from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import validators
from wtforms import HiddenField
from wtforms import PasswordField
import email_validator
from models import User

def lenght_honeypot(form, field):
    if len(field.data)>0:
        raise validators.ValidationError(' El campo debe estar vacio')



class CommentForm(Form):
   
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
    honeypot=HiddenField('',[lenght_honeypot])

class createForm(Form):

    username=StringField('username', 
                         [validators.required(message=' El usuario es requerido'),
                         validators.length(min=4, max=25,message='Usuario invalido')
                         ])
    email=EmailField('Correo Electronico',[validators.required(message=' El campo es requerido'),
                                         validators.Email(message='Debe ingresar un email valido')])
    password=PasswordField("Password",
                            [
                                validators.Required(message="La clave es requerida")])
    honeypot=HiddenField('',[lenght_honeypot])

    def validate_username(form,field):
        username=field.data
        user=User.query.filter_by(username=username).first()
        if user is not  None:
             raise validators.ValidationError(' El usuario ya existe')