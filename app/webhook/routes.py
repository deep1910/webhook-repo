from flask import Blueprint, json, request, jsonify
from datetime import datetime
from app.extensions import mongo


# Create a Blueprint for the webhook routes, with the prefix '/webhook'
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# Route to handle POST requests for receiving GitHub webhook events
@webhook.route('/receiver', methods=["POST"])
def receiver():

    # Parse the incoming JSON data from the GitHub webhook request
    data = request.json
    
    # Check if the event is a 'push' event
    if 'pusher' in data:
        print('pusher')
        
        # Parse the timestamp from the 'head_commit' field and format it
        dt = datetime.fromisoformat(data['head_commit']['timestamp'])
        format_dt = dt.strftime("%d %B %Y - %I:%M %p UTC")
        
        # Determine the correct suffix for the day (st, nd, rd, th)
        day_suffix = "th" if 4 <= dt.day <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(dt.day % 10, "th")
        formatted_date = format_dt.replace(f"{dt.day}", f"{dt.day}{day_suffix}")

        # Create a dictionary to represent the event details
        event = {
            'request_id': data['head_commit']['id'],  # Use commit ID as request_id
            'author': data['pusher']['name'],          # Name of the person who pushed
            'action': 'Push',                          # Set the action as 'Push'
            'from_branch': data['ref'].split('/')[-1], # Extract the branch name from 'ref'
            'to_branch': data['ref'].split('/')[-1],   # Same branch for 'from' and 'to' in a push
            'timestamp': formatted_date                # Formatted timestamp
        }

    # Check if the event is an 'opened' pull request event
    elif 'action' in data and data['action'] == 'opened':
        print(data['action'])

        # Get the current time and format it
        dt = datetime.now()
        format_dt = dt.strftime("%d %B %Y - %I:%M %p UTC")
        
        # Add the correct suffix to the day
        day_suffix = "th" if 4 <= dt.day <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(dt.day % 10, "th")
        formatted_date = format_dt.replace(f"{dt.day}", f"{dt.day}{day_suffix}")

        # Create a dictionary to represent the pull request event details
        event = {
            'request_id': str(data['pull_request']['id']),    # Use pull request ID as request_id
            'author': data['pull_request']['user']['login'],  # Author of the pull request
            'action': 'Pull Request',                        # Set the action as 'Pull Request'
            'from_branch': data['pull_request']['head']['ref'], # Source branch of the pull request
            'to_branch': data['pull_request']['base']['ref'],  # Target branch of the pull request
            'timestamp': formatted_date                       # Formatted timestamp
        }

    # Check if the event is a 'merged' pull request event
    elif 'action' in data and data['action'] == 'closed' and data['pull_request']['merged']:
        print(data['action'])

        # Get the current time and format it
        dt = datetime.now()
        format_dt = dt.strftime("%d %B %Y - %I:%M %p UTC")
        
        # Add the correct suffix to the day
        day_suffix = "th" if 4 <= dt.day <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(dt.day % 10, "th")
        formatted_date = format_dt.replace(f"{dt.day}", f"{dt.day}{day_suffix}")
    
        # Create a dictionary to represent the merge event details
        event = {
            'request_id': data['pull_request']['id'],       # Use pull request ID as request_id
            'author': data['pull_request']['user']['login'],# Author of the pull request
            'action': 'Merge',                             # Set the action as 'Merge'
            'from_branch': data['pull_request']['head']['ref'], # Source branch being merged
            'to_branch': data['pull_request']['base']['ref'],  # Target branch after the merge
            'timestamp': formatted_date                       # Formatted timestamp
        }

    # If the event type is unhandled, return an error response
    else:
        return jsonify({'message': 'Unhandled event type'}), 400

    # Insert the event into the MongoDB 'events' collection
    mongo.db.events.insert_one(event)

    # Return a success message indicating the event was received
    return jsonify({'message': 'Event received'}), 200

