# Standard modules
import argparse
import fnmatch
import glob
import os
import os.path
import shutil

# Third-party modules
from matplotlib import pyplot as plt
import numpy as np
import spectral

# Map ENVI data type codes to NumPy dtypes
envi_dtype_mapping = {
    1: "uint8",
    2: "int16",
    3: "int32",
    4: "float32",
    5: "float64",
    6: "complex64",
    9: "complex128",
    12: "uint16",
    13: "uint32",
    14: "int64",
    15: "uint64",
}


def clear_directory(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)


def find_packed_files(path):
    packed_files = [
        os.path.join(path, file)
        for file in sorted(os.listdir(path))
        if fnmatch.fnmatch(file, "raw_*") and not file.endswith(".hdr")
    ]
    return packed_files


if __name__ == "__main__":
    # Set default flag/option values
    verbose = False
    delete_png = False

    # Command line parsing
    description = "Unpack Headwall Hypercore packed image data (only)"
    parser = argparse.ArgumentParser(description=description)
    help_message = "source directory containing the packed image data files"
    parser.add_argument("source_directory", help=help_message)
    help_message = "verbose [default is False]"
    parser.add_argument("-v", "--verbose", action="store_true", help=help_message)
    help_message = "Remove any vendor-created PNG files in the source directory "
    help_message += "[default is False]"
    parser.add_argument("-d", "--delete-png", action="store_true", help=help_message)
    help_message = 'Output file format [default is "tif"]'
    parser.add_argument(
        "-o",
        "--output-format",
        dest="output_format",
        type=str,
        default="tif",
        help=help_message,
    )

    args = parser.parse_args()
    source_directory = args.source_directory.rstrip(os.path.sep)
    verbose = args.verbose
    delete_png = args.delete_png
    output_format = args.output_format

    output_extension = "." + output_format

    if os.path.isdir(source_directory):
        # Delete vendor-created PNG files in source directory if requested
        if delete_png:
            file_pattern = (
                source_directory.rstrip(os.path.sep) + os.path.sep + "raw_*.png"
            )
            for file_path in glob.glob(file_pattern):
                if os.path.isfile(file_path):
                    os.remove(file_path)

        # Create a list of all packed files in the provided source directory
        packed_files = find_packed_files(source_directory)

        # Initalize the frame number for sequential frame numbering across all
        # packed files found
        frame_number = 0

        pixel_list = np.array([])

        # Extract frames from each packed file present
        for idx, packed_file in enumerate(packed_files):
            if verbose:
                msg = "\nWORKING ON PACKED IMAGE {0} ...".format(packed_file)
                print(msg)

            if os.path.isfile(packed_file):
                # Create the current packed (ENVI) image object
                packed_object = spectral.envi.open(packed_file + ".hdr", packed_file)

                # Display the header data for the current packed (ENVI) image object
                if verbose:
                    msg = "\nHEADER DATA ..."
                    print(msg)
                    print(packed_object)
                    msg = ""
                    print(msg)

                # Load data from current packed (ENVI) image file
                data = packed_object.load()

                pixel_list = np.append(
                    pixel_list, data[240, 320, :].flatten() / 256, axis=0
                )
                print(pixel_list.shape)

                if verbose:
                    adj_idx = idx * 2000
                    print(f"Current index {adj_idx}")

        frame_period = 0.0332  # [s]
        times = np.arange(0, pixel_list.shape[0]) * frame_period / 60

        plt.plot(times, pixel_list)
        plt.ylim(0, 255)
        plt.show()
