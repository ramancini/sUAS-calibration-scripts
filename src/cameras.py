import os
import numpy as np
import spectral.io.envi as envi


class Camera:
    """
    Class for reading Thermal Images from ENVI Files
    """

    def __init__(self, name: str):
        """
        Initialise a Camera object
        Parameters:
        name(str): Name for the camera
        Raises:
        ValueError: If name is not a string
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        self.name = name.strip()

    def validate_file(self, filepath: str) -> bool:
        """

        Validate if a file exists and has a ENVI header file
        Parameters:
            filepath(str): Path to the ENVI file

        Returns:
            bool: True if file exists, False otherwise

        Raises:
            ValueError: If file does not exist

        """
        if not isinstance(filepath, str) or not filepath.strip():
            raise ValueError("Path must be a non-empty string")
        if not os.path.exists(filepath):
            return False
        hdr_file = os.path.splitext(filepath)[0] + ".hdr"
        if not os.path.exists(hdr_file):
            return False
        return True

    def read(self, filepath: str, validate: bool = True) -> np.ndarray:
        """
        Reads the Thermal Images from ENVI Files
        Parameters:
            filepath(str): Path to the ENVI file
            validate(bool): Whether to validate the file
        Returns:
        np.ndarray: Array containing the Thermal Images

        """
        try:
            if validate and not self.validate_file(filepath):
                raise ValueError(f"File {filepath} is not a valid path")

            image = envi.open(filepath)
            data = image.load()
            return data
        except Exception as e:
            raise Exception(f"Error reading {filepath}: {e}")


# end of file
