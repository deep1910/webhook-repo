from flask import Flask

from app.webhook.routes import webhook   # Import the webhook Blueprint from the routes file
from app.extensions import init_app      # Import the function to initialize extensions like MongoDB

# Function to create and configure the Flask application
def create_app():

    app = Flask(__name__, template_folder='templates')  # Initialize the Flask app and set the template folder

    init_app(app)  # Initialize any extensions (e.g., MongoDB, other configurations)
    
    # Register the webhook Blueprint with the app so that routes defined in 'webhook' are active
    app.register_blueprint(webhook)
    
    return app  # Return the configured Flask app instance

