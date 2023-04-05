# convert RGB to YCbCr
def convert_rgb_to_cycbcr(r: int, g: int, b: int) -> tuple[int, int, int]:
    y = 16 + + (((65.738 * r) + (129.057 * g) + (25.064 * b)) / 256)
    cb = 128 + (((-37.945 * r) - (74.494 * g) + (112.439 * b)) / 256)
    cr = 128 + (((112.439 * r) - (94.154 * g) - (18.285 * b)) / 256)
    return y, cb, cr

def convert_rgb_to_hsv(r: int, g: int, b: int) -> tuple[int, int, int]:    
    # Find maximum and minimum values of RGB components
    # cmax, cmin = max(r, g, b), min(r, g, b)
    # delta = cmax - cmin
    # if delta == 0:
    #     hue = 0
    # elif cmax == r:
    #     hue = ((g - b) * 60) // delta
    # elif cmax == g:
    #     hue = ((b - r) * 60) // delta + 120
    # else:
    #     hue = ((r - g) * 60) // delta + 240

    cmax, cmin = max(r, g, b), min(r, g, b)
    delta = cmax - cmin
    if delta == 0:
        hue = 0
    elif cmax == r:
        hue = g - b
    elif cmax == g: 
        hue = b - r
    else: 
        hue = r - g

    return hue, cmax, cmin

import random
import colorsys
import numpy as np

if __name__ == "__main__":
    n = 10
    r = [random.randint(0, 255) for _ in range(n)]
    g = [random.randint(0, 255) for _ in range(n)]
    b = [random.randint(0, 255) for _ in range(n)]

    # print as verilog array format
    print("  logic [7:0] r_in [0:%d] = '{" % (n-1), end='')
    for i in range(n):
        print("{:02d}".format(r[i]), end="")
        if i != n - 1:
            print(", ", end="")
    print("};\n", end="")
    print("  logic [7:0] g_in [0:%d] = '{" % (n-1), end='')
    for i in range(n):
        print("{:02d}".format(g[i]), end="")
        if i != n - 1:
            print(", ", end="")
    print("};\n", end="")
    print("  logic [7:0] b_in [0:%d] = '{" % (n-1), end='')
    for i in range(n):
        print("{:02d}".format(b[i]), end="")
        if i != n - 1:
            print(", ", end="")
    print("};\n", end="")

    for i in range(n):
        x, y, z = convert_rgb_to_hsv(r[i], g[i], b[i])
        x1, y1, z1 = colorsys.rgb_to_hsv(r[i]/255.0, g[i]/255.0, b[i]/255.0)
        print("%d,%d,%d correct: %d,%d,%d, mine: %d,%d,%d" % (r[i], g[i], b[i], x1*360, y1*100, z1*100, x, y, z))

    