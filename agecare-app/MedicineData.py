from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the Vue frontend

class Medication:
    def __init__(self, id, name, dosage):
        self.id = id
        self.name = name
        self.dosage = dosage

        self.taken = False  # Flag to track whether the medication has been taken.

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "dosage": self.dosage,
            "taken": self.taken,
        }

    def mark_as_taken(self):
        self.taken = True

# Temporary in-memory storage for medication reminders
medications = [
    # Medication(id=1, name="Aspirin", dosage="100mg", time="08:00 AM", instructions="Take with food"),
    # Medication(id=2, name="Lisinopril", dosage="10mg", time="12:00 PM", instructions="")
    Medication(id=1, name="Aspirin", dosage="100mg"),
    Medication(id=2, name="Lisinopril", dosage="10mg")
]

@app.route('/api/medications', methods=['GET'])
def get_medications():
    return jsonify([med.to_dict() for med in medications if not med.taken])

@app.route('/api/medications/<int:med_id>/take', methods=['POST'])
def take_medication(med_id):
    med = next((med for med in medications if med.id == med_id), None)
    if med:
        med.mark_as_taken()
        return jsonify({"message": f"Medication {med_id} marked as taken"}), 200
    return jsonify({"message": "Medication not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=8001)
