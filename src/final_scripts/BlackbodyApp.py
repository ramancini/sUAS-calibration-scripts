import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# DANNY CODE
# rubber temp 39.1c or 312.25

def interp1(x, y, xp, order=1, extrapolate=False):
    # Make sure that the provided data set consists of numpy ndarrays, if
    # not, convert them for use within the scope of this method
    if type(x).__module__ != np.__name__:
        xN = np.asarray(x, dtype=float)
    else:
        xN = x

    if type(y).__module__ != np.__name__:
        yN = np.asarray(y, dtype=float)
    else:
        yN = y

    # Make sure the elements of the provided data set are the same length
    if xN.size != yN.size:
        raise ValueError('Provided datasets must have the same size')

    # Compute the vector of knots and the B-spline coefficients for the
    # provided data
    tck = scipy.interpolate.splrep(xN, yN, k=order, s=0)

    # Given the knots and B-spline coefficients, evaluate the ordinate 
    # value(s) of the spline at the provided abscissa location(s)
    yp = scipy.interpolate.splev(xp, tck)

    # If extrapolation is not desired, return NaN for abscissa value(s)
    # outside the range of the original data provided
    if extrapolate is False:
        index = np.where(xp < xN[0])
        if len(index[0]) > 0:
            yp[index[0]] = float('NaN')

        index = np.where(xp > xN[-1])
        if len(index[0]) > 0:
            yp[index[0]] = float('NaN')

    # Return the interpolated/extrapolated ordinate value(s) using the same
    # array-like structure as the provided data
    if type(y).__module__ != np.__name__:
        return yp.tolist()
    else:
        return yp


