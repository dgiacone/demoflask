from flask import Flask
from flask import render_template
from flask import request 
import forms
from flask_wtf import CsrfProtect  
from flask import make_response
from flask import session
from flask import url_for
from flask import redirect
from flask import flash
from flask import g # permite trabajar con variables globales
from config import DevelopmentConfig
import json

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
# Genero el Token para los formularios
csrf=CsrfProtect()

#gestor de errores
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

# Decorador para antes de request permite validar cosas antes 
# de acceder a las paginas.
@app.before_request
def before_request():
        g.test='test' # cada cliente genera una instancia de la variable global

@app.route('/', methods=['GET','POST'])
def index():
    print("index"+g.test)
    custom_cookie=request.cookies.get('customer_cookie','Undefined')
    print(custom_cookie)
    coment_form=forms.CommentForm(request.form)
    if request.method=='POST' and coment_form.validate():
        print (coment_form.username.data)
        print (coment_form.email.data)
        print (coment_form.comment.data)
    else:
        print("Error en el formulario")
    #Leo Session
    if 'username' in session:
        username=session['username']
        print(username)
    title="Curso Flask"

    return render_template('index.html',title=title, form=coment_form)

@app.route('/login', methods=['GET','POST'])
def login():
    login_form=forms.loginForm(request.form)
    if request.method=='POST' and login_form.validate():
        username=login_form.username.data
        success_message='Bienvenido {}'.format(username)
        flash(success_message)
        # Creo sesion
        session['username']=login_form.username.data
    title="Curso Flask"
    return render_template('login.html',title=title, form=login_form)

@app.route('/cookie')
def cookie():
    response=make_response(render_template('cookie.html'))
    response.set_cookie('customer_cookie','Damian')
    return response

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    # Redireccionamiento de Pagina
    return redirect(url_for('login'))

@app.route('/ajaxlogin', methods=['POST'] )
def ajaxlogin():
    print (request.form)
    username=request.form['username']
    #validacion
    response={'status':200,'username':username,'id':1}
    return json.dumps(response)

@app.after_request
def after_request_func(request):
    print("before_request is running!")
    print(g.test)
    return request


if __name__ == "__main__":
    csrf.init_app(app)
    app.run(port=8000)


