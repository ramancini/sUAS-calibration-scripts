from src.thermal_cal.file_search import FileSearch

path = "/local/data/imgs589/data/MX1/raw/100027_TAM_22_10_2023_09_10_23_33_17/tam640"

long_path = "/local/data/imgs589/data/MX1/raw/100051_tam_longtest_20241126_0814_22_22_2023_09_24_21_20_43/tam640"

path_3 = "/local/data/imgs589/data/MX1/raw/100045_tam_long_20241125_22_22_2023_09_24_06_19_41/tam640"


search = FileSearch()

# files = search.search(path_3)

# print(files)


file_path = "/home/cnspci/vcu_rice_river/emissivity/20250130/1300/grass.dwc"

test_path2 = "/home/cnspci/vcu_rice_river/emissivity/20250130/1300/grass.sac"

data = search.emmissivity_search(test_path2)

print(data)
