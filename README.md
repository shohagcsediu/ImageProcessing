# High-Dimensional Image Processor API
This project provides a Flask-based API for processing 5D images (X, Y, Z, Time, Channel). It supports uploading multi-dimensional TIFF images, extracting slices, performing PCA analysis, and retrieving metadata.

## 🚀 Setup Instructions

### 1️⃣ Prerequisites
Ensure you have the following installed:
- Python 3.10+
- Docker & Docker Compose (if using Docker)
- PostgreSQL & Redis (if running without Docker)

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/shohagcsediu/ImageProcessing.git
```

### 3️⃣ Set Up Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Configure the Environment Variables
Create a `.env` file in the project root:
```ini
UPLOAD_FOLDER=uploads/
SQLALCHEMY_DATABASE_URI=postgresql://myuser:mypassword@db:5432/mydatabase
BROKER_URL=redis://redis:6379/0
```

### 6️⃣ Initialize Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7️⃣ Run the API Server
#### Without Docker:
```bash
python app.py
```
#### With Docker:
```bash
docker-compose up --build
```

---

## 📌 API Endpoints & Usage

### 1️⃣ Upload an Image
**Endpoint:** `POST /upload`
```bash
curl -X POST -F "file=@image.tif" http://localhost:5000/upload
```

### 2️⃣ Get Image Metadata
**Endpoint:** `GET /metadata?filename=image.tif`
```bash
curl -X GET http://localhost:5000/metadata?filename=image.tif
```

### 3️⃣ Extract an Image Slice
**Endpoint:** `GET /slice?filename=image.tif&z=5&time=3&channel=2`
```bash
curl -X GET "http://localhost:5000/slice?filename=image.tif&z=5&time=3&channel=2" -o slice.tif
```

### 4️⃣ Run PCA Analysis
**Endpoint:** `POST /analyze`
```bash
curl -X POST http://localhost:5000/analyze -H "Content-Type: application/json" -d '{"filename": "image.tif"}'
```

### 5️⃣ Get Image Statistics
**Endpoint:** `GET /statistics?filename=image.tif`
```bash
curl -X GET http://localhost:5000/statistics?filename=image.tif
```

---

## 🎯 Additional Notes
- Ensure the PostgreSQL and Redis services are running.
- Use Postman or cURL for API testing.
- For large images, Celery and Redis handle async processing.
