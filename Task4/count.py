import os
import numpy as plt
import matplotlib.pyplot as plt
from skimage import filters, morphology
from skimage.measure import label, regionprops


def toGray(image):
    return (0.2989 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]).astype("uint8")


count = 0
folder = input("Enter path to images: ")

for file in os.listdir(folder):
    print(file)
    image = plt.imread(os.path.join(folder, file))
    gray = toGray(image)
    threshold = filters.threshold_isodata(gray)
    binary = gray < threshold
    binary = binary[70:-70, 70:-70]
    for i in range(45):
        binary = morphology.binary_dilation(binary)

    lbl = label(binary)
    # plt.imshow(lbl)
    # plt.show()
    for region in regionprops(lbl):
        if region.eccentricity > 0.95:
            count += 1
            # plt.imshow(region.image)
            # plt.show()
    print(count)

print(count)