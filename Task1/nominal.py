import numpy as np
from io import StringIO

filename = input('Enter filename: ')
real_width = 0
image = []

with open(filename, 'r') as file_input:
    real_width = float(file_input.readline())
    file_input.readline()
    data = StringIO(file_input.read())
    image = np.loadtxt(data)

obj = np.sum(image, 1)
if obj.max() == 0:
    print('There is no object')
else:
    print(real_width / obj.max())