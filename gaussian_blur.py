import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import time

def process_image(img: list) -> list:
    """
    Input: 3D list of pixels in RGB 0-255 format, where it's [channel][row][col]
    Output: 3D list of pixels in RGB 0-255 format, where it's [channel][row][col]
    """
    start_time = time.time()
    channels, rows, cols = len(img), len(img[0]), len(img[0][0])

    output = [[[0 for _ in range(cols)] for _ in range(rows)] for _ in range(channels)]

    # gaussian blur
    for c in range(channels):
        output[c] = gaussian_blur_2d(img[c], 3) # modify sigma here

    print("process_image took %s seconds" % (time.time() - start_time))
    return output


def gaussian_blur_2d(img: list, sigma: int) -> list:
    """
    Gaussian blur with only python lists
    """
    start_time = time.time()

    euler = 2.7182818284590452353602874713527
    kernel = []
    kernel_size = 4 * sigma + 1
    center = kernel_size // 2
    for i in range(kernel_size):
        row = []
        for j in range(kernel_size):
            x = i - center
            y = j - center
            if sigma == 0:
                row.append(1)
            else:
                row.append((1 / (2 * math.pi * sigma**2)) * euler**(-(x**2 + y**2) / (2 * sigma**2)))
        kernel.append(row)

    img = convolution_2d(img, kernel)

    print("gaussian_blur_2d took %s seconds" % (time.time() - start_time))
    return img


def convolution_2d(img: list, kernel: list) -> list:
    """
    2D convolution with only python lists
    """
    start_time = time.time()

    image_height = len(img)
    image_width = len(img[0])
    kernel_height = len(kernel)
    kernel_width = len(kernel[0])
    kernel_center = kernel_height // 2
    output = [[0 for _ in range(image_width - kernel_width + 1)] for _ in range(image_height - kernel_height + 1)]
    kernel_sum = sum(map(sum, kernel))

    for i in range(image_height - kernel_height + 1):
        for j in range(image_width - kernel_width + 1):
            for m in range(kernel_height):
                for n in range(kernel_width):
                    ii = i + m - kernel_center
                    jj = j + n - kernel_center
                    output[i][j] += img[ii][jj] * kernel[m][n]
    for i in range(len(output)):
        for j in range(len(output[0])):
            output[i][j] /= kernel_sum

    print("convolution_2d took %s seconds" % (time.time() - start_time))
    return output


def main():
    """
    Wrapper function for converting from file to list and back to matplotlib display
    Uses library functions to read and display image
    """
    img_np = cv2.imread('scene1.jpg')
    img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    
    # resize image to max_size on either side by blurring then resizing
    max_size = 300
    if img_np.shape[0] > max_size or img_np.shape[1] > max_size:
        if img_np.shape[0] > img_np.shape[1]:
            img_np = cv2.resize(img_np, (max_size, int(img_np.shape[0] * max_size / img_np.shape[1])))
        else:
            img_np = cv2.resize(img_np, (int(img_np.shape[1] * max_size / img_np.shape[0]), max_size))

    # convert to python list
    img_np = np.transpose(img_np, (2, 0, 1))
    img = img_np.tolist()

    # process image
    img = process_image(img)

    # display image
    img_np = np.transpose(img, (1, 2, 0))
    img_np = np.array(img_np).astype(np.uint8)
    plt.subplot(1, 1, 1)
    plt.imshow(img_np)
    plt.show()


if __name__ == '__main__':
    main()