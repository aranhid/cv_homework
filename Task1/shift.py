import numpy as np
from io import StringIO
from scipy import ndimage


def read_file(filename):
    with open(filename, 'r') as file_input:
        file_input.readline()
        file_input.readline()
        data = StringIO(file_input.read())
        image = np.loadtxt(data, dtype=int)
    return image


def find_position(image, object):
    for y in range(image.shape[0] - object.shape[0]):
        for x in range(image.shape[1] - object.shape[1]):
            frame = image[y:y+obj.shape[0], x:x+obj.shape[1]]
            if (np.all(frame == obj)):
                return y, x
    return None, None


image1 = read_file('img1.txt')
image2 = read_file('img2.txt')
obj = image1[ndimage.find_objects(image1)[0]]
y1, x1 = find_position(image1, obj)
y2, x2 = find_position(image2, obj)

if (y1 and y2):
    print("delta x: ", x2 - x1)
    print("delta y: ", y2 - y1)