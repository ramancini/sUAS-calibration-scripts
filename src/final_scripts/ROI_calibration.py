import os
import re
import csv
import numpy as np
import matplotlib.pyplot as plt
import tifffile

def search(directory: str) -> list:
    """
    Search for .csv files in the specified directory and return them in numerical order.

    Args:
        directory (str): The directory to search in

    Returns:
        list: List of .hdr files in numerical order
    """
    # List all files in the specified directory
    all_files = os.listdir(directory)

    # Filter out files that do not end with csv
    hdr_files = [file for file in all_files if file.endswith(".csv")]

    # Sort the csv files based on the numerical part of their filenames
    hdr_files.sort(key=lambda x: int(re.search(r"\d+", x).group()))

    full_paths = [os.path.join(directory, file) for file in hdr_files]

    # print(hdr_files)
    return full_paths

def read_csv(file_path) -> np.ndarray:
    """
    Read the data from a CSV file and apply the calibration coefficients.
    Args:
        file_path (str): The path to the CSV file
    Returns:
        np.ndarray: The data as a NumPy array
    """
    data = []

    #cal_cube = np.load("results/cal_coeff_4_1_E97_FLATRSR.npy") # HARDCODED PATH CHANGE THIS

    cal_cube = tifffile.imread('data/cam_sheets/gain_bias_chamber_23.9C.tiff')

    # Open the CSV file
    with open(file_path, mode='r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file, delimiter=',')
        
        # Skip the header lines (lines starting with ';')
        for row in csv_reader:
            if not row or row[0].startswith(';'):
                continue
            
            # Extract x, y, and B1 values
            x = int(row[0].strip())
            y = int(row[1].strip())
            b1 = int(row[2].strip())

            # Apply the calibration coefficients
            slope = cal_cube[y, x, 0]
            intercept = cal_cube[y, x, 1]
            b1 = b1 / 255
            b1 = b1 * slope + intercept

            # Append the data as a list [x, y, B1]
            data.append([b1])
    
    # Convert the list to a NumPy array
    return np.array(data)


# Program starts

mean_values = []
std_values = []
min_values = []
max_values = []

full_paths = search("data/cam_sheets/asphalt")

for file in full_paths:
    data = read_csv(file)
    print(f"File: {file}")

    mean = np.mean(data)
    mean_values.append(mean)

    std = np.std(data)
    std_values.append(std)

    min = np.min(data)
    min_values.append(min)

    max = np.max(data)
    max_values.append(max)

    print(f"Mean: {mean}, Std: {std}, Min: {min}, Max: {max}\n")

# Write the results to a CSV file
output_file = "results/new_cal_RIT_Targets/asphalt.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["File", "Mean_Radiance", "Std", "Min", "Max"])
    for i, file in enumerate(full_paths):
        writer.writerow([file, mean_values[i], std_values[i], min_values[i], max_values[i]])

print(f"Results written to {output_file}")