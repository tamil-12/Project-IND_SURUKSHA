from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'patient_data.json'

def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as file:
            json.dump({}, file)
        print(f"Initialized empty data file: {DATA_FILE}")
    else:
        print(f"Data file {DATA_FILE} already exists.")

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file) if os.path.getsize(DATA_FILE) > 0 else {}
            print(f"Loaded data: {data}")
            return data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading data: {e}")
        return {}

def save_data(data):
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
            print(f"Data saved: {data}")
    except IOError as e:
        print(f"Error saving data: {e}")

@app.route('/patient_details', methods=['POST'])
def receive_patient_details():
    data = request.json
    print(f"Received patient details: {data}")

    patients_data = load_data()
    patient_id = data.get('patient_id')
    if not patient_id:
        return jsonify({"status": "failure", "message": "Invalid or missing patient ID"}), 400

    # Check if the patient_id exists in the data
    if patient_id in patients_data:
        # Update the existing patient details
        patient_details = patients_data[patient_id]['patient_details']
        patient_details.update(data)
    else:
        # Add new patient details
        patients_data[patient_id] = {"patient_details": data}

    save_data(patients_data)
    return jsonify({"status": "success"}), 200

@app.route('/medication_reminder', methods=['POST'])
def receive_medication_reminder():
    data = request.json
    print(f"Received medication reminder: {data}")

    patient_id = data.get('patient_id')
    medication_name = data.get('medication_name')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    times = data.get('times')

    if not all([patient_id, medication_name, start_date, end_date, times]):
        return jsonify({"status": "failure", "message": "Invalid data"}), 400

    patients_data = load_data()
    patient_details = patients_data.get(patient_id, {}).get('patient_details', {})
    if not patient_details:
        return jsonify({"status": "failure", "message": "Patient ID not found"}), 404

    medication_list = patient_details.setdefault('medication_list', [])
    
    # Check if medication already exists and update it
    medication_exists = False
    for med in medication_list:
        if med['name'] == medication_name:
            med.update({
                "start_date": start_date,
                "end_date": end_date,
                "times": times
            })
            medication_exists = True
            break

    if not medication_exists:
        medication_entry = {
            "name": medication_name,
            "start_date": start_date,
            "end_date": end_date,
            "times": times
        }
        medication_list.append(medication_entry)

    save_data(patients_data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    initialize_data_file()
    app.run(debug=True)
