from flask import Flask, request, jsonify, render_template_string
import requests
import json
from requests.auth import HTTPBasicAuth
from flask_cors import CORS
import os
secret_key = os.urandom(24)
app = Flask(__name__)
CORS(app)
# Replace these with your Zoom API credentials
CLIENT_ID = 'EvNY6dvWTsaZZ8Y7YS_d3Q'
CLIENT_SECRET = 'aQlvogJt16hDEGYIBGeFj2BHUgZ3N97Y'
ACCOUNT_ID = 'jwoIw2hMSUesTNAd_BA6Bw'

# Global variable to store the access token
ACCESS_TOKEN = None

# HTML template for getting the OAuth token and creating meetings

# @app.route('/')
# def index():
#     return render_template_string(HTML_TEMPLATE)

@app.route('/api/get-token', methods=['POST'])
def get_token():
    global ACCESS_TOKEN
    url = 'https://zoom.us/oauth/token?grant_type=account_credentials&account_id=' + ACCOUNT_ID

    # Request the access token
    response = requests.post(url, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))

    if response.status_code == 200:
        token_info = response.json()
        ACCESS_TOKEN = token_info['access_token']
        return jsonify(token_info)
    else:
        return jsonify({
            'error': 'Failed to obtain access token',
            'status_code': response.status_code,
            'response': response.json()
        }), response.status_code

@app.route('/api/create-meeting', methods=['POST'])
def create_meeting():
    global ACCESS_TOKEN
    meeting_data = request.json
    url = 'https://api.zoom.us/v2/users/me/meetings'

    # Set up headers
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    # Make the API request
    response = requests.post(url, headers=headers, data=json.dumps(meeting_data))

    # Return the response
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=8001)
