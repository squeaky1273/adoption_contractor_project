from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Adoption')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
adoptions = db.adoptions

app = Flask(__name__)

@app.route('/')
def adoptions_index():
    """Return homepage."""
    return render_template('adoptions_index.html', adoptions=adoptions.find())

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
    print(adoption)
    adoption_id = adoptions.insert_one(adoption).inserted_id
    return redirect(url_for('adoptions_show', adoption_id=adoption_id))

@app.route('/adoptions/<adoption_id>')
def adoptions_show(adoption_id):
    """Show a single adoption ad"""
    adoption = adoptions.find_one({'_id': ObjectId(adoption_id)})
    return render_template('adoptions_show.html', adoption=adoption)

@app.route('/adoptions/<adoption_id>/edit')
def adoptions_edit(playlist_id):
    """Show the edit form for an adoption ad."""
    adoption = adoptions.find_one({'_id': ObjectId(adoption_id)})
    return render_template('adoptions_edit.html', adoption=adoption, title='Edit Adoption AD')

@app.route('/adoptions/<adoption_id>/delete', methods=['POST'])
def adoptions_delete(adoption_id):
    """Delete one adoption ad."""
    adoptions.delete_one({'_id': ObjectId(adoption_id)})
    return redirect(url_for('adoptions_index'))

if __name__ == '__main__':
    app.run(debug=True)