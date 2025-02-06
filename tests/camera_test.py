from src.thermal_cal.image_reader import ImageReader
from matplotlib import pyplot as plt

path = "/local/data/imgs589/data/MX1/raw/100027_TAM_22_10_2023_09_10_23_33_17/tam640/raw_2000.hdr"

path = "/local/data/imgs589/field_data/100062_20250117_Solar_2025_01_17_17_05_35/tam640/raw_4000.hdr"

Tam = ImageReader()

img = Tam.read(path)

print(img.shape)

test = img[:, :, 0]

print(img)

plt.figure(figsize=(8, 6))
plt.imshow(test)
plt.colorbar()
plt.savefig("data/cam_sheets/images/Field_Test3.png")
plt.show()