class BlackbodyApp:
    def __init__(self, root):
        """
        Initialize the Blackbody GUI application.
        :param root: The root window of the application.
        """
        self.root = root
        self.root.title("Blackbody Radiation Calculator")

        # Variables for user input
        self.start_temp = tk.DoubleVar(value=300)  # Default start temperature
        self.temp_range = tk.DoubleVar(value=0)   # Default temperature range (±x)
        self.temp_increment = tk.DoubleVar(value=1)  # Default temperature increment
        self.wavelength_start = tk.DoubleVar(value=7.5)  # Default wavelength start (µm)
        self.wavelength_end = tk.DoubleVar(value=12.5)   # Default wavelength end (µm)
        self.wavelength_increment = tk.DoubleVar(value=0.005)  # Default wavelength increment (µm)
        self.imported_wavelengths = None  # For storing imported wavelength regions
        self.emissivity_data = None  # For storing emissivity data
        self.rsr_data = None  # For storing RSR data
        self.rsr_wavelengths = None
        self.emissivity_wavelengths = None

        # Create and layout the GUI components
        self.create_widgets()

    def create_widgets(self):
        """
        Create and layout the GUI components.
        """
        # Frame for temperature inputs
        temp_frame = ttk.LabelFrame(self.root, text="Temperature Settings")
        temp_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(temp_frame, text="Start Temperature (K):").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(temp_frame, textvariable=self.start_temp).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(temp_frame, text="Temperature Range (±x):").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(temp_frame, textvariable=self.temp_range).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(temp_frame, text="Temperature Increment:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(temp_frame, textvariable=self.temp_increment).grid(row=2, column=1, padx=5, pady=5)

        # Frame for wavelength inputs
        wavelength_frame = ttk.LabelFrame(self.root, text="Wavelength Settings")
        wavelength_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(wavelength_frame, text="Wavelength Start (µm):").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(wavelength_frame, textvariable=self.wavelength_start).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(wavelength_frame, text="Wavelength End (µm):").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(wavelength_frame, textvariable=self.wavelength_end).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(wavelength_frame, text="Wavelength Increment (µm):").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(wavelength_frame, textvariable=self.wavelength_increment).grid(row=2, column=1, padx=5, pady=5)

        # Button to import wavelength regions from CSV
        ttk.Button(wavelength_frame, text="Import Wavelength Regions (CSV or TXT)", command=self.import_wavelengths).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Button to import emissivity data from CSV
        ttk.Button(wavelength_frame, text="Import Emissivity Data (CSV or TXT)", command=self.import_emissivity).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Button to import RSR data from CSV
        ttk.Button(wavelength_frame, text="Import RSR Data (CSV or TXT)", command=self.import_rsr).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Button to calculate and plot
        ttk.Button(self.root, text="Calculate and Plot", command=self.calculate_and_plot).grid(row=2, column=0, padx=10, pady=10)

        # Frame for results and plot
        result_frame = ttk.LabelFrame(self.root, text="Results")
        result_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Button to open formula pop-up
        ttk.Button(wavelength_frame, text="Open Sensor Radiance Calculator", command=self.open_formula_calculator).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Clear Data
        ttk.Button(wavelength_frame, text="Clear All Imported Data", command=self.clear_data).grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        self.result_text = tk.Text(result_frame, height=10, width=60)
        self.result_text.grid(row=0, column=0, padx=5, pady=5)

        # Create separate figures and canvases for each plot
        self.fig_spectral, self.ax1 = plt.subplots()
        self.canvas_spectral = FigureCanvasTkAgg(self.fig_spectral, master=self.root)
        self.canvas_spectral.get_tk_widget().grid(row=0, column=1, rowspan=4, padx=10, pady=10)

        self.fig_emissivity, self.ax2 = plt.subplots()
        self.canvas_emissivity = FigureCanvasTkAgg(self.fig_emissivity, master=self.root)
        self.canvas_emissivity.get_tk_widget().grid(row=0, column=2, rowspan=4, padx=10, pady=10)

        self.fig_rsr, self.ax3 = plt.subplots()
        self.canvas_rsr = FigureCanvasTkAgg(self.fig_rsr, master=self.root)
        self.canvas_rsr.get_tk_widget().grid(row=2, column=1, rowspan=4, padx=10, pady=10)

        # Scrollable frame for toggle buttons
        self.toggle_buttons_frame = ttk.LabelFrame(self.root, text="Toggle Curves")
        self.toggle_buttons_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        # Create a canvas and scrollbar for the toggle buttons
        self.toggle_canvas = tk.Canvas(self.toggle_buttons_frame)
        self.toggle_scrollbar = ttk.Scrollbar(self.toggle_buttons_frame, orient="vertical", command=self.toggle_canvas.yview)
        self.toggle_scrollable_frame = ttk.Frame(self.toggle_canvas)

        # Configure the canvas
        self.toggle_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.toggle_canvas.configure(
                scrollregion=self.toggle_canvas.bbox("all")
            )
        )

        self.toggle_canvas.create_window((0, 0), window=self.toggle_scrollable_frame, anchor="nw")
        self.toggle_canvas.configure(yscrollcommand=self.toggle_scrollbar.set)

        # Pack the canvas and scrollbar
        self.toggle_canvas.pack(side="left", fill="both", expand=True)
        self.toggle_scrollbar.pack(side="right", fill="y")

        self.toggle_buttons = {}  # To store toggle buttons

    def import_wavelengths(self):
        """
        Import wavelength regions from a CSV file.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                self.imported_wavelengths = df.iloc[:, 0]
                self.result_text.insert(tk.END, "Imported Wavelengths.\n")
            except Exception as e:
                self.result_text.insert(tk.END, f"Error reading file: {e}\n")

    def import_emissivity(self):
        """
        Import emissivity data from a CSV file.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
        if file_path:
            try:
                # Import DF and sort from low to high
                df = pd.read_csv(file_path)
                sorted_df = df.sort_values(by='Wavelength')
                self.emissivity_wavelengths = sorted_df.iloc[:, 0].values  # Already in microns
                self.emissivity_data = sorted_df.iloc[:, 1].values
                self.result_text.insert(tk.END, "Imported wavelengths and Emissivity values.\n")
            except Exception as e:
                self.result_text.insert(tk.END, f"Error reading file: {e}\n")

    def import_rsr(self):
        """
        Import RSR data from a CSV file.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                self.rsr_wavelengths = df.iloc[:, 0].values  # Already in microns
                self.rsr_data = df.iloc[:, 1].values  # Second column as RSR values
                self.result_text.insert(tk.END, "Imported wavelengths and RSR values.\n")
            except Exception as e:
                self.result_text.insert(tk.END, f"Error reading file: {e}\n")

    def clear_data(self):
        """
        Clear all imported data (RSR, emissivity, and wavelengths).
        """
        self.rsr_data = None
        self.rsr_wavelengths = None
        self.emissivity_data = None
        self.emissivity_wavelengths = None
        self.imported_wavelengths = None
 
        # Clear the result text
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "All imported data and plots cleared.\n")
       
        # Clear the plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
       
        # Redraw the canvases
        self.canvas_spectral.draw()
        self.canvas_emissivity.draw()
        self.canvas_rsr.draw()
        
    def calculate_and_plot(self):
        """
        Calculate the blackbody curves and plot them.
        """
        # Clear previous results and plots
        self.result_text.delete(1.0, tk.END)
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        for widget in self.toggle_scrollable_frame.winfo_children():
            widget.destroy()

        # Get user inputs
        start_temp = self.start_temp.get()
        temp_range = self.temp_range.get()
        temp_increment = self.temp_increment.get()
        wavelength_start = self.wavelength_start.get()  # Already in microns
        wavelength_end = self.wavelength_end.get()      # Already in microns
        wavelength_increment = self.wavelength_increment.get()  # Already in microns

        # Use imported wavelengths if available
        if self.imported_wavelengths is not None:
            wavelength_spectrum = self.imported_wavelengths
        else:
            # Wavelength Range in Meters 
            wavelength_spectrum = np.arange(wavelength_start, wavelength_end, wavelength_increment)

        # Numpy Interp
        # Interpolate emissivity and RSR data if necessary
        if self.emissivity_data is not None:
            if not np.array_equal(self.emissivity_wavelengths, wavelength_spectrum):
                self.emissivity_data = interp1(self.emissivity_wavelengths, self.emissivity_data, wavelength_spectrum, extrapolate=True)
                self.result_text.insert(tk.END, "Emissivity data interpolated to match wavelength range.\n\n")

        if self.rsr_data is not None:
            if not np.array_equal(self.rsr_wavelengths, wavelength_spectrum):
                self.rsr_data = interp1(self.rsr_wavelengths, self.rsr_data, wavelength_spectrum, extrapolate=True)
                self.result_text.insert(tk.END, "RSR data interpolated to match wavelength range.\n\n")

        # Calculate blackbody curves for the temperature range
        temperatures = np.arange(start_temp - temp_range, start_temp + temp_range + 1, temp_increment)
        self.toggle_buttons = {}  # Reset toggle buttons


        for temp in temperatures:
            spectral_exitance = self.blackbody_exitance(wavelength_spectrum, temp) #Final units [W/cm^2 * µm]
            spectral_radiance = self.blackbody_exitance(wavelength_spectrum, temp) / np.pi #Final units [W/cm^2 * sr * µm]

            if self.emissivity_data is not None:
                spectral_radiance *= self.emissivity_data[:]

            if self.rsr_data is not None:
                spectral_radiance *= self.rsr_data[:]
  
            line, = self.ax1.plot(wavelength_spectrum, spectral_radiance , label=f"{temp} K", visible=(temp == start_temp))

            # Add toggle button for this temperature
            var = tk.BooleanVar(value=bool(temp == start_temp))  # Convert np.bool_ to Python bool
            toggle_button = ttk.Checkbutton(self.toggle_scrollable_frame, text=f"{temp:.2f} K", variable=var, command=lambda t=temp, v=var: self.toggle_curve(t, v))
            toggle_button.pack(anchor="w")
            self.toggle_buttons[temp] = (line, var)

            # Calculate and display peak wavelength
            peak_wavelength = self.peak_wavelength(temp)
            self.result_text.insert(tk.END, f"Temperature: {temp:.2f} K\n")
            self.result_text.insert(tk.END, f"Peak Wavelength: {peak_wavelength:.2f} µm\n")
    
            integrated_spectral_radiance = np.trapz(spectral_radiance, wavelength_spectrum)
            # self.result_text.insert(tk.END, f"Integrated Spectral Radiance: {integrated_spectral_radiance:.6} W/(cm² sr)\n")
            self.result_text.insert(tk.END, f"Integrated Spectral Radiance: {integrated_spectral_radiance:.6} W/(m² sr)\n")

                
            integrated_spectral_exitance = np.trapz(spectral_exitance, wavelength_spectrum)  
            self.result_text.insert(tk.END, f"Integrated Spectral Exitance: {integrated_spectral_exitance:.4} W/cm²\n\n")



        # Plot emissivity data if available
        if self.emissivity_data is not None:
            self.ax2.plot(wavelength_spectrum, self.emissivity_data, label="Emissivity", color="blue")
            self.ax2.set_title("Material Emissivity")
            self.ax2.set_ylabel("Emissivity")
            self.ax2.set_xlabel("Wavelength (µm)")
            self.ax2.grid(True)
            self.ax2.relim()  # Rescale the axis
            self.ax2.autoscale_view()

        # Plot RSR data if available
        if self.rsr_data is not None:
            self.ax3.plot(wavelength_spectrum, self.rsr_data, label="RSR", color="green")
            self.ax3.set_ylabel("RSR")
            self.ax3.set_xlabel("Wavelength (µm)")
            self.ax3.set_title("Detector RSR")
            self.ax3.grid(True)
            self.ax3.relim()  # Rescale the axis
            self.ax3.autoscale_view()

        # Customize the spectral radiance plot
        self.ax1.set_xlabel("Wavelength (µm)")
        self.ax1.set_ylabel("Spectral Radiance (W/(cm² sr µm))")
        self.ax1.set_title("Blackbody Radiation Curves")
        self.ax1.grid(True)
        self.ax1.relim()  # Rescale the axis
        self.ax1.autoscale_view()

        # Redraw the canvases
        self.canvas_spectral.draw()
        self.canvas_emissivity.draw()
        self.canvas_rsr.draw()

    def toggle_curve(self, temperature, var):
        """
        Toggle the visibility of a temperature curve.
        :param temperature: The temperature of the curve to toggle.
        :param var: The BooleanVar associated with the toggle button.
        """
        line, _ = self.toggle_buttons[temperature]
        line.set_visible(var.get())
        self.canvas_spectral.draw()

   
    def blackbody_exitance(self, wavelength_spectrum, temperature):
        """
        Calculate the spectral exitance of the blackbody at a given temperature.
        :param wavelength_spectrum: Array of wavelengths in microns.
        :param temperature: Temperature in Kelvin.
        :return: Array of spectral exitance values in W/(cm²·sr·µm).
        """
        h = 6.62607015e-34  # Planck's constant (Joule seconds)
        c = 2.99792458e8    # Speed of light (meters/second)
        kb = 1.380649e-23   # Boltzmann constant (Joules/Kelvin)
    
        # Convert wavelength from microns to meters
        wavelength_spectrum_m = wavelength_spectrum * 1e-6
    
        # Calculate spectral exitance
        toppart = 2 * np.pi * h * c**2
        bottompart = (wavelength_spectrum_m**5) * (np.exp((h * c) / (wavelength_spectrum_m * kb * temperature)) - 1)
    
        # Spectral exitance in W/(m²·sr·µm)
        spectral_exitance = (toppart / bottompart) * 1e-6  # Convert to W/(m²·sr·µm)
    
        # Convert to W/(cm²·sr·µm) by multiplying by 10e-4
        return spectral_exitance # * 1e-4  # Final units [W/(cm²·sr·µm)]


    def peak_wavelength(self, temperature):
        """
        Calculate the peak wavelength of emission using Wien's displacement law.
        :param temperature: Temperature in Kelvin.
        :return: Peak wavelength in microns.
        """
        return 2897.771955 / temperature  # Wien's displacement law in microns

    def open_formula_calculator(self):
        """
        Open a pop-up window for the formula calculator.
        """
        # Create a new pop-up window
        popup = tk.Toplevel(self.root)
        popup.title("Formula Calculator")
        popup.geometry("400x300")

        # Display the formula
        self.formula_label = ttk.Label(popup, text="Lₛ(λ) = (L\u1d33(λ) - Lᵤ(λ)) / τ")
        self.formula_label.pack(pady=10)

        # Input fields for variables
        ttk.Label(popup, text="L\u1d33(λ):").pack()
        self.lg_entry = ttk.Entry(popup)
        self.lg_entry.pack()
        self.lg_entry.bind("<KeyRelease>", self.update_formula_display)

        ttk.Label(popup, text="τ:").pack()
        self.transmission_entry = ttk.Entry(popup)
        self.transmission_entry.pack()
        self.transmission_entry.bind("<KeyRelease>", self.update_formula_display)

        ttk.Label(popup, text="Lᵤ(λ):").pack()
        self.lu_entry = ttk.Entry(popup)
        self.lu_entry.pack()
        self.lu_entry.bind("<KeyRelease>", self.update_formula_display)

        # Button to compute the result
        ttk.Button(popup, text="Compute", command=self.compute_formula).pack(pady=10)

        # Label to display the result
        self.result_label = ttk.Label(popup, text="Result: ")
        self.result_label.pack()

    def update_formula_display(self, event=None):
        """
        Update the formula display with the current input values.
        """
        lg = self.lg_entry.get()
        transmission = self.transmission_entry.get()
        lu = self.lu_entry.get()

        # Update the formula display
        self.formula_label.config(text=f"Lₛ(λ) = ({lg} - {lu}) / {transmission}")

    def compute_formula(self):
        """
        Compute the result of the formula.
        """
        try:
            # Get input values
            lg = float(self.lg_entry.get())
            transmission = float(self.transmission_entry.get())
            lu = float(self.lu_entry.get())

            # Compute the result
            result = (lg - lu) / transmission
            result_cm2 = result  # Result in cm²
            result_m2 = result * 1e4  # Convert cm² to m²

            # Display the result
            self.result_label.config(text=f"Result: {result_cm2:.4f} cm²\n{result_m2:.4f} m²")

        except ValueError:
            self.result_label.config(text="Invalid input. Please enter numbers.")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackbodyApp(root)
    root.mainloop()