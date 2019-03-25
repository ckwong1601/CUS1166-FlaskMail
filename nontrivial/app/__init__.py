from flask import Flask, render_template
from flask_mail import Mail
from flask_sqlalchemy import sqlalchemy
from flask_login import LoginManager
from config import Config
from app.core.auth import auth
from app.core.listings import listings
from app.core.errors import errors
from app.models import db, User

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view ="auth.login"
mail = Mail(app)
db.init_app(app)
#with app.app_context():
    #db.reflect()
    #db.drop_all()
    #db.create_all()

@app.route('/')
def index():
    return render_template('index.html', title="Nontrivial")

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', title="Nontrivial - 404"), 404

app.register_blueprint(auth)
app.register_blueprint(listings)
app.register_blueprint(errors)