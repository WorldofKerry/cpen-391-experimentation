import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

def process_image(img: list) -> list:
    channels, rows, cols = len(img), len(img[0]), len(img[0][0])

    output = [[[0 for _ in range(cols)] for _ in range(rows)] for _ in range(channels)]

    # gaussian blur
    for c in range(channels):
        output[c] = gaussian_blur(img[c], 7, 7)

    return output


def gaussian_blur(img: list, kernel_size: int, sigma: int) -> list:
    kernel = []
    center = kernel_size // 2
    for i in range(kernel_size):
        row = []
        for j in range(kernel_size):
            x = i - center
            y = j - center
            row.append(math.exp(-(x**2 + y**2) / (2 * sigma**2)))
        kernel.append(row)
            
    # display kernel scaled to 0-255
    plt.subplot(1, 2, 1)
    plt.imshow(np.array(kernel) * 255, cmap='gray')

    return img


def convolution(img: list, kernel: list) -> list:
    rows, cols = len(img), len(img[0])
    kernel_size = len(kernel)

    output = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            for k in range(kernel_size):
                for l in range(kernel_size):
                    if i + k - kernel_size // 2 < 0 or i + k - kernel_size // 2 >= rows or j + l - kernel_size // 2 < 0 or j + l - kernel_size // 2 >= cols:
                        continue
                    output[i][j] += img[i + k - kernel_size // 2][j + l - kernel_size // 2] * kernel[k][l]

    return output


def main():
    img_np = cv2.imread('scene1.jpg')
    img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    
    # resize image to max_size on either side
    max_size = 300
    if img_np.shape[0] > max_size or img_np.shape[1] > max_size:
        scale = max_size / max(img_np.shape[0], img_np.shape[1])
        img_np = cv2.resize(img_np, (0, 0), fx=scale, fy=scale)

    # convert to python list
    img = img_np.tolist()

    # process image
    img = process_image(img)

    # display image
    img_np = np.array(img).astype(np.uint8)
    plt.subplot(1, 2, 2)
    plt.imshow(img_np)
    plt.show()

if __name__ == '__main__':
    main()