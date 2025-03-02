from celery import Celery
from processor import HighDimImageProcessor
import os
from config import UPLOAD_FOLDER

celery = Celery("tasks", broker="redis://localhost:6379/0")

@celery.task
def process_pca(filename, n_components):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    processor = HighDimImageProcessor(file_path)
    pca_result = processor.apply_pca(n_components)

    return {"message": "PCA analysis completed", "result_shape": pca_result.shape}
