from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
from datetime import timedelta
import requests

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123123@localhost/sklep'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretKey:D'

db = SQLAlchemy(app)

from auth import *
from products import *
from cart import *
from orders import *

if __name__ == "__main__":
    app.run(debug=True)
