import pandas as pd

from src.thermal_cal.blackbody import Blackbody

blackbody = Blackbody()

Wavelength = 8  # Wavelength in micrometers
Temperature = 200  # Temperature in Kelvin
exitance = blackbody.planck_exitance(Wavelength, Temperature)
print(f"Exitance: {exitance} W/m^2/sr/µm")

Wavelength = 8  # Wavelength in micrometers
Temperature = 200  # Temperature in Kelvin
radiance = blackbody.planck_radiance(Wavelength, Temperature)
print(f"Radiance: {radiance} W/m^2/sr/µm")

# Enter CSV Path of the RSR File
csv_path = (
    "data/cam_sheets/flir_rsr copy.csv"
)
# Convert the csv into a pandas dataframe
Datasheet = pd.read_csv(csv_path, sep=",", header=0)

# Convert wavelengths into np array
wavelength = Datasheet["Wavelength (µm)"]
wavelengths = wavelength.to_numpy()
# Convert rsr into np array
rsr = Datasheet["Relative response"]
rsr = rsr.to_numpy()

Temperature = 30  # Temperature in Celsius
band_radiance = blackbody.band_radiance(wavelengths, rsr, Temperature)

print(f"Band Radiance: {band_radiance} W/m^2/sr")