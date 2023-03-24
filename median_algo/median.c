#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUM_DETECTORS 2
#define BUFFER_SIZE 3
#define DIMENSIONS 2

float fetchCameraData(int i) {
    return (float)(rand() % 1000);
}

struct CameraInterface {
    float buf[NUM_DETECTORS][BUFFER_SIZE][DIMENSIONS];
    int buf_idx;
};

void update(struct CameraInterface* cam) {
    for (int i = 0; i < NUM_DETECTORS; i++) {
        cam->buf[i][cam->buf_idx][0] = fetchCameraData(i);
        cam->buf[i][cam->buf_idx][1] = fetchCameraData(i);
    }
    cam->buf_idx = (cam->buf_idx + 1) % BUFFER_SIZE;
}

void getMedian(struct CameraInterface* cam, float* median) {
    for (int i = 0; i < NUM_DETECTORS; i++) {
        for (int j = 0; j < DIMENSIONS; j++) {
            float values[BUFFER_SIZE];
            for (int k = 0; k < BUFFER_SIZE; k++) {
                values[k] = cam->buf[i][k][j];
            }
            float temp;
            for (int k = 0; k < BUFFER_SIZE; k++) {
                for (int l = k + 1; l < BUFFER_SIZE; l++) {
                    if (values[k] > values[l]) {
                        temp = values[k];
                        values[k] = values[l];
                        values[l] = temp;
                    }
                }
            }
            if (BUFFER_SIZE % 2 == 0) {
                median[i * DIMENSIONS + j] = (values[BUFFER_SIZE/2] + values[BUFFER_SIZE/2 - 1]) / 2;
            } else {
                median[i * DIMENSIONS + j] = values[BUFFER_SIZE/2];
            }
        }
    }
}

int main() {
    srand(time(NULL));
    struct CameraInterface camera_interface;
    camera_interface.buf_idx = 0;
    for (int i = 0; i < BUFFER_SIZE; i++) {
        update(&camera_interface);
    }
    printf("Buffer:\n");
    for (int i = 0; i < NUM_DETECTORS; i++) {
        for (int j = 0; j < BUFFER_SIZE; j++) {
            printf("%f %f\n", camera_interface.buf[i][j][0], camera_interface.buf[i][j][1]);
        }
    }
    float median[NUM_DETECTORS * DIMENSIONS];
    getMedian(&camera_interface, median);
    printf("Median:\n");
    for (int i = 0; i < NUM_DETECTORS; i++) {
        for (int j = 0; j < DIMENSIONS; j++) {
            printf("%f ", median[i * DIMENSIONS + j]);
        }
        printf("\n");
    }
    return 0;
} 
