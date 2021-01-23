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
from models import db
from models import User
from models import Comment

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
        g.test=''
        if 'username' not in session  and request.endpoint in ['comment']:
            return redirect(url_for('login'))
        elif 'username' in session and request.endpoint in ['login','create']:
            return redirect(url_for('index'))

@app.route('/', methods=['GET','POST'])
def index():
     
    custom_cookie=request.cookies.get('customer_cookie','Undefined')
 
    coment_form=forms.CommentForm(request.form)
    
    title="Curso Flask"

    return render_template('index.html',title=title, form=coment_form)

@app.route('/login', methods=['GET','POST'])
def login():
    login_form=forms.loginForm(request.form)
    if request.method=='POST' and login_form.validate():
        username=login_form.username.data
        password=login_form.password.data

        user=User.query.filter_by(username=username).first()
         
        if user is not None and user.verify_password(password):
            success_message='Bienvenido {}'.format(username)
            flash(success_message)
            session['username']=username
            session['user_id']=user.id
            return redirect(url_for('index'))
        else:
            error_message='Usuario no valido'.format(username)
            flash(error_message)

       
  
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


@app.route('/create',methods=['GET','POST'])
def create():
    create_form=forms.createForm(request.form)
    if request.method=='POST' and create_form.validate():
        success_message="Usuario registrado en base de datos"
 
        user=User(create_form.username.data,create_form.password.data,create_form.email.data)

        db.session.add(user)
        db.session.commit()

        flash(success_message)
    return render_template('create.html', form=create_form)

@app.route('/comment',methods=['GET','POST'])
def comment():
    comment_form=forms.CommentForm(request.form)
    if request.method=='POST' and comment_form.validate():
        user_id=session['user_id']
        comment=Comment(user_id=user_id,text=comment_form.comment.data)
        db.session.add(comment)
        db.session.commit()
        success_message="Nuevo Comentario Creado"
        flash(success_message)
    title="Curso Flask"
    return render_template('comment.html', title=title, form=comment_form)

@app.route('/reviews/',methods=['GET','POST'])
@app.route('/reviews/<int:page>',methods=['GET','POST'])
def reviews(page=1):
    per_page=3
    comment=Comment.query.join(User).add_columns(User.username,Comment.text).paginate(page,per_page,False)



    return render_template('reviews.html', comments=comment)
# --------------------------------------------------------------------------------------
@app.after_request
def after_request_func(request):
    print("before_request is running!")
    print(g.test)
    return request 

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with  app.app_context():
        db.create_all()
    
    app.run(port=8000)



