from src.thermal_cal.calibration import Calibrator
from src.thermal_cal.image_reader import ImageReader
from src.thermal_cal.file_search import FileSearch
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress
from multiprocessing import Pool
from scipy.stats import linregress

file_finder = FileSearch()
img_reader = ImageReader()


# HARD CODED PATHS
# CHANGE THIS TO YOUR PATHS
path = "/local/data/imgs589/data/calibration/raw/tam640/20250207/293.15/278.15-313.15_increment-5"
img_path = "/local/data/imgs589/data/calibration/raw/tam640/20250207/293.15/278.15-313.15_increment-5/raw_0.hdr"
cal_cube_path = "results/cal_coeff_4_4_E97_Flat_NORMRSR.npy" # Path to save the calibration cube
file_list = file_finder.search(path)

img = img_reader.read(img_path)
rows, cols = img.shape[0], img.shape[1]
cal_cube = np.empty((rows, cols, 2))

# HARD CODED IMAGES AND CORRESPONDING RADIANCE VALUES
# CHANGE THIS TO YOUR VALUES
index_list = [11,21,33,45,57,68,78,92]
radiance_vals = [
6.23,
6.822,
7.44,
8.1,
8.792,
9.518,
10.2806,
11.07
]

# Read the selected images and store them in a list
images = [img_reader.read(file_list[index]) for index in index_list]

# Compute the mean of each image along the color channels and stack them into a single array
mean_stack = np.array([np.mean(img, axis=2) for img in images]) 

def process_pixel(args):
    """Process a single pixel of the calibration cube.
    
    Args:
        args (tuple): A tuple containing the pixel coordinates (i, j).
    
    Returns:
        tuple: A tuple containing the pixel coordinates (i, j), slope, and intercept.
    """
    i, j = args
    DC_array = mean_stack[:, i, j]  # Use precomputed means
    result = linregress(DC_array, radiance_vals)
    return i, j, result.slope, result.intercept

# Create a list of all pixel coordinates
pixel_coords = [(i, j) for i in range(rows) for j in range(cols)]

# Use multiprocessing to process pixels
with Pool() as pool:
    results = pool.map(process_pixel, pixel_coords)

# Populate the calibration cube with results
cal_cube = np.empty((rows, cols, 2))
for i, j, slope, intercept in results:
    cal_cube[i, j, 0] = slope
    cal_cube[i, j, 1] = intercept

np.save(cal_cube_path, cal_cube)