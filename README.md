#  VoluScan

**VoluScan** is an open-source web-based API designed to calculate the **volume of scanned 3D mesh objects**, such as masks or medical devices.

This project:

* Allows users to upload `.stl`, `.obj`, or `.ply` mesh files
* Calculates the 3D volume via a Python backend
* Visualizes the object in real-time using **WebGPU** and **Three.js**


##  Tech Stack

* **Backend**: Python (Flask)
* **Frontend**: JavaScript (Vite + Three.js + WebGPU)
* **File Parsing**: STL / OBJ / PLY
* **UI**: HTML5 + CSS


##  Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rava11213/VoluScan.git
cd VoluScan
```


### 2. Backend Setup (Flask)

#### (Optional) Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Run the backend server

```bash
python app.py
```

The backend will start at: [http://localhost:5000](http://localhost:5000)

---

### 3. Frontend Setup (Vite + Three.js + WebGPU)

```bash
cd ../frontend
npm install
npm run dev
```

The frontend will be available at: [http://localhost:5173](http://localhost:5173)


##  Features

* Upload and process 3D mesh files
* Calculate the volume of the object
* View the 3D mesh interactively in-browser
* Real-time rendering using WebGPU and Three.js


##  Future Plans

* [ ] Improve volume accuracy with better mesh geometry handling
* [ ] Enable batch uploads and volume history
* [ ] UI enhancements (drag-and-drop, upload progress)
* [ ] Unit conversion (mm³, cm³, in³)
* [ ] Deploy to cloud platforms (e.g., Render, Vercel)



##  Contributing

PRs are welcome! For major changes, please [open an issue](https://github.com/rava11213/VoluScan/issues) first to discuss what you'd like to change.




