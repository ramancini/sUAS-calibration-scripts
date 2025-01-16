from src.thermal_cal.blackbody import Blackbody

blackbody = Blackbody()

Wavelength = 8  # Wavelength in microns
Temperature = -73.15  # Temperature in Celsius

exitance = blackbody.planck_exitance(Wavelength, Temperature)
print(f"Exitance: {exitance} W/m^2/")

radiance = blackbody.planck_radiance(Wavelength, Temperature)
print(f"Radiance: {radiance} W/m^2/sr/µm")

# Enter path of the RSR File as a csv
csv_path = "data/cam_sheets/flir_rsr copy.csv"

# Calculate the band radiance with RSR
band_radiance = blackbody.band_radiance(csv_path, Temperature)

print(f"Band Radiance: {band_radiance} W/m^2/sr")
