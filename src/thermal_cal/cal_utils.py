import numpy as np
from src.thermal_cal.image_reader import ImageReader


class CalUtils:
    def __init__(self):
        pass

    def combine(self, file_list) -> np.ndarray:
        """
        Combine images from a list of file paths into a single numpy array.

        Args:
            file_list (list): List of file paths to .hdr images

        Returns:
            np.ndarray: Combined image array
        """

        # Initialize an empty list to store images
        images = []

        # Create an instance of ImageReader
        reader = ImageReader()

        # Read each image and append to the list
        for path in file_list:
            img = reader.read(path)
            images.append(img)

        # Stack images along the third axis
        comb_img = np.concatenate(images, axis=2)

        return comb_img
    
    def bad_pixel_map(self, image) -> np.ndarray:
        """
        Create a bad pixel map from an image.

        Args:
            image (np.ndarray): Image array

        Returns:
            np.ndarray: Bad pixel map
        """

        # Calculate the standard deviation of the image
        std_dev = np.std(image, axis=2)


        # Threshold the standard deviation to create a bad pixel map
        bad_pixel_map = std_dev > 640

        bad_pixel_map = bad_pixel_map.astype(int)

        return bad_pixel_map
