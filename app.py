from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Adoptions
adoptions = db.adoptions

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('index.html', adoptions=adoptions.find())

@app.route('/adoptions/new')
def adoptions_new():
    """Create a new adoption ad"""
    return render_template('adoptions_new.html')

if __name__ == '__main__':
    app.run(debug=True)