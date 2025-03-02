from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from processor import HighDimImageProcessor
from database import db, ImageMetadata
from tasks import process_pca
import tifffile as tiff
from config import UPLOAD_FOLDER

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
db.init_app(app)

@app.route("/upload", methods=["POST"])
def upload_image():
    #Upload a 5D TIFF image#
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Store metadata in the database
    processor = HighDimImageProcessor(file_path)
    metadata = ImageMetadata(filename=filename, dimensions=str(processor.image.shape))
    db.session.add(metadata)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully", "file": filename})

@app.route("/metadata", methods=["GET"])
def get_metadata():
    #Retrieve image metadata#
    images = ImageMetadata.query.all()
    return jsonify([{"id": img.id, "filename": img.filename, "dimensions": img.dimensions} for img in images])

@app.route("/slice", methods=["GET"])
def get_slice():
    #Extract a specific slice#
    filename = request.args.get("filename")
    z = request.args.get("z", type=int)
    time = request.args.get("time", type=int)
    channel = request.args.get("channel", type=int)

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    processor = HighDimImageProcessor(file_path)
    slice_image = processor.extract_slice(z, time, channel)

    slice_path = f"{UPLOAD_FOLDER}/slice_{filename}.tif"
    tiff.imwrite(slice_path, slice_image)

    return send_file(slice_path, as_attachment=True)

@app.route("/analyze", methods=["POST"])
def analyze_image():
    #Run PCA and return reduced data (asynchronous)#
    filename = request.json.get("filename")
    n_components = request.json.get("n_components", 3)

    result = process_pca.apply_async(args=[filename, n_components])
    return jsonify({"task_id": result.id, "status": "Processing started"})

@app.route("/statistics", methods=["GET"])
def get_statistics():
    #Return image statistics#
    filename = request.args.get("filename")
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    processor = HighDimImageProcessor(file_path)
    stats = processor.compute_statistics()

    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)
