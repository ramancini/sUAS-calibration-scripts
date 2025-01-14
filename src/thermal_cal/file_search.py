import os
import re


class FileSearch:
    def __init__(self):
        pass

    def search(self, directory: str) -> list:
        """
        Search for .hdr files in the specified directory and return them in numerical order.

        Args:
            directory (str): The directory to search in

        Returns:
            list: List of .hdr files in numerical order
        """
        # List all files in the specified directory
        all_files = os.listdir(directory)

        # Filter out files that do not end with .hdr
        hdr_files = [file for file in all_files if file.endswith(".hdr")]

        # Sort the .hdr files based on the numerical part of their filenames
        hdr_files.sort(key=lambda x: int(re.search(r"\d+", x).group()))

        full_paths = [os.path.join(directory, file) for file in hdr_files]

        # print(hdr_files)
        return full_paths
