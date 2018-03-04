import math
from PIL import Image, ImageFont

def to_text(im, font):
    w, h = font.getsize('/')
    text = ''
    for y in range(math.floor(im.height/h)):
        for x in range(math.floor(im.width/w)):
            c = '/'
            text += c
        text += '\n'

    return text[:-1]

if __name__ == '__main__':
    import sys
    im = Image.open(sys.argv[1])
    font = ImageFont.truetype('./static/OpenSans-Regular.ttf')
    text = to_text(im, font)
    print(text)
