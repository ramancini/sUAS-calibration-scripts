from src.cameras import Camera
from matplotlib import pyplot as plt


filepath = (
    "/Users/parkermei/Projects/Github/uas-thermal-cal/data/images/Tam Data/raw_0.hdr"
)

Tam = Camera("Tameris")

img = Tam.read(filepath)

print(img.shape)
print(img)

test = img[:,:,500]

plt.figure(figsize=(8, 6))
plt.imshow(test)
plt.colorbar()
plt.show()
