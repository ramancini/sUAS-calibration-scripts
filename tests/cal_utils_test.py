from src.thermal_cal.cal_utils import CalUtils
from src.thermal_cal.file_search import FileSearch
from src.thermal_cal.image_reader import ImageReader

import matplotlib.pyplot as plt

path = "/local/data/imgs589/data/MX1/raw/100027_TAM_22_10_2023_09_10_23_33_17/tam640"

long_path = "/local/data/imgs589/data/MX1/raw/100051_tam_longtest_20241126_0814_22_22_2023_09_24_21_20_43/tam640"

path_3 = "/local/data/imgs589/data/MX1/raw/100045_tam_long_20241125_22_22_2023_09_24_06_19_41/tam640"

single_image_path = "/local/data/imgs589/data/MX1/raw/100027_TAM_22_10_2023_09_10_23_33_17/tam640/raw_2000.hdr"

search = FileSearch()

files = search.search(path)

cal = CalUtils()

Tam = ImageReader()

img = Tam.read(single_image_path)

norm_img = cal.quantization(img)

print(norm_img)

norm_img_visual = norm_img[:, :, 321]

plt.imshow(norm_img_visual)
plt.colorbar()
plt.savefig("Norm_Img.png")
plt.show()


""" final_img = cal.combine(files)

print(final_img.shape)

bad_pixel_map = cal.bad_pixel_map(final_img)

plt.imshow(bad_pixel_map)
plt.colorbar()
plt.savefig("Bad_Pixel_Map.png")
plt.show() """
