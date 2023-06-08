""" Image resizer and crop automatically.

Usage:
    imgr.py --width=<width> [--height=<height>] [--folder=<folder>]

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from pathlib import Path
from PIL import Image
import unidecode
import os, re

if __name__ == "__main__":
    arguments = docopt(__doc__, argv=None, help=True, version="1.0", options_first=False)

    folder = '.' if arguments['--folder'] is None else str(arguments['--folder'])

    for f in os.listdir(folder):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in [".jpg", ".gif", ".png"]:
            continue

        fileName = os.path.join(folder, f)
        path = Path(fileName)

        image = Image.open(fileName)
        original_width, original_height = image.size

        print(path.name)
        print(f"Original size : ({original_width}, {original_height})")

        try:
            new_width = int(arguments['--width'])
        except:
            print('Invalid argument --width  must be numeric value')
            exit()

        if original_width >= new_width:
            image.thumbnail((new_width, new_width))
        else:
            # calculate height ratio
            new_height = new_width * original_height / original_width
            image = image.resize((new_width, int(new_height)), Image.LANCZOS)

        if not arguments['--height'] is None:
            try:
                new_height = int(arguments['--height'])
            except:
                print('Invalid argument --height must be numeric value')
                exit()
        else:
            new_height = image.size[1]

        if new_height > image.size[1]:
            new_image = Image.new("RGB", (new_width, new_height), (255, 255, 255))
            x = (new_image.width - image.size[0]) // 2
            y = (new_image.height - image.size[1]) // 2
            new_image.paste(image, (x, y), image.convert('RGBA'))
            image = new_image
        else:
            if new_height < image.size[1]:
                top = ((image.size[1] - new_height) / 2)  # calculate top of height
                box = (0, int(top), new_width, new_height + int(top))
                image = image.crop(box)

        print(f"New size : {image.size}")

        new_file = re.sub(r'[\W_]+', '-', unidecode.unidecode(os.path.splitext(path.name)[0])) + ext
        new_file = os.path.join(folder, new_file)

        if ext == ".jpg" or ext == '.jpeg':
            image.save(new_file, 'JPEG', quality=100)
        elif ext == '.png':
            image.save(new_file, 'PNG', quality=100)
        elif ext == '.gif':
            image.save(new_file, 'GIF', quality=100)

        print(f'Image saved as {new_file}')
