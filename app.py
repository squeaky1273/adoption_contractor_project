from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/my_app_db')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
adoption_ads = db.adoptions

app = Flask(__name__)

@app.route('/')
def adoptions_index():
    """Return homepage."""
    return render_template('adoptions_index.html', adoptions=adoption_ads.find())

@app.route('/adoptions/new')
def adoptions_new():
    """Return to the new adoption ad page"""
    return render_template('adoptions_new.html', adoption={}, title="New Adoption Ad")

@app.route('/adoptions', methods=['POST'])
def adoptions_submit():
    """Submit a new adoption ad. Allows the user to input information for the adoption ad."""
    adoption = {
        'breed of the animal': request.form.get('breed of the animal'),
        'description of the animal': request.form.get('description of the animal'),
        'price': request.form.get('price'),
        'img_url': request.form.get('img_url')
    }
    adoption_id = adoption_ads.insert_one(adoption).inserted_id
    return redirect(url_for('adoptions_show', adoption_id=adoption_id))

@app.route('/adoptions/<adoption_id>')
def adoptions_show(adoption_id):
    """Show a single adoption ad"""
    adoption = adoption_ads.find_one({'_id': ObjectId(adoption_id)})
    return render_template('adoptions_show.html', adoption=adoption)

@app.route('/edit/<adoption_id>', methods=['POST'])
def adoption_update(adoption_id):
    """Edit page for an Adoption Ad."""
    updated_adoption = {
        'name': request.form.get('name'),
        'breed': request.form.get('breed'),
        'decription': request.form.get('description'),
        'price': request.form.get('price'),
        'img_url': request.form.get('img_url')
    }
    adoption_ads.update_one(
        {'_id': ObjectId(adoption_id)},
        {'$set': updated_adoption}
    )
    return redirect(url_for('adoption_show', adoption_id=adoption_id))

@app.route('/adoptions/<adoption_id>/edit')
def adoptions_edit(adoption_id):
    """Show the edit form for an adoption ad."""
    adoption = adoption_ads.find_one({'_id': ObjectId(adoption_id)})
    return render_template('adoptions_edit.html', adoption=adoption)

@app.route('/adoptions/<adoption_id>/delete', methods=['POST'])
def adoptions_delete(adoption_id):
    """Delete one adoption ad."""
    adoption_ads.delete_one({'_id': ObjectId(adoption_id)})
    return redirect(url_for('adoptions_index'))

if __name__ == '__main__':
    app.run(debug=True)