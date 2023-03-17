# convert RGB to YCbCr
def convert_rgb_to_cycbcr(r: int, g: int, b: int) -> tuple[int, int, int]:
    y = 16 + + (((65.738 * r) + (129.057 * g) + (25.064 * b)) / 256)
    cb = 128 + (((-37.945 * r) - (74.494 * g) + (112.439 * b)) / 256)
    cr = 128 + (((112.439 * r) - (94.154 * g) - (18.285 * b)) / 256)
    return (y, cb, cr)

# logic [7:0] r_in [0:7] = '{64, 128, 192, 255, 0, 128, 0, 255};
# logic [7:0] g_in [0:7] = '{0, 64, 128, 192, 128, 0, 255, 128};
# logic [7:0] b_in [0:7] = '{128, 192, 255, 0, 128, 255, 128, 0};

r_in = [64, 128, 192, 255, 0, 128, 0, 255]
g_in = [0, 64, 128, 192, 128, 0, 255, 128]
b_in = [128, 192, 255, 0, 128, 255, 128, 0]

for i in range(8):
    y, cb, cr = convert_rgb_to_cycbcr(r_in[i], g_in[i], b_in[i])
    # truncate to 8 bits
    y = int(y) & 0xFF
    cb = int(cb) & 0xFF
    cr = int(cr) & 0xFF
    print("%d,%d,%d %d,%d,%d" % (r_in[i], g_in[i], b_in[i], y, cb, cr))