from src.thermal_cal.image_reader import ImageReader
from matplotlib import pyplot as plt
import numpy as np

path = "/local/data/imgs589/data/MX1/raw/100027_TAM_22_10_2023_09_10_23_33_17/tam640/raw_2000.hdr"

path = "/local/data/imgs589/data/calibration/raw/tam640/20241119/295.15/295.15/raw_2000.hdr"

Tam = ImageReader()

img = Tam.read(path)

print(img.shape)

test = img[:, :, 500]


hist_img = np.histogram(img)

print(hist_img)

plt.hist(hist_img, bins="auto")
plt.title("Histogram")
plt.savefig("Histogram2.png")


plt.figure(figsize=(8, 6))
plt.imshow(test)
plt.colorbar()
plt.savefig("Test.png")
plt.show()
