import numpy as np
import tifffile as tiff
from skimage.filters import threshold_otsu
from sklearn.decomposition import PCA
from skimage import img_as_ubyte

class HighDimImageProcessor:
    def __init__(self, file_path):
        self.image = self.load_image(file_path)

    def load_image(self, file_path):
        #Load a 5D TIFF image (X, Y, Z, Time, Channel)#
        img = tiff.imread(file_path)
        if img.ndim != 5:
            raise ValueError("The input image must be 5D (X, Y, Z, Time, Channel).")
        return img

    def extract_slice(self, z=None, time=None, channel=None):
        #Extract a specific slice based on Z, Time, and Channel#
        sliced = self.image
        if z is not None:
            sliced = sliced[z, :, :, :, :]
        if time is not None:
            sliced = sliced[:, :, :, time, :]
        if channel is not None:
            sliced = sliced[:, :, :, :, channel]
        return img_as_ubyte(sliced)

    def compute_statistics(self):
        #Compute mean, std, min, max for each band#
        stats = {
            "mean": np.mean(self.image, axis=(0, 1, 2)),
            "std": np.std(self.image, axis=(0, 1, 2)),
            "min": np.min(self.image, axis=(0, 1, 2)),
            "max": np.max(self.image, axis=(0, 1, 2)),
        }
        return stats

    def apply_pca(self, n_components=3):
        #Apply PCA on the high-dimensional image#
        reshaped = self.image.reshape(-1, self.image.shape[-1])  # Flatten spatial dimensions
        pca = PCA(n_components=n_components)
        reduced = pca.fit_transform(reshaped)
        return reduced
