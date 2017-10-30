from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
lm = LoginManager()
lm.login_view = 'login'

# print(app.static_folder)

from app import views
import models

if __name__ == '__main__':
    app.run(debug=True)
