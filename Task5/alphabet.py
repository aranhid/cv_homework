import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def lakes(image):
    B = ~image
    BB = np.ones((B.shape[0] + 2, B.shape[1] + 2))
    BB[1:-1, 1:-1] = B
    return np.max(label(BB)) - 1

def lakes_area(image):
    B = ~image
    BB = np.ones((B.shape[0] + 2, B.shape[1] + 2))
    BB[1:-1, 1:-1] = B
    BB = label(BB)
    BB[BB == 1] = 0
    return label(BB).sum()

def has_vlines(image):
    lines = np.sum(image, 0) // image.shape[0]
    return np.sum(lines)

def has_bay(image):
    b = ~image
    bb = np.zeros((b.shape[0] + 1, b.shape[1])).astype("uint8")
    bb[:-1, :] = b
    return lakes(~bb) - 1

def bay_area(image):
    b = ~image
    bb = np.zeros((b.shape[0] + 1, b.shape[1])).astype("uint8")
    bb[:-1, :] = b
    return lakes_area(image)

def count_bays(image):
    holes = ~image.copy()
    return np.max(label(holes))

def recognize(region):
    lc = lakes(region.image)
    if lc == 2:
        if has_vlines(region.image) > 2:
            plt.imsave('images/B_' + str(region.label) + '.png', region.image)
            return "B"
        plt.imsave('images/8_' + str(region.label) + '.png', region.image)
        return "8"
    if lc == 1:
        if has_bay(region.image) > 0:
            plt.imsave('images/A_' + str(region.label) + '.png', region.image)
            return "A"
        if has_vlines(region.image) > 2:
            bay_relative_area = bay_area(region.image) / region.area
            if bay_relative_area > 0.5:
                plt.imsave('images/D_' + str(region.label) + '.png', region.image)
                return "D"
            plt.imsave('images/P_' + str(region.label) + '.png', region.image)
            return "P"
        plt.imsave('images/0_' + str(region.label) + '.png', region.image)
        return "0"
    if lc == 0:
        if has_vlines(region.image) > 2:
            if np.all(region.image == 1):
                plt.imsave('images/-_' + str(region.label) + '.png', region.image)
                return "-"
            plt.imsave('images/1_' + str(region.label) + '.png', region.image)
            return "1"
        bays = count_bays(region.image)
        
        if bays == 2:
            plt.imsave('images/Slash_' + str(region.label) + '.png', region.image)
            return "/"
        if bays > 3:
            circ = region.perimeter ** 2 / region.area
            if circ < 40:
                plt.imsave('images/Star' + str(region.label) + '.png', region.image)
                return "*"
            if bays == 5:
                plt.imsave('images/W_' + str(region.label) + '.png', region.image)
                return "W"
            if bays == 4:
                plt.imsave('images/X_' + str(region.label) + '.png', region.image)
                return "X"
    return None

image = plt.imread("symbols.png")
image = np.sum(image, 2)
image[image > 0] = 1

labeled = label(image)
print(np.max(labeled))

regions = regionprops(labeled)
d = {}
for region in regions:
    symbol = recognize(region)
    if symbol not in d:
        d[symbol] = 1
    else:
        d[symbol] += 1

print(d)

# plt.subplot(121)
# plt.imshow(image)
# plt.subplot(122)
# plt.imshow(labeled)
# plt.show()