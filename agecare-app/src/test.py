from flask import Flask, request, jsonify, render_template_string
import requests
import json
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Replace these with your Zoom API credentials
CLIENT_ID = 'EvNY6dvWTsaZZ8Y7YS_d3Q'
CLIENT_SECRET = 'aQlvogJt16hDEGYIBGeFj2BHUgZ3N97Y'
ACCOUNT_ID = 'jwoIw2hMSUesTNAd_BA6Bw'

# Global variable to store the access token
ACCESS_TOKEN = None

# HTML template for getting the OAuth token and creating meetings
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zoom OAuth & Meeting</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        .container {
            margin-top: 20px;
        }
        .card {
            margin-top: 20px;
        }
        .form-group label {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mb-4">Zoom OAuth & Meeting Integration</h1>

        <!-- Section to get OAuth token -->
        <div class="card">
            <div class="card-body">
                <h2>Get Zoom OAuth Token</h2>
                <button id="getTokenButton" class="btn btn-primary">Get OAuth Token</button>
                <div id="tokenDisplay" class="mt-3"></div>
            </div>
        </div>

        <!-- Section to create a Zoom meeting -->
        <div class="card">
            <div class="card-body">
                <h2>Create Zoom Meeting</h2>
                <form id="meetingForm">
                    <div class="form-group">
                        <label for="topic">Topic:</label>
                        <input type="text" id="topic" name="topic" class="form-control" required>
                    </div>

                    <div class="form-group">
                        <label for="start_time">Start Time (ISO format):</label>
                        <input type="text" id="start_time" name="start_time" class="form-control" required>
                    </div>

                    <div class="form-group">
                        <label for="duration">Duration (minutes):</label>
                        <input type="number" id="duration" name="duration" class="form-control" required>
                    </div>

                    <div class="form-group">
                        <label for="timezone">Timezone:</label>
                        <input type="text" id="timezone" name="timezone" class="form-control" required>
                    </div>

                    <div class="form-group">
                        <label for="agenda">Agenda:</label>
                        <textarea id="agenda" name="agenda" class="form-control" rows="3" required></textarea>
                    </div>

                    <button type="submit" class="btn btn-primary">Create Meeting</button>
                </form>
            </div>
        </div>

        <div id="meetingInfo" class="card">
            <div class="card-body">
                <!-- Meeting information will be injected here -->
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script>
        document.getElementById('getTokenButton').addEventListener('click', function() {
            axios.post('/api/get-token')
                .then(response => {
                    const data = response.data;
                    if (data.access_token) {
                        document.getElementById('tokenDisplay').innerHTML = `
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Access Token</h5>
                                    <p class="card-text"><strong>Token:</strong> ${data.access_token}</p>
                                </div>
                            </div>
                        `;
                    } else {
                        document.getElementById('tokenDisplay').innerHTML = '<p>Error fetching token. Check console for details.</p>';
                    }
                })
                .catch(error => {
                    console.error('Error fetching token:', error);
                    document.getElementById('tokenDisplay').innerHTML = '<p>Error fetching token. Check console for details.</p>';
                });
        });

        document.getElementById('meetingForm').addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(this);
            const meetingData = {
                topic: formData.get('topic'),
                type: 2,  // Scheduled meeting
                start_time: formData.get('start_time'),
                duration: parseInt(formData.get('duration')),
                timezone: formData.get('timezone'),
                agenda: formData.get('agenda'),
                settings: {
                    host_video: true,
                    participant_video: true,
                    join_before_host: true,
                    mute_upon_entry: false,
                    watermark: false,
                    auto_recording: "none"
                }
            };

            fetch('/api/create-meeting', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(meetingData)
            })
            .then(response => response.json())
            .then(data => {
                const meetingInfo = document.getElementById('meetingInfo').querySelector('.card-body');
                if (data.id) {
                    meetingInfo.innerHTML = `
                        <h5 class="card-title">Meeting Created Successfully</h5>
                        <p><strong>Meeting ID:</strong> ${data.id}</p>
                        <p><strong>Join URL:</strong> <a href="${data.join_url}" target="_blank">${data.join_url}</a></p>
                        <p><strong>Start URL:</strong> <a href="${data.start_url}" target="_blank">${data.start_url}</a></p>
                    `;
                } else {
                    meetingInfo.innerHTML = `<p class="text-danger">Error creating meeting. Check console for details.</p>`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('meetingInfo').querySelector('.card-body').innerHTML = `<p class="text-danger">Error creating meeting. Check console for details.</p>`;
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

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
