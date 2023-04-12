import cv2
import mediapipe as mp
import numpy as np
import json
import time
import argparse
import math
import random
import asyncio
import json
import websockets


def get_stick_figure_lines(landmarks, frame: np.ndarray) -> list:
    connections = [(12, 11), (11, 23), (24, 23), (24, 12), (24, 26), (26, 28), (23, 25), (25, 27), (28, 32), (32, 30), (28, 30), (27, 31), (29, 31), (27, 29), (14, 12), (14, 16), (11, 13),
                   (13, 15), (8, 6), (3, 7), (10, 9), (6, 5), (5, 4), (4, 0), (3, 2), (2, 1), (1, 0), (16, 18), (18, 20), (20, 16), (16, 22), (15, 21), (15, 19), (19, 17), (17, 15), (12, 23), (11, 24)]
    lines = []
    # TODO: fix jank try except
    try:
        for connection in connections:
            x1 = int(landmarks.landmark[connection[0]].x * frame.shape[1])
            y1 = int(landmarks.landmark[connection[0]].y * frame.shape[0])
            x2 = int(landmarks.landmark[connection[1]].x * frame.shape[1])
            y2 = int(landmarks.landmark[connection[1]].y * frame.shape[0])
            lines.append((x1, y1, x2, y2))
    except:
        for connection in connections:
            x1 = landmarks[connection[0]][0]
            y1 = landmarks[connection[0]][1]
            x2 = landmarks[connection[1]][0]
            y2 = landmarks[connection[1]][1]
            lines.append((x1, y1, x2, y2))
    return lines


def create_stick_figure(landmarks: mp.solutions.pose.Pose, frame: np.ndarray, color: tuple = (0, 255, 0)) -> np.ndarray:
    """
    returns the stick figure line set
    saves the the last 10 line-sets in fileName if save_lines is True
    currently using this save lines feature is deprecated by `save_points`, which records all the points rather than lines
    """
    stick_figure = np.zeros_like(frame)
    lines = get_stick_figure_lines(landmarks, frame)
    for line in lines:
        cv2.line(stick_figure, line[0:2], line[2:4], color, 2)
    return stick_figure


def blend_images(frame: np.ndarray, stick_figure: np.ndarray, alpha=0.5) -> np.ndarray:
    blended = cv2.addWeighted(frame, alpha, stick_figure, 1 - alpha, 0)
    return blended

global_landmarks = None
def record_poses(fileName: str = None) -> None:
    global global_landmarks

    mp_pose = mp.solutions.pose.Pose()
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose = mp_pose.process(image=rgb)
        landmarks = pose.pose_landmarks
        if landmarks is not None:
            global_landmarks = landmarks
            stick_figure = create_stick_figure(landmarks, frame)
            if time.time() - record_poses.last_save_time > 3:
                record_poses.last_save_time = time.time()
                # save lines and make the imshow flash white
                flash_screen('Stick Figure', frame)
            blended = blend_images(frame, stick_figure)
            # mirror image horizontally
            blended = cv2.flip(blended, 1)
            cv2.imshow('Stick Figure', blended)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


record_poses.last_save_time = 0


def flash_screen(cv2_window_name: str, frame: np.ndarray, num_frames_keep_flash: int = 10) -> None:
    rainbow = np.zeros_like(frame)
    m, n = rainbow.shape[0], rainbow.shape[1]
    for i in range(m):
        for j in range(n):
            rainbow[i, j] = [i % 255, j % 255, (i + j) % 255]
    for _ in range(num_frames_keep_flash):
        cv2.imshow(cv2_window_name, rainbow)
        cv2.waitKey(1)
    return

from threading import Thread

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Record and playback poses')
    parser.add_argument('-i', '--ip', type=str,
                        default='127.0.0.1', help='ip address')
    args = parser.parse_args()

    async def handle_message(message, websocket):
        # get text before first comma as cmd
        cmd = message.split(',')[0]
        data = message.split(',')[1:]
        if cmd == 'id':
            print(f"id", data)
        elif cmd == 'cap':
            print(f"cap")            
            if global_landmarks is None:
                await websocket.send(json.dumps({"median": [[319, 240], [122, 240], [36, 34], [34, 56], [27, 53], [68, 46], [69, 37], [19, 56]], "devId": 6, "medianLen": 8, "poseId": 3, "command": "poseData"}))
            else: 
                chest = [max(0, int(640 - global_landmarks.landmark[11].x * 640)), max(0, int(global_landmarks.landmark[11].y * 480))]
                leftArm = [max(0, int(640 - global_landmarks.landmark[15].x * 640)), max(0, int(global_landmarks.landmark[15].y * 480))]
                rightArm = [max(0, int(640 - global_landmarks.landmark[16].x * 640)), max(0, int(global_landmarks.landmark[16].y * 480))]
                pelvis = chest
                leftLeg = [max(0, int(640 - global_landmarks.landmark[27].x * 640)), max(0, int(global_landmarks.landmark[27].y * 480))]
                rightLeg = [max(0, int(640 - global_landmarks.landmark[28].x * 640)), max(0, int(global_landmarks.landmark[28].y * 480))]

                await websocket.send(json.dumps({"median": [chest, leftArm, rightArm, pelvis, leftLeg, rightLeg], "devId": 6, "medianLen": 8, "poseId": data, "command": "poseData"}))
                print(json.dumps({"median": [chest, leftArm, rightArm, pelvis, leftLeg, rightLeg], "devId": 6, "medianLen": 8, "poseId": data, "command": "poseData"}))

    async def main():
        global global_landmarks

        uri = 'ws://192.168.0.194:8080'
        async with websockets.connect(uri) as websocket:
            print(f"Connected to WebSocket server at {uri}")
            await websocket.send(json.dumps({
                "command": "setType",
                "identifier": "camera"
            }))
            while True:
                message = await websocket.recv()
                await handle_message(message, websocket)

    thread = Thread(target=record_poses)
    thread.start()
    asyncio.run(main())

    while True: 
        if global_landmarks is not None: 
            chest = [max(0, int(640 - global_landmarks.landmark[11].x * 640)), max(0, int(global_landmarks.landmark[11].y * 480))]
            leftArm = [max(0, int(640 - global_landmarks.landmark[15].x * 640)), max(0, int(global_landmarks.landmark[15].y * 480))]
            rightArm = [max(0, int(640 - global_landmarks.landmark[16].x * 640)), max(0, int(global_landmarks.landmark[16].y * 480))]
            pelvis = chest
            leftLeg = [max(0, int(640 - global_landmarks.landmark[27].x * 640)), max(0, int(global_landmarks.landmark[27].y * 480))]
            rightLeg = [max(0, int(640 - global_landmarks.landmark[28].x * 640)), max(0, int(global_landmarks.landmark[28].y * 480))]

            print(json.dumps({"median": [chest, leftArm, rightArm, pelvis, leftLeg, rightLeg], "devId": 6, "medianLen": 8, "poseId": 69, "command": "poseData"}))
