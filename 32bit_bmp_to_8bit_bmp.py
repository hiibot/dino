from PIL import Image

image = Image.open('imgs/mario.bmp')
result = image.quantize(colors=256, method=2)
result.save('imgs/mario.bmp')
