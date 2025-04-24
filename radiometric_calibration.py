from src.thermal_cal.file_search import FileSearch
from src.thermal_cal.cal_utils import CalUtils
from src.thermal_cal.calibration import Calibrator

import argparse

import numpy as np

local_path = "/local/data/imgs589/data/calibration/raw/tam640/20241114/295/283"
local_rsr_path = "data/cam_sheets/flir_rsr copy.csv"


if __name__ == "__main__":
    txt_description = (
        "The radiometric calibration process, returns the calibration coefficients"
    )
    parser = argparse.ArgumentParser(description=txt_description)
    parser.add_argument(
        "-dir_path",
        type=str,
        help="Path to the directory containing the images",
        default=local_path,
    )
    parser.add_argument(
        "-temp", type=float, help="Temperature of the blackbody in C", default=21.85
    )
    parser.add_argument(
        "-temp_chamber",
        type=float,
        help="Temperature of the chamber in C",
        default=9.85,
    )
    parser.add_argument(
        "-rsr_path", type=str, help="Path to the RSR file", default=local_rsr_path
    )

    args = parser.parse_args()
    dir_path = args.dir_path
    temp = args.temp
    temp_chamber = args.temp_chamber
    rsr_path = args.rsr_path

    search = FileSearch()

    files = search.search(dir_path)

    utils = CalUtils()

    final_img = utils.combine(files)

    final_img = utils.quantization(final_img)

    calibrator = Calibrator()

    sensor_radiance = calibrator.calibrate_radiance(temp, temp_chamber, rsr_path)

    image_gain = calibrator.image_gain(final_img, sensor_radiance)

    bias_img = calibrator.image_offset(final_img, image_gain, sensor_radiance)

    image_gain = np.mean(image_gain, axis=2)

    print(image_gain)

    bias_img = np.mean(bias_img, axis=2)

    np.save("results/calibration_coeff/gain_img.npy", image_gain, allow_pickle=False)
    np.save("results/calibration_coeff/bias_img.npy", bias_img, allow_pickle=False)

    print("Calibration Coeff Saved!")
