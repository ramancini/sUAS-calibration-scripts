from src.cameras import Camera

filepath = (
    "/Users/parkermei/Projects/Github/uas-thermal-cal/data/images/Tam Data/raw_0.hdr"
)

Tam = Camera("Tameris")

img = Tam.read(filepath)

print(img.shape)
print(img)
