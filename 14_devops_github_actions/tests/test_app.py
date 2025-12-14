import unittest
from app import app

class PetShopTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.post('/pets/reset')

    def test_home(self):
        """Test the home page route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_pet(self):
        """Test creating a new pet via POST."""
        new_pet = {
            "name": "Buddy",
            "category": "Dog",
            "age": 3
        }
        response = self.client.post('/pets', json=new_pet)
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], "Buddy")
        self.assertEqual(data['category'], "Dog")

    def test_get_pets_with_data(self):
        """Test getting all pets after adding some."""
        self.client.post('/pets', json={"name": "Buddy", "category": "Dog"})
        self.client.post('/pets', json={"name": "Mittens", "category": "Cat"})

        response = self.client.get('/pets')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Buddy")
        self.assertEqual(data[1]['name'], "Mittens")

    def test_search_pets_by_category(self):
        """Test searching/filtering pets by category."""
        self.client.post('/pets', json={"name": "Buddy", "category": "Dog"})
        self.client.post('/pets', json={"name": "Rex", "category": "Dog"})
        self.client.post('/pets', json={"name": "Mittens", "category": "Cat"})

        # Search for Dog (case insensitive test)
        response = self.client.get('/pets?category=dog')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        for pet in data:
            self.assertEqual(pet['category'], 'Dog')

        # Search for Cat
        response = self.client.get('/pets?category=Cat')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Mittens")

    def test_update_pet_success(self):
        """Test updating an existing pet."""
        self.client.post('/pets', json={"name": "Buddy", "category": "Dog"})
        
        update_data = {"name": "Buddy Jr.", "category": "Dog"}
        response = self.client.put('/pets/1', json=update_data)
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], "Buddy Jr.")
        self.assertEqual(data['id'], 1)

    def test_update_pet_not_found(self):
        """Test updating a pet that does not exist."""
        response = self.client.put('/pets/999', json={"name": "Ghost"})
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.get_json()['message'])

    def test_delete_pet_success(self):
        """Test deleting an existing pet."""
        self.client.post('/pets', json={"name": "Buddy", "category": "Dog"})
        
        response = self.client.delete('/pets/1')
        self.assertEqual(response.status_code, 204)
        
        get_response = self.client.get('/pets')
        self.assertEqual(get_response.get_json(), [])

    def test_delete_pet_not_found(self):
        """Test deleting a pet that does not exist."""
        response = self.client.delete('/pets/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.get_json()['message'])

    def test_reset_pets(self):
        """Test the reset functionality."""
        self.client.post('/pets', json={"name": "Buddy", "category": "Dog"})
        
        response = self.client.post('/pets/reset')
        self.assertEqual(response.status_code, 204)
        
        get_response = self.client.get('/pets')
        self.assertEqual(get_response.get_json(), [])
