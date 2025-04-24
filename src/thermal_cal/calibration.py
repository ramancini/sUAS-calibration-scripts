from src.thermal_cal.blackbody import Blackbody


class Calibrator:
    def __init__(self):
        pass

    def calibrate_radiance(
        self,
        temperature,
        temperature_chamber,
        rsr_path,
        emissivity=1,
        reflectivity=0,
    ):
        """
        Calculate the radiance on the sensor using the Planck's law and the RSR of the sensor.
        Parameters:
        temperature: Temperature in Celsius.
        temperature_chamber: Temperature of the chamber in Celsius.
        rsr_path: Path to the RSR file as a csv.
        emissivity: Emissivity of the object.
        reflectivity: Reflectivity of the object.

        Returns:
        Radiance in W/m^2/sr/µm.
        """
        blackbody = Blackbody()

        radiance = (
            5.67e-8 * (temperature + 273.15) ** 4
        )  # Stefan-Boltzmann Law for total radiance
        bg_radiance = 5.67e-8 * (temperature_chamber + 273.15) ** 4
        band_radiance = blackbody.band_radiance(rsr_path, temperature)

        numerator = (
            (emissivity * radiance) + (reflectivity * bg_radiance)
        ) * band_radiance

        radiance_on_sensor = numerator / band_radiance

        return radiance_on_sensor

    def calibrate_images(self, image_cube, radiance_cube):
        """
        Calibrates the image digital counts to radiance using linear regression
        Parameters:
        image_cube: cube of images, channels are time
        radiance: cube of radiance values on sensor, channels are time

        Returns:
        calibration coeffecients: image file of calibation coeffiecents
        """
        rows, cols = image_cube.shape
        calibration_cube = np.zeros(rows, cols)
        # Iterating through image data
        for i in range(rows):
            for j in range(cols):
                digital_counts = image_cube[i, j, :]
                radiance_vals = radiance_cube[i, j, :]
                model = LinearRegression()

                # Fit the model to the data
                model.fit(digital_counts, radiance_vals)

                # Get the slope (coefficient) and intercept
                slope = model.coef_[0]
                intercept = model.intercept_

                calibration_cube[i, j, 0] = slope
                calibration_cube[i, j, 1] = intercept

        return calibration_cube

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
        gain_image = image
        gain_image = gain_image / (radiance - instrument_radiance)

        return gain_image

    def image_offset(self, image, img_gain, radiance):
        gain_term = img_gain * radiance
        offset_image = image / gain_term

        return offset_image
