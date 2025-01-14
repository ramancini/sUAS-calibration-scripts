from scripts.cameras import Camera
from matplotlib import pyplot as plt


filepath = (
    "/Users/parkermei/Projects/Github/uas-thermal-cal/data/images/Tam Data/raw_0.hdr"
)

path = "/local/data/imgs589/data/MX1/raw/100027_TAM_22_10_2023_09_10_23_33_17/tam640/raw_0.hdr"

Tam = Camera("Tameris")

img = Tam.read(path)

print(img.shape)
print(img)

test = img[:,:,500]

plt.figure(figsize=(8, 6))
plt.imshow(test)
plt.colorbar()
plt.show()
