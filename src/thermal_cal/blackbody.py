import numpy as np
import pandas as pd
import scipy.integrate as integrate


class Blackbody:
    """
    A class for calculating blackbody radiation using Planck's law.
    """

    def __init__(self):
        """
        Initialize the Blackbody object with physical constants.
        """
        self.h = 6.62607015e-34  # Planck's constant
        self.c = 299792458  # Speed of light
        self.k = 1.380649e-23  # Boltzmann constant

    def planck_exitance(self, wavelength, temperature):
        """
        Calculate the exitance of a blackbody.

        Parameters:
        wavelength: Wavelength in micrometers.
        temperature: Temperature in Celsius.

        Returns:
        Exitance in W/m^2/sr/µm.
        """
        temperature = temperature + 273.15  # Convert temperature to Kelvin
        wavelength = wavelength * 1e-6  # Convert micrometers to meters
        c1 = 2 * np.pi * self.h * self.c**2
        c2 = self.h * self.c / (self.k * temperature * wavelength)
        numerator = c1
        denominator = wavelength**5 * (np.exp(c2) - 1)
        return (numerator / denominator) * 10e-7

    def planck_radiance(self, wavelength, temperature):
        """
        Calculate the radiance of a blackbody.

        Parameters:
        wavelength: Wavelength in micrometers.
        temperature: Temperature in Celsius.

        Returns:
        Radiance in W/m^2/sr/µm.
        """
        temperature = temperature + 273.15  # Convert temperature to Kelvin
        wavelength = wavelength * 1e-6  # Convert micrometers to meters
        c1 = 2 * self.h * self.c**2
        c2 = self.h * self.c / (self.k * temperature * wavelength)
        numerator = c1
        denominator = wavelength**5 * (np.exp(c2) - 1)
        return numerator / denominator * 10e-7

    def band_radiance(self, rsr_path, temperature):
        """
        Calculate the band radiance of a blackbody.

        Parameters:
        wavelengths: Array of wavelengths in micrometers.
        rsr_path: Path to the relative spectral response file.
        temperature: Temperature in Celsius.

        Returns:
        Band radiance for pixel element.
        """
        Datasheet = pd.read_csv(rsr_path, sep=",", header=0)
        wavelength = Datasheet["Wavelength (µm)"]
        wavelengths = wavelength.to_numpy()
        rsr = Datasheet["Relative response"]
        rsr = rsr.to_numpy()
        band_radiance = np.multiply(self.planck_radiance(wavelengths, temperature), rsr)
        total_radiance = integrate.trapezoid(band_radiance, wavelengths)
        return total_radiance
