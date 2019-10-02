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
    """Return to the new adoption ad page"""
    return render_template('adoptions_new.html')

@app.route('/adoptions', methods=['POST'])
def adoptions_submit():
    """Submit a new adoption ad. Allows the user to input information for the adoption ad."""
adoption = {
        'breed of the animal': request.form.get('breed of the animal'),
        'description of the animal': request.form.get('description of the animal')
        'price': request.form.get('price')
        'img_url': request.form.get('img_url')
    }
    print(adoption)
    adoptions.insert_one(adoption)
    return redirect(url_for('adoptions_index'))

@app.route()
def

if __name__ == '__main__':
    app.run(debug=True)