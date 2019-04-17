from PIL import Image

file = "lobo.jpg"
img = Image.open(file).convert('LA')
img.save('greyscale.png')