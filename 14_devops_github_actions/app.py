# app.py
from flask import Flask, jsonify, request, render_template, make_response

# A simple in-memory dictionary to simulate a database for our pets
pets = {}
next_id = 1

app = Flask(__name__)

# Helper function to generate a unique ID
def get_next_id():
    """Generates a unique ID for a new pet."""
    global next_id
    current_id = next_id
    next_id += 1
    return current_id

# Route for the homepage
@app.route('/')
def home():
    """Serves the homepage for the app."""
    return render_template('index.html')

# API endpoint to get all pets or search by category
@app.route('/pets', methods=['GET', 'POST'])
def handle_pets():
    """
    Handles pet creation (POST) and searching (GET).
    
    For a POST request, it adds a new pet to the in-memory list.
    For a GET request, it returns pets that match the search criteria.
    """
    if request.method == 'POST':
        new_pet = request.get_json()
        new_id = get_next_id()
        new_pet['id'] = new_id
        pets[new_id] = new_pet
        response_data = jsonify(new_pet)
        response_data.status_code = 201
        return response_data

    if request.method == 'GET':
        category = request.args.get('category')
        if category:
            matching_pets = [pet for pet in pets.values() if pet['category'] == category]
            return jsonify(matching_pets)
        
        return jsonify(list(pets.values()))

# API endpoint for updating a pet
@app.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    """
    Updates an existing pet.
    """
    if pet_id not in pets:
        return jsonify({"message": f"Pet with ID {pet_id} not found"}), 404
    
    data = request.get_json()
    pet = pets[pet_id]
    pet.update(data)
    pets[pet_id] = pet
    return jsonify(pet), 200

# API endpoint for deleting a pet
@app.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    """
    Deletes a single pet from the dictionary by ID.
    """
    if pet_id not in pets:
        return jsonify({"message": f"Pet with ID {pet_id} not found"}), 404
        
    del pets[pet_id]
    return make_response('', 204)

# Added a route to clear the pets list for testing purposes
@app.route('/pets/reset', methods=['POST'])
def reset_pets():
    """Clears the pets list and resets the ID counter."""
    global pets, next_id
    pets = {}
    next_id = 1
    response = make_response('', 204)
    return response
    
@app.route('/shutdown')
def shutdown(): # pragma: no cover
    """Shuts down the server gracefully for testing purposes."""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()
    return 'Server shutting down...'

if __name__ == '__main__': # pragma: no cover
    app.run(debug=True, host='0.0.0.0', port=5000)
