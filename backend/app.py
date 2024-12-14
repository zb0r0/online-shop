from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*"]}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123123@48.209.24.37/sklep1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretKey:D'

db = SQLAlchemy(app)

from auth import *
from products import *
from cart import *
from orders import *
from analysis import *

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
