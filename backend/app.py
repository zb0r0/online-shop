from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://192.168.18.2:8080", "http://48.209.24.37:8080"
                                         , "http://48.209.24.37:8081"]}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123123@48.209.24.37/sklep'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretKey:D'

db = SQLAlchemy(app)

from auth import *
from products import *
from cart import *
from orders import *

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
