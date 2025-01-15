from src.thermal_cal.calibration import Calibrator

calibrator = Calibrator()

temp = 30 # In Celsius
wavelength = 8 # In micrometers
rsr_path = "data/cam_sheets/flir_rsr copy.csv"
temp_chamber = 10 # In Celsius

sensor_radiance = calibrator.calibrate_radiance(temp, temp_chamber, rsr_path, wavelength)

print(f'Spectral Radiance on Sensor: {sensor_radiance} W/m^2/sr')

gain = calibrator.gain_calc(sensor_radiance, 9607)

print(f'Gain: {gain}')