from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '688bfe736440a24a0981a865e8815b58'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'timefornothingwc'
app.config['MAIL_PASSWORD'] = 'anniebad'

mail = Mail(app)

db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_message_category = 'info'


from breeze import routes
