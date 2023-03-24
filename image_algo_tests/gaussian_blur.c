#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int clamp(int x, int lo, int hi) {
    return x < lo ? lo : (x > hi ? hi : x);
}

void gaussian_blur(unsigned char img[800][640][3], int w, int h, float sigma) {
    int r = ceil(3 * sigma);
    int ksize = 2 * r + 1;
    float* kernel = (float*)malloc(ksize * sizeof(float));
    float s = 0;
    for (int i = 0; i < ksize; i++) {
        kernel[i] = exp(-(i - r) * (i - r) / (2 * sigma * sigma));
        s += kernel[i];
    }
    for (int i = 0; i < ksize; i++) {
        kernel[i] /= s;
    }
    unsigned char tmp[800][640][3];
    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
            for (int ch = 0; ch < 3; ch++) {
                float val = 0;
                for (int i = -r; i <= r; i++) {
                    int xi = clamp(x + i, 0, w - 1);
                    int ki = i + r;
                    val += kernel[ki] * img[xi][y][ch];
                }
                tmp[x][y][ch] = (unsigned char)round(val);
            }
        }
    }
    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
            for (int ch = 0; ch < 3; ch++) {
                img[x][y][ch] = tmp[x][y][ch];
            }
        }
    }
    free(kernel);
}

int main() {
    // Read input file
    FILE* fp = fopen("input.txt", "r");
    unsigned char img[800][640][3];
    for (int y = 0; y < 640; y++) {
        for (int x = 0; x < 800; x++) {
            for (int ch = 0; ch < 3; ch++) {
                int val;
                fscanf(fp, "%d", &val);
                img[x][y][ch] = (unsigned char)val;
            }
        }
    }
    fclose(fp);

    // Perform Gaussian blur
    gaussian_blur(img, 800, 640, 1.5);

    // Write output file
    fp = fopen("output.txt", "w");
    for (int y = 0; y < 640; y++) {
        for (int x = 0; x < 800; x++) {
            for (int ch = 0; ch < 3; ch++) {
                fprintf(fp, "%d ", img[x][y][ch]);
            }
            fprintf(fp, "\n");
        }
    }
    fclose(fp);

    return 0;
}