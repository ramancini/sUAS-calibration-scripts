from src.thermal_cal.calibration import Calibrator
from src.thermal_cal.image_reader import ImageReader
from src.thermal_cal.cal_utils import CalUtils

calibrator = Calibrator()

temp = 26.85  # In Celsius
wavelength = 8  # In micrometers
rsr_path = "data/cam_sheets/flir_rsr copy.csv"
temp_chamber = 5  # In Celsius

sensor_radiance = calibrator.calibrate_radiance(
    temp, temp_chamber, rsr_path, wavelength
)

print(f"Spectral Radiance on Sensor: {sensor_radiance} W/m^2/sr")

gain = calibrator.gain_calc(sensor_radiance, 193)

print(f"Gain: {gain}")

single_image_path = "/local/data/imgs589/data/MX1/raw/100027_TAM_22_10_2023_09_10_23_33_17/tam640/raw_2000.hdr"

util = CalUtils()

Tam = ImageReader()

img = Tam.read(single_image_path)

norm_img = util.quantization(img)

image_gain = calibrator.image_gain(norm_img, sensor_radiance)

print(image_gain)
