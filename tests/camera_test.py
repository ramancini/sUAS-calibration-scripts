from src.cameras import Camera

filepath = '/Users/parkermei/Projects/Github/uas-thermal-cal/data/images/Tam Data/raw_0.hdr'

reader = Camera("Tameris")

img = reader.read(filepath)

print(img.shape)
