import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
import numpy as np
from skimage import color

image = plt.imread("balls_and_rects.png")
binary = image.copy()[:, :, 0]
binary[binary > 0] = 1
image = color.rgb2hsv(image)[:, :, 0]

labeled = label(binary)
print("Total shapes: ", np.max(labeled))

colors = []

for region in regionprops(labeled):
    bb = region.bbox
    region_color = np.max(image[bb[0]:bb[2], bb[1]:bb[3]])
    colors.append(region_color)

colors.sort()

plt.figure()
plt.plot(np.diff(colors), 'o')

diffs = np.diff(colors)
diffs = diffs[diffs > 0.05]

ranged_colors = [colors[0]]
for diff in diffs:
    ranged_colors.append(ranged_colors[-1] + diff)

# print(colors)
# print(diffs)
# print(ranged_colors)

figures = {
    'circle': 0,
    'rectangle': 0
}

figures_colors = {
    'circle': {},
    'rectangle': {}
}

for region in regionprops(labeled):
    bb = region.bbox
    figure = ''
    if region.extent == 1:
        figure = 'rectangle'
    else:
        figure = 'circle'
    region_color = np.max(image[bb[0]:bb[2], bb[1]:bb[3]])
    ret_color = min(ranged_colors, key=lambda x: abs(region_color - x))
    if ret_color not in figures_colors[figure].keys():
        figures_colors[figure][ret_color] = 1
    else:
        figures_colors[figure][ret_color] += 1
    figures[figure] += 1

print("Figures: ", figures)
print("Figures by colors: ", figures_colors)

plt.figure()
plt.imshow(image, cmap="gray")
plt.show()
