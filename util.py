from PIL import Image

def image_resize(input_image_file, resfile):
    new_height = 300
    im = Image.open(input_image_file)
    w,h = im.size
    if (w<=500 or h<=300):
        im.save(resfile)
        return True
    new_width = w*new_height/h
    out = im.resize((new_width, new_height))
    out.save(resfile)
    return True

