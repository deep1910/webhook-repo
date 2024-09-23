from app import create_app  # Import the function to create the Flask app
from flask import request, jsonify  # Import Flask modules for handling requests and returning JSON responses
from flask import json, render_template  # Import modules for JSON handling and rendering HTML templates
from app.extensions import mongo  # Import the MongoDB instance from the app extensions

# Create a Flask app instance by calling the create_app function
app = create_app()

# Define the route for the root URL ('/')
@app.route('/')
def api_root():
    # Render and return the 'events.html' template
    return render_template('events.html')

# Define a route to get the recent events from the MongoDB database
@app.route('/events')
def get_events():
    # Fetch the latest 5 events from MongoDB, sorted by timestamp in descending order
    events = list(mongo.db.events.find().sort('timestamp', -1).limit(5))
    
    # Convert each event's '_id' field (MongoDB ObjectId) into a string for proper JSON serialization
    for event in events:
        event['_id'] = str(event['_id'])
    
    # Return the list of events as a JSON response
    return jsonify(events)

# Run the app when the script is executed directly
if __name__ == '__main__': 
    # Start the Flask development server with debug mode enabled
    app.run(debug=True)
