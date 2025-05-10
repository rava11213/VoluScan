from flask import Flask, request, jsonify
from flask_cors import CORS
import trimesh
import numpy as np
import os
import uuid
import traceback

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'obj', 'stl'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return "Welcome to the Flask file upload API!"

@app.route('/upload', methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only .obj and .stl are allowed"}), 400

    # Create unique filename to avoid conflicts
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        mesh = trimesh.load_mesh(filepath, process=True)
        volume = mesh.volume
        bbox = mesh.bounding_box.extents.tolist()

        return jsonify({
            "volume": volume,
            "vertices": len(mesh.vertices),
            "faces": len(mesh.faces),
            "bounding_box": bbox
        })
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content for favicon

if __name__ == "__main__":
    app.run(debug=True, port=5000)
