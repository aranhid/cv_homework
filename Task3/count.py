import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.morphology import binary_opening
from skimage.measure import label, regionprops

image = np.load('ps.npy.txt')
labeled = label(image)
n = np.max(labeled)

masks = [
    np.array([[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]),
    np.array([[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1]]),
    np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0], [1, 1, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1]]),
    np.array([[1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]),
    np.array([[1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]),
]

objects = []

for mask in masks:
    binop = binary_opening(image, mask)
    binop_labeled = label(binop)
    count = np.max(binop_labeled)
    objects.append(count)

areas = []

regions = regionprops(labeled)
for region in regions:
    areas.append(region.area)

d = {}

for ar in areas:
    if ar in d:
        d[ar] += 1
    else:
        d[ar] = 1

print("Count: ", n)
print("Objects: ", objects)
print("Areas: ", d)

plt.imshow(image)
plt.show()