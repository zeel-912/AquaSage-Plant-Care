from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import db, credentials
import requests

app = Flask(__name__)

# Initialize Firebase app
cred = credentials.Certificate("/Users/zeelpatel/Desktop/Final_year_project/flask_app/src/JSON/dht11-c18dd-firebase-adminsdk-gvq2q-3d5bffde0e.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://dht11-c18dd-default-rtdb.firebaseio.com'})

# Global variable for plant health
plant_health = "Unknown"
def fetch_sensor_data():
    try:
        ref = db.reference('/')  # Update the reference path
        data = ref.get()
        return data
    except Exception as e:
        print("Error fetching sensor data:", e)
        return None

# Route to fetch sensor data
@app.route('/get_sensor_data')
def get_sensor_data():
    data = fetch_sensor_data()
    return jsonify(data)

# Function to call the Google Cloud Function for image processing
def process_image(image_file):
    # Replace 'cloud_function_url' with your actual Cloud Function URL
    cloud_function_url = "https://us-central1-tomato-disease-123.cloudfunctions.net/predict"
    files = {'file': image_file}
    response = requests.post(cloud_function_url, files=files)
    return response.json()

# Function to calculate plant health
def calculate_plant_health(data, image_uploaded):
    if data:
        temperature = data.get('temperature', 0)
        humidity = data.get('humidity', 0)
        
        
        if image_uploaded:
            # Call Cloud Function for disease detection
            result = process_image(upload_image)
            
            return f"Disease: {result['class']}"
        
        # Calculate plant health based on other factors (e.g., humidity)
        
        return "Unknown"
    



@app.route('/')
def index():
    data = fetch_sensor_data()
    image_uploaded = False  # Update this based on whether an image is uploaded
    
    global plant_health
    plant_health = calculate_plant_health(data, image_uploaded)
    
    return render_template('index.html', title='AquaSage Plant Care Solution', data=data, plant_health=plant_health)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Get the uploaded image file
    uploaded_image = request.files['image']
    # Process the uploaded image using the Cloud Function
    result = process_image(uploaded_image)
    
    # Update plant_health variable if disease is detected
    
    global plant_health
    plant_health = f"Disease: {result['class']}"
    
    return jsonify({"plant_health": plant_health})
