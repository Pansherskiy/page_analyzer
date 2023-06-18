import os
from dotenv import load_dotenv
from flask import Flask, render_template


app = Flask(__name__)


load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(_):
    return render_template('not_found404.html'), 404
