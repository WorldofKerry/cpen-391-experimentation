import cv2
import mediapipe as mp
import numpy as np
import json
import time
import argparse
import math

def get_stick_figure_lines(landmarks, frame): 
    connections = [(12, 11), (11, 23), (24, 23), (24, 12), (24, 26), (26, 28), (23, 25), (25, 27), (28, 32), (32, 30), (28, 30), (27, 31), (29, 31), (27, 29), (14, 12), (14, 16), (11, 13), (13, 15), (8, 6), (3, 7), (10, 9), (6, 5), (5, 4), (4, 0), (3, 2), (2, 1), (1, 0), (16, 18), (18, 20), (20, 16), (16, 22), (15, 21), (15, 19), (19, 17), (17, 15), (12, 23), (11, 24)]
    lines = []
    for connection in connections:
        x1 = int(landmarks[connection[0]].x * frame.shape[1])
        y1 = int(landmarks[connection[0]].y * frame.shape[0])
        x2 = int(landmarks[connection[1]].x * frame.shape[1])
        y2 = int(landmarks[connection[1]].y * frame.shape[0])
        lines.append((x1, y1, x2, y2))
    return lines

def save_points(landmarks, frame: np.ndarray, fileName: str, period: float = 3, save_this_many_point_sets: int = 5) -> None:
    if time.time() - save_points.last_save_time > period:
        save_points.last_save_time = time.time()
        points = []
        for index in range(len(landmarks)):
            x = int(landmarks[index].x * frame.shape[1])
            y = int(landmarks[index].y * frame.shape[0])
            points.append((x, y))
        if len(save_points.last_points) > save_this_many_point_sets: 
            save_points.last_points.pop(0)
        save_points.last_points.append(points)
        with open(fileName, 'w') as outfile:
            json.dump(save_points.last_points, outfile)
save_points.last_save_time = 0
save_points.last_points = []

def create_stick_figure(landmarks, frame: np.ndarray, save_lines: bool = False, fileName: str = None) -> np.ndarray:
    """
    returns the stick figure line set
    saves the the last 10 line-sets in fileName if save_lines is True
    currently using this save lines feature is deprecated by `save_points`, which records all the points rather than lines
    """
    stick_figure = np.zeros_like(frame)
    lines = get_stick_figure_lines(landmarks, frame)
    for line in lines:
        cv2.line(stick_figure, line[0:2], line[2:4], (0, 255, 0), 2)
    if save_lines: 
        if len(create_stick_figure.line_sets) > 10: # record last 10 line-sets
            create_stick_figure.line_sets.pop(0)
        create_stick_figure.line_sets.append(lines)
        with open(fileName, 'w') as outfile:
            json.dump(create_stick_figure.line_sets, outfile)
    return stick_figure
create_stick_figure.line_sets = []

def blend_images(frame: np.ndarray, stick_figure: np.ndarray, alpha=0.5) -> np.ndarray:
    blended = cv2.addWeighted(frame, alpha, stick_figure, 1 - alpha, 0)
    return blended

def record_poses(fileName: str = None) -> None:
    mp_pose = mp.solutions.pose.Pose()
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose = mp_pose.process(image=rgb)
        landmarks = pose.pose_landmarks.landmark if pose.pose_landmarks is not None else None
        if landmarks is not None:
            stick_figure = create_stick_figure(landmarks, frame)
            if time.time() - record_poses.last_save_time > 3:
                record_poses.last_save_time = time.time()
                # save lines and make the imshow flash white
                save_points(landmarks, frame, fileName)
                flash_screen('Stick Figure', frame, 5)
            blended = blend_images(frame, stick_figure)
            # mirror image horizontally
            blended = cv2.flip(blended, 1)
            cv2.imshow('Stick Figure', blended)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
record_poses.last_save_time = 0

def get_score(landmarks1: mp.solutions.pose.Pose, landmarks2: mp.solutions.pose.Pose) -> float:    
    major_indexes = [
        0, # nose
        16, # right wrist
        14, # right elbow
        12, # right shoulder
        11, # left shoulder
        13, # left elbow
        15, # left wrist
        24, # right hip
        26, # right knee
        28, # right ankle
        23, # left hip
        25, # left knee
        27, # left ankle
    ]
    score = 0
    for index in major_indexes:
        x1 = landmarks1.landmark[index].x
        y1 = landmarks1.landmark[index].y
        x2 = landmarks2.landmark[index].x
        y2 = landmarks2.landmark[index].y
        score += math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return score

def flash_screen(cv2_window_name: str, frame: np.ndarray, num_frames_keep_white: int) -> None:
    white = np.zeros_like(frame)
    white.fill(255)
    for _ in range(num_frames_keep_white): 
        cv2.imshow(cv2_window_name, white)
        cv2.waitKey(1)
    return

def playback_poses(fileName: str = None) -> None:
    """
    displays the current webcam, 
    overlayed are the poses in the file in green, going to the next pose every 5 seconds, 
    overlayed is the current poses in red. 
    """
    mp_pose = mp.solutions.pose.Pose()
    cap = cv2.VideoCapture(0)
    last_draw_time = 0
    with open(fileName) as json_file:
        points_list = json.load(json_file)
    while True:
        _, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose = mp_pose.process(image=rgb)
        landmarks = pose.pose_landmarks.landmark if pose.pose_landmarks is not None else None
        if time.time() - last_draw_time > 5:
            last_draw_time = time.time()
            if points_list: 
                points = points_list.pop(0)
                flash_screen('Stick Figure', frame, 5)
            else: 
                break
        if landmarks is not None:
            stick_figure_realtime = create_stick_figure(landmarks, frame)
        else: 
            stick_figure_realtime = np.zeros_like(frame)
        blended = blend_images(frame, stick_figure_realtime)
        if points is not None:
            stick_figure_recorded = create_stick_figure(points, frame)
            blended = blend_images(blended, stick_figure_recorded)
        # mirror image horizontally
        blended = cv2.flip(blended, 1)
        cv2.imshow('Stick Figure', blended)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Record and playback poses')
    parser.add_argument('-r', '--record', action='store_true', help='record poses')
    parser.add_argument('-p', '--playback', action='store_true', help='playback poses')
    args = parser.parse_args()

    if args.record:
        record_poses(fileName='lines.json')
    elif args.playback:
        playback_poses(fileName='lines.json')
    else:
        print('Please specify either record or playback')