from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Set the folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Allowed file types (STL, OBJ, PLY formats)
app.config['ALLOWED_EXTENSIONS'] = {'stl', 'obj', 'ply'}

# Function to check if the uploaded file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to simulate volume calculation (replace with actual logic)
def calculate_volume(file_path):
    # In real scenarios, you would use libraries like numpy-stl to load the file and calculate the volume
    return 123.45  # Simulated volume value

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # Check if no file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Check if the file type is allowed
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)  # Save the uploaded file to the server
        
        # Call the function to calculate the volume of the file
        volume = calculate_volume(filename)
        
        # Return the calculated volume as a JSON response
        return jsonify({'volume': volume})
    
    # If the file type is not allowed
    return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    app.run(debug=True)
