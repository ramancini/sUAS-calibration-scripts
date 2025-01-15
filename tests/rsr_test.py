import pandas as pd

csv_path = "data/cam_sheets/flir_rsr copy.csv"
# Convert the csv into a pandas dataframe
Datasheet = pd.read_csv(csv_path, sep=",", header=0)

value = 7.4

result = Datasheet.loc[Datasheet["Wavelength (µm)"] == value]

# Get the value in the specified next column
if not result.empty:
    next_column_value = result["Relative response"].values[0]
    print(next_column_value)
else:
    print("Value not found")
