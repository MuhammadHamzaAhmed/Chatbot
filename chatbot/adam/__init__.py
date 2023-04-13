from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app, origins=['*'])

app.secret_key = '3294786542378ghegfr234'
SESSION_TYPE = 'sqlalchemy'
app.config.from_object(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SECRET_KEY"] = "3294786542378ghegfr234"

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['Access-Control-Allow-Origin'] = '*'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root123@bot_db:3307/BotDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# three line comment
app.config['SQLALCHEMY_BINDS'] = {
    'FormDB': 'mysql+pymysql://root:root123@bot_db:3307/BotDB'
}

db = SQLAlchemy(app)

from adam.routes.bot import *