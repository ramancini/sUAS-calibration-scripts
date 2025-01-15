import pandas as pd

from src.thermal_cal.blackbody import Blackbody


class Calibrator:
    def __init__(self):
        pass

    def calibrate_radiance(
        self,
        temperature,
        temperature_chamber,
        rsr_path,
        wavelength,
        emissivity=1,
        reflectivity=0,
    ):
        """
        Calculate the radiance on the sensor using the Planck's law and the RSR of the sensor.
        Parameters:
        wavelength: Wavelength in micrometers.
        temperature: Temperature in Celsius.
        temperature_chamber: Temperature of the chamber in Celsius.
        rsr_path: Path to the RSR file as a csv.
        emissivity: Emissivity of the object.
        reflectivity: Reflectivity of the object.

        Returns:
        Radiance in W/m^2/sr/µm.
        """
        blackbody = Blackbody()

        #radiance = blackbody.planck_radiance(wavelength, temperature)
        radiance = 5.67e-8 * (temperature +273.15) ** 4 # Stefan-Boltzmann Law, maybe works?
        bg_radiance = blackbody.planck_radiance(wavelength, temperature_chamber)
        band_radiance = blackbody.band_radiance(rsr_path, temperature)

        # Convert the csv into a pandas dataframe
        Datasheet = pd.read_csv(rsr_path, sep=",", header=0)

        result = Datasheet.loc[Datasheet["Wavelength (µm)"] == wavelength]

        # Get the Responsivity value in the specified next column
        if not result.empty:
            relative_response = result["Relative response"].values[0]
        else:
            raise ValueError(
                "Responsivity value not found for the specified wavelength"
            )

        numerator = (
            (emissivity * radiance) + (reflectivity * bg_radiance)
        ) * relative_response

        radiance_on_sensor = numerator / band_radiance

        return radiance_on_sensor

    def gain_calc(self, radiance, digital_count, offset=0, instrument_radiance=0):
        """
        Calculate the gain of the sensor.
        Parameters:
        radiance: Radiance in W/m^2/sr/µm.
        digital_count: Digital count of the sensor.
        offset: Offset of the sensor.
        instrument_radiance: Radiance of the instrument.

        Returns:
        Gain of the sensor."""

        gain = (digital_count - offset) / (radiance - instrument_radiance)

        return gain

    def offset_calc(self, radiance, digital_count, gain, instrument_radiance=0):
        """
        Calculate the offset of the sensor.
        Parameters:
        radiance: Radiance in W/m^2/sr/µm.
        digital_count: Digital count of the sensor.
        gain: Gain of the sensor.
        instrument_radiance: Radiance of the instrument.
        Returns:
        Offset of the sensor."""

        offset = digital_count - (gain * (radiance - instrument_radiance))

        return offset

    def image_gain(self, image, radiance, offset=0, instrument_radiance=0):
        gain_image = image - offset
        gain_image = gain_image / (radiance - instrument_radiance)

        return gain_image

    def image_offset(self, image, radiance, gain, instrument_radiance=0):
        offset_image = image / (gain * (radiance - instrument_radiance))

        return offset_image
