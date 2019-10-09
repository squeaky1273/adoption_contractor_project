from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

adoption_ads = db.adoptions
adoption_ads.insert_many = ([
    {"name": "Mr. Chew", "img_url": "toy_poodle.png", "breed": "toy_poodle", "gender": "male", "description": "He is playful, but can get into lots of trouble.", "age": "3 years", "price": "$1000"}, 
    {"name": "Skittles", "img_url": "beagle.png", "breed": "beagle", "gender": "female", "description": "She loves people and is playful.", "age": "4 years", "price": "$500"},
    {"name": "Cleo", "img_url": "goldfish.png", "breed": "goldfish", "gender": "female", "description": "She is healthy and is funny to watch.", "age": "3 year", "price": "$5"},
    {"name": "Potty", "img_url": "parrot.png", "breed": "parrot", "gender": "male", "description": "He may or may not have learned some curse words.", "age": "2 years", "price": "$100"},
    {"name": "Percival", "img_url": "persian.png", "breed": "persian", "gender": "male", "description": "He enjoys sitting on fluffy thrones and being pampered.", "age": "2.5 years", "price": "$1250"},
    {"name": "Jerry", "img_url": "mouse.png", "breed": "mouse", "gender": "male", "description": "He is fun to watch move around.", "age": "10 months", "price": "$7"},
    {"name": "Woofers", "img_url": "chihuahua.png", "breed": "chihuahua", "gender": "male", "description": "He is avery chill dog as you can see on his face.", "age": "3 years", "price": "$150"},
    {"name": "Hunter", "img_url": "bengal.png", "breed": "bengal", "gender": "female", "description": "She is quiet, but warms up to others.", "age": "1.5 years", "price": "$300"},
    {"name": "Chicken Little", "img_url": "chick.png", "breed": "chicken", "gender": "male", "description": "He is a little cutie, but can be vicious.", "age": "1 month", "price": "$3"}
])

app = Flask(__name__)

@app.route('/')
def adoptions_index():
    """Return homepage."""
    return render_template('adoptions_index.html', adoptions=adoption_ads.find())

@app.route('/adoptions/new')
def adoptions_new():
    """Return to the new adoption profile page"""
    return render_template('adoptions_new.html', adoption={}, title='New Adoption Ad')

@app.route('/adoptions', methods=['POST'])
def adoptions_submit():
    """Submit a new adoption profile. Allows the user to input information for the adoption ad."""
    adoption = {
        'name': request.form.get('name'),
        'img_url': request.form.get('img_url'),
        'breed': request.form.get('breed'),
        'gender': request.form.get('gender'),
        'description': request.form.get('description'),
        'age': request.form.get('age'),
        'price': request.form.get('price')
    }
    print(adoption)
    adoption_id = adoption_ads.insert_one(adoption).inserted_id
    return redirect(url_for('adoptions_show', adoption_id=adoption_id))

@app.route('/adoptions/<adoption_id>')
def adoptions_show(adoption_id):
    """Show a single adoption profile"""
    adoption = adoption_ads.find_one({'_id': ObjectId(adoption_id)})
    return render_template('adoptions_show.html', adoption=adoption)

@app.route('/adoptions/<adoption_id>/edit')
def adoptions_edit(adoption_id):
    """Show the edit form for an adoption profile."""
    adoption = adoption_ads.find_one({'_id': ObjectId(adoption_id)})
    return render_template('adoptions_edit.html', adoption=adoption, title='Edit Adoption Ad')

@app.route('/adoptions/<adoption_id>', methods=['POST'])
def adoption_update(adoption_id):
    """Submit an edited an Adoption Profile."""
    updated_adoption = {
        'name': request.form.get('name'),
        'img_url': request.form.get('img_url'),
        'breed': request.form.get('breed'),
        'gender': request.form.get('gender'),
        'decription': request.form.get('description'),
        'age': request.form.get('age'),
        'price': request.form.get('price')
    }
    adoption_ads.update_one(
        {'_id': ObjectId(adoption_id)},
        {'$set': updated_adoption})
    return redirect(url_for('adoptions_show', adoption_id=adoption_id))

@app.route('/adoptions/<adoption_id>/delete', methods=['POST'])
def adoptions_delete(adoption_id):
    """Delete one adoption profile."""
    adoption_ads.delete_one({'_id': ObjectId(adoption_id)})
    return redirect(url_for('adoptions_index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))