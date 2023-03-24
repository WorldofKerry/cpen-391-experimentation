void rgb_to_hsv(unsigned char r, unsigned char g, unsigned char b, float* h, float* s, float* v) {
    float red = r / 255.0;
    float green = g / 255.0;
    float blue = b / 255.0;

    float cmax = fmaxf(red, fmaxf(green, blue));
    float cmin = fminf(red, fminf(green, blue));
    float delta = cmax - cmin;

    if (delta == 0) {
        *h = 0;
    } else if (cmax == red) {
        *h = fmodf((green - blue) / delta, 6);
    } else if (cmax == green) {
        *h = (blue - red) / delta + 2;
    } else {
        *h = (red - green) / delta + 4;
    }
    *h *= 60;

    if (cmax == 0) {
        *s = 0;
    } else {
        *s = delta / cmax;
    }

    *v = cmax;
}