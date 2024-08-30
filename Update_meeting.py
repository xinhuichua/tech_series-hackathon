from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Store meetings in a simple list (in-memory storage for demonstration purposes)
meetings = []

@app.route('/')
def index():
    return render_template('user.html', meetings=meetings)

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/api/add-meeting', methods=['POST'])
def add_meeting():
    data = request.json
    link = data.get('link')
    if link:
        meetings.append({'link': link})
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'failed', 'error': 'No link provided'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8000)
