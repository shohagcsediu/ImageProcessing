from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ImageMetadata(db.Model):
    __tablename__ = "image_metadata"
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    dimensions = db.Column(db.String(255), nullable=False)
