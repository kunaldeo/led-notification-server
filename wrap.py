from PIL import Image
from PIL import ImageFont


def text_wrap(text, font, max_width):
    lines = []
    # If the width of the text is smaller than image width
    # we don't need to split it, just add it to the lines array
    # and return
    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        # split the line by spaces to get words
        words = text.split(' ')
        i = 0
        # append every word to a line while its width is shorter than image width
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            # when the line gets longer than the max width do not append the word,
            # add the line to the lines array
            lines.append(line)
    return lines


def split_lines(text):
    # open the background file
    img = Image.open('bg.jpg')

    # size() returns a tuple of (width, height)
    image_size = img.size

    # create the ImageFont instance
    font_file_path = 'Roboto-Regular.ttf'
    font = ImageFont.truetype(font_file_path, size=11, encoding="unic")

    # get shorter lines
    lines = text_wrap(text, font, image_size[0])
    return lines


if __name__ == "__main__":
    split_lines("This could be a single line text but its too long to fit in one.")
