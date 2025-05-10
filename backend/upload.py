from flask import Flask, request, jsonify
import os
import uuid
import trimesh
import traceback
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Optional: allow requests from frontend (Vue)

# Set the folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file types (STL, OBJ, PLY formats)
ALLOWED_EXTENSIONS = {'stl', 'obj', 'ply'}

# Check for allowed file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check for file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Check for empty filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # Save the file with a unique name to avoid conflict
        unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        try:
            # Load mesh and calculate volume
            mesh = trimesh.load_mesh(filepath, process=True)
            volume = mesh.volume
            return jsonify({
                'volume': volume,
                'vertices': len(mesh.vertices),
                'faces': len(mesh.faces),
                'filename': file.filename
            })
        except Exception as e:
            return jsonify({
                'error': str(e),
                'trace': traceback.format_exc()
            }), 500

    return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
