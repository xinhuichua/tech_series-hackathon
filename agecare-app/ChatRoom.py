from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from requests.auth import HTTPBasicAuth
import os

app = Flask(__name__)
CORS(app)

# Replace these with your Zoom API credentials
CLIENT_ID = 'EvNY6dvWTsaZZ8Y7YS_d3Q'
CLIENT_SECRET = 'aQlvogJt16hDEGYIBGeFj2BHUgZ3N97Y'
ACCOUNT_ID = 'jwoIw2hMSUesTNAd_BA6Bw'

# Global variables
SECRET_KEY = os.urandom(24)
ACCESS_TOKEN = None
meetings = []


@app.route('/api/get-token', methods=['POST'])
def get_token():
    """ Obtain the Zoom access token. """
    url = 'https://zoom.us/oauth/token?grant_type=account_credentials&account_id=' + ACCOUNT_ID
    response = requests.post(url, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))

    if response.status_code == 200:
        token_info = response.json()
        global ACCESS_TOKEN
        ACCESS_TOKEN = token_info['access_token']
        return jsonify(token_info)
    else:
        return jsonify({
            'error': 'Failed to obtain access token',
            'status_code': response.status_code,
            'response': response.json()
        }), response.status_code


# @app.route('/api/create-meeting', methods=['POST'])
# def create_meeting():
#     """ Create a new Zoom meeting. """
#     global ACCESS_TOKEN
#     headers = {
#         'Authorization': f'Bearer {ACCESS_TOKEN}',
#         'Content-Type': 'application/json'
#     }
#     response = requests.post('https://api.zoom.us/v2/users/me/meetings',
#                              headers=headers, data=json.dumps(request.json))
#     return jsonify(response.json()), response.status_code
@app.route('/api/create-meeting', methods=['POST'])
def create_meeting():
    data = request.json
    token = request.headers.get('Authorization').split()[1]

    meeting_details = {
        "topic": data['topic'],
        "type": 2,  # Scheduled meeting
        "start_time": data['start_time'],
        "timezone": "UTC"
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.zoom.us/v2/users/me/meetings",
        headers=headers,
        json=meeting_details
    )

    if response.status_code == 201:
        meeting_info = response.json()
        return jsonify({
            "join_url": meeting_info['join_url'],
            "start_url": meeting_info['start_url']  # Include start_url
        })
    else:
        return jsonify({"message": "Failed to create Zoom meeting"}), response.status_code


@app.route('/api/add-meeting', methods=['POST'])
def add_meeting():
    """ Add a meeting link to the list of meetings. """
    link = request.json.get('link')
    if link:
        meetings.append({'link': link})
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'failed', 'error': 'No link provided'}), 400


@app.route('/api/meetings', methods=['GET'])
def list_meetings():
    """ List all meetings. """
    return jsonify(meetings)


if __name__ == '__main__':
    # Consolidate to use one port for simplicity
    app.run(debug=True, port=8000)
