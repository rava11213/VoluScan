from flask import Flask, request, jsonify
from flask_cors import CORS
import trimesh
import numpy as np
import os

app = Flask(__name__)
CORS(app)  

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        mesh = trimesh.load_mesh(filepath)
        volume = mesh.volume
        return jsonify({"volume": volume})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
