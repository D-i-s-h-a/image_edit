"""

file: sketch.py

"""

from simpleimage import SimpleImage

RGB_MAX = 255
BLUR_SIZE = 9
BLUR_ITER = 10

def main():
    image= SimpleImage("images/(use any image).jpg")
    image.show()

    gray= image_gray(image)
    gray.show()

    inverted= inverted_image(gray)
    inverted.show()

    blurred= blur(inverted, BLUR_ITER, BLUR_SIZE)
    blurred.show()

    pencil = dodge (gray, blurred)
    pencil.show()


def copy_image(image):
    copy= SimpleImage.blank (image.width, image.height)
    for pixel in copy:
        x=pixel.x
        y=pixel.y
        copy.set_pixel(x, y, image.get_pixel(x, y))
    return copy


def image_gray(image):
    gray= copy_image(image)
    for pixel in gray:
        value= 0.299*pixel.red + 0.587*pixel.green + 0.114*pixel.blue
        pixel.red= value
        pixel.green= value
        pixel.blue= value
    return gray

def inverted_image(image):
    inverted= copy_image(image)
    for pixel in inverted:
        pixel.red = RGB_MAX - pixel.red
        pixel.green = RGB_MAX - pixel.green
        pixel.blue = RGB_MAX - pixel.blue
    return inverted

def blur(image, BLUR_ITER, BLUR_SIZE):
    blurred= None
    ref = image
    for i in range(BLUR_ITER):
        blurred = copy_image(ref)
        for x in range(ref.width):
            for y in range(ref.height):
                blur_pixel(x, y, blurred, ref, BLUR_SIZE)
        ref = blurred
    return blurred

def blur_pixel(x, y, blurred, ref, BLUR_SIZE):
    red=0
    green=0
    blue=0
    count=0
    r = (BLUR_SIZE-1) // 2
    for i in range(x-r, x+r+1):
        for j in range(y-r, y+r+1):
            if in_bound(i, j, ref.width, ref.height):
                count += 1
                pixel=ref.get_pixel(i, j)
                red += pixel.red
                green += pixel.green
                blue += pixel.blue
    pixel = blurred.get_pixel(x, y)
    pixel.red = red / count
    pixel.green = green / count
    pixel.blue = blue / count

def in_bound(x, y, width, height):
    if 0 <= x < width and 0 <= y < height:
        return True
    return False

def dodge (top, bottom):
    image = copy_image(top)
    for pixel in image:
        x=pixel.x
        y=pixel.y
        pixel_top= top.get_pixel(x, y)
        pixel_bottom= bottom.get_pixel(x, y)
        pixel.red = compute_dodge (pixel_top.red, pixel_bottom.red)
        pixel.green = compute_dodge (pixel_top.green, pixel_bottom.green)
        pixel.blue = compute_dodge (pixel_top.blue, pixel_bottom.blue)
    return image

def compute_dodge(top_val, bottom_val):
    val = bottom_val*RGB_MAX / max(1, RGB_MAX - top_val)
    return min(val, RGB_MAX)


if __name__ == '__main__':
    main()
