import numpy as np

NUM_DETECTORS = 2
BUFFER_SIZE = 2
DIMENSIONS = 2

def fetchCameraData(i: int) -> np.ndarray:
    return np.random.rand(2) * 1000

class CameraInterface: 
    def __init__(self): 
        self.buf = np.zeros((NUM_DETECTORS, BUFFER_SIZE, DIMENSIONS))
        self.buf_idx = 0
    
    def update(self) -> None:
        for i in range(NUM_DETECTORS):
            self.buf[i, self.buf_idx] = fetchCameraData(i)
        self.buf_idx = (self.buf_idx + 1) % BUFFER_SIZE

    def getMedian(self) -> np.ndarray:
        return np.median(self.buf, axis=1)

camera_interface = CameraInterface()
for _ in range(BUFFER_SIZE): 
    camera_interface.update()

print(camera_interface.buf)
print(camera_interface.getMedian())