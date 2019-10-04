# test.py

from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_playlist_id = ObjectId('')
sample_playlist = {
    'name': 'Mr. Chew',
    'breed': 'poodle'
    'description': 'He is a cute dog, but is a handful.',
    'price': '150',
    'img_url': [

    ]
}

sample_form_data = {
    'name': sample_adoption['name'],
    'breed': sample_adoption['breed'],
    'description': sample_adoption['description'],
    'price': sample_adoption['price'],
    'img_url': sample_adoption['img_url']
}

class PlaylistsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""
        
        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
    
    def test_index(self):
        """Test the adoptions homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Adoption', result.data)
    
    def test_new(self):
        """Test the new adoption creation page."""
        result = self.client.get('/adoptions/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Adoption Ad', result.data)

@mock.patch('pymongo.collection.Collection.find_one')
def test_show_adoption(self, mock_find):
    """Test showing a single adoption ad."""
    mock_find.return_value = sample_playlist

    result = self.client.get(f'/adoptions/{sample_adoption_id}')
    self.assertEqual(result.status, '200 OK')
    self.assertIn(b'Mr. Chew', result.data)

if __name__ == '__main__':
    unittest_main()
