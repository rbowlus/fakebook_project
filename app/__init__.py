from flask import Flask

app = Flask(__name__)

#building the rest of flask application
from .import routes