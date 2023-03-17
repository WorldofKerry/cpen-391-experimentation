# convert RGB to YCbCr
def convert_rgb_to_cycbcr(r: int, g: int, b: int) -> tuple[int, int, int]:
    y = 16 + + (((65.738 * r) + (129.057 * g) + (25.064 * b)) / 256)
    cb = 128 + (((-37.945 * r) - (74.494 * g) + (112.439 * b)) / 256)
    cr = 128 + (((112.439 * r) - (94.154 * g) - (18.285 * b)) / 256)
    return (y, cb, cr)

if __name__ == "__main__":
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

    # lawngreen 	#7CFC00 	rgb(124,252,0)
    # chartreuse 	#7FFF00 	rgb(127,255,0)
    # limegreen 	#32CD32 	rgb(50,205,50)
    # lime 	#00FF00 	rgb(0,255,0)
    # forestgreen 	#228B22 	rgb(34,139,34)
    # green 	#008000 	rgb(0,128,0)
    # darkgreen 	#006400 	rgb(0,100,0)
    # greenyellow 	#ADFF2F 	rgb(173,255,47)
    # yellowgreen 	#9ACD32 	rgb(154,205,50)
    # springgreen 	#00FF7F 	rgb(0,255,127)
    # mediumspringgreen 	#00FA9A 	rgb(0,250,154)
    # lightgreen 	#90EE90 	rgb(144,238,144)
    # palegreen 	#98FB98 	rgb(152,251,152)
    # darkseagreen 	#8FBC8F 	rgb(143,188,143)
    # mediumseagreen 	#3CB371 	rgb(60,179,113)
    # lightseagreen 	#20B2AA 	rgb(32,178,170)
    # seagreen 	#2E8B57 	rgb(46,139,87)
    # olive 	#808000 	rgb(128,128,0)
    # darkolivegreen 	#556B2F 	rgb(85,107,47)
    # olivedrab 	#6B8E23 	rgb(107,142,35)

    r_in = [124, 127, 50, 0, 34, 0, 0, 173, 154, 0, 0, 144, 152, 143, 60, 32, 46, 128, 85, 107]
    g_in = [252, 255, 205, 255, 139, 128, 100, 255, 205, 255, 250, 238, 251, 188, 179, 178, 139, 128, 107, 142]
    b_in = [0, 0, 50, 0, 34, 0, 0, 47, 50, 127, 154, 144, 152, 143, 113, 170, 87, 0, 47, 35]

    print()
    for i in range(20):
        y, cb, cr = convert_rgb_to_cycbcr(r_in[i], g_in[i], b_in[i])
        # truncate to 8 bits
        y = int(y) & 0xFF
        cb = int(cb) & 0xFF
        cr = int(cr) & 0xFF
        print("%d,%d,%d" % (y, cb, cr))