#default file for the travel package
from flask import Flask
from  . import views,events,auth
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views.viewsbp)
    # Bootstrap(app)
    # app.register_blueprint(views.viewsbp)
    app.register_blueprint(auth.bookingsbp)
    app.register_blueprint(events.eventbp)
    app.secret_key = "Group15"
    return app