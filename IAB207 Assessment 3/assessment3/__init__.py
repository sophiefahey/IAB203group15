#default file for the travel package
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime    

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap5(app)
    app.secret_key = "Group15"
    #Configuring and initialising DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cookdb.sqlite'
    db.init_app(app)

    #config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    #initialising login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #user loader function 
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #add blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import events
    app.register_blueprint(events.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)


    return app

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", error=e)

@app.context_processor
def get_context():
    year = datetime.datetime.today().year 
    return dict(year=year)
