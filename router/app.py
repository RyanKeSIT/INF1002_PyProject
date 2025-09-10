# Import libraries
from flask import Flask

# Import modules
from model.index import *
from model.tools import *

# API config
app = Flask(__name__)

# API routes
@app.route("/")
def index():
    return "Hello World!"