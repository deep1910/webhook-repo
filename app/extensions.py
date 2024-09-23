from flask_pymongo import PyMongo

# Initialize PyMongo instance
mongo = PyMongo()

# Function to set up MongoDB and attach it to the Flask app
def init_app(app):
    # Configure the MongoDB URI (the database URL)
    app.config['MONGO_URI'] = "mongodb://localhost:27017/database"
    
    # Initialize PyMongo with the Flask app, connecting the app to the MongoDB instance
    mongo.init_app(app)
