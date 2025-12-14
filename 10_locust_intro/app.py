# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# A simple in-memory counter
hit_counter = 0

@app.route('/')
def home():
    """Serves the homepage with the hit counter."""
    global hit_counter
    return render_template('index.html', counter=hit_counter)

@app.route('/hit', methods=['POST'])
def hit():
    """Increments the hit counter and returns the new value."""
    global hit_counter
    hit_counter += 1
    return jsonify({'hits': hit_counter}), 200

@app.route('/reset', methods=['POST'])
def reset():
    """Resets the hit counter."""
    global hit_counter
    hit_counter = 0
    return jsonify({'hits': hit_counter}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003, threaded=True)
