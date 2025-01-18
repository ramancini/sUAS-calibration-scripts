from src.thermal_cal.calibration import Calibrator
from src.thermal_cal.image_reader import ImageReader
from src.thermal_cal.cal_utils import CalUtils


# Test File for the calibration class

calibrator = Calibrator()

temp = 22  # In Celsius
rsr_path = "data/cam_sheets/flir_rsr copy.csv"
temp_chamber = 22  # In Celsius
single_image_path = "/local/data/imgs589/data/MX1/raw/100027_TAM_22_10_2023_09_10_23_33_17/tam640/raw_2000.hdr"


sensor_radiance = calibrator.calibrate_radiance(temp, temp_chamber, rsr_path)

print(f"Spectral Radiance on Sensor: {sensor_radiance} W/m^2/sr")

gain = calibrator.gain_calc(sensor_radiance, 193)

print(f"Gain: {gain}")

util = CalUtils()

Tam = ImageReader()

img = Tam.read(single_image_path)

norm_img = util.quantization(img)

image_gain = calibrator.image_gain(norm_img, sensor_radiance)

bias_img = calibrator.image_offset(norm_img, image_gain, sensor_radiance)

print(image_gain)

print(bias_img)
