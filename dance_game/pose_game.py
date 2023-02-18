import cv2
import mediapipe as mp
import numpy as np
import json
import time
import argparse
import math
import random

def get_stick_figure_lines(landmarks, frame: np.ndarray) -> list:
    connections = [(12, 11), (11, 23), (24, 23), (24, 12), (24, 26), (26, 28), (23, 25), (25, 27), (28, 32), (32, 30), (28, 30), (27, 31), (29, 31), (27, 29), (14, 12), (14, 16), (11, 13), (13, 15), (8, 6), (3, 7), (10, 9), (6, 5), (5, 4), (4, 0), (3, 2), (2, 1), (1, 0), (16, 18), (18, 20), (20, 16), (16, 22), (15, 21), (15, 19), (19, 17), (17, 15), (12, 23), (11, 24)]
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

def save_points(landmarks: mp.solutions.pose.Pose, frame: np.ndarray, fileName: str, period: float = 3, save_this_many_point_sets: int = 8) -> None:
    if time.time() - save_points.last_save_time > period:
        save_points.last_save_time = time.time()
        points = []
        for i in range(len(landmarks.landmark)):
            x = int(landmarks.landmark[i].x * frame.shape[1])
            y = int(landmarks.landmark[i].y * frame.shape[0])
            points.append((x, y))
        if len(save_points.last_points) > save_this_many_point_sets: 
            save_points.last_points.pop(0)
        save_points.last_points.append(points)
        with open(fileName, 'w') as outfile:
            json.dump(save_points.last_points, outfile)
save_points.last_save_time = 0
save_points.last_points = []

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

def record_poses(fileName: str = None) -> None:
    mp_pose = mp.solutions.pose.Pose()
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose = mp_pose.process(image=rgb)
        landmarks = pose.pose_landmarks
        if landmarks is not None:
            stick_figure = create_stick_figure(landmarks, frame)
            if time.time() - record_poses.last_save_time > 3:
                record_poses.last_save_time = time.time()
                # save lines and make the imshow flash white
                save_points(landmarks, frame, fileName)
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

def get_score(landmarks1: mp.solutions.pose.Pose, landmarks2: list, frame: np.ndarray) -> float:  
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
        x1 = int(landmarks1.landmark[index].x * frame.shape[1])
        y1 = int(landmarks1.landmark[index].y * frame.shape[0])
        x2 = landmarks2[index][0]
        y2 = landmarks2[index][1]
        score += math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    # make score so that higher the better
    score = 1 / score * 100000
    return score

def flash_screen(cv2_window_name: str, frame: np.ndarray, num_frames_keep_flash: int = 5) -> None:
    rainbow = np.zeros_like(frame)
    m, n = rainbow.shape[0], rainbow.shape[1]
    for i in range(m):
        for j in range(n):
            rainbow[i, j] = [i % 255, j % 255, (i + j) % 255]
    for _ in range(num_frames_keep_flash):
        cv2.imshow(cv2_window_name, rainbow)
        cv2.waitKey(1)
    return

def playback_poses(fileName: str = None) -> None:
    """
    displays the current webcam, 
    overlayed are the poses in the file in green, going to the next pose every 5 seconds, 
    overlayed is the current poses in red. 
    """
    mp_pose = mp.solutions.pose.Pose()
    print("DEBUG: loaded mp_pose")
    cap = cv2.VideoCapture(0)
    print("DEBUG: loaded cap")
    with open(fileName) as json_file:
        points_list = json.load(json_file)
    print("DEBUG: loaded points_list with length", len(points_list))
    last_draw_time = time.time()
    points = points_list.pop(0)
    score = -1
    score_location = (10, 30)
    score_rotation = 0
    score_color = (0, 255, 0)
    print("DEBUG: initialized variables")
    while True:
        _, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose = mp_pose.process(image=rgb)
        landmarks = pose.pose_landmarks
        if time.time() - last_draw_time > 5:
            if points_list: 
                points = points_list.pop(0)
                flash_screen('Stick Figure', frame)
                last_draw_time = time.time()
                if landmarks and landmarks.landmark and points: 
                    score = get_score(landmarks, points, frame)
                score_location = (random.randint(50, frame.shape[1] - 50), random.randint(100, frame.shape[0] - 100))
                score_rotation = random.randint(-35, 35)
                score_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            else: 
                if time.time() - last_draw_time > 10: 
                    break
        if landmarks is not None:
            stick_figure_realtime = create_stick_figure(landmarks, frame)
        else: 
            stick_figure_realtime = np.zeros_like(frame)
        stick_figures = stick_figure_realtime
        if points is not None:
            stick_figure_recorded = create_stick_figure(points, frame, color=(255, 0, 0))
            stick_figures = cv2.add(stick_figures, stick_figure_recorded)
        blended = blend_images(frame, stick_figures)
        # mirror image horizontally
        blended = cv2.flip(blended, 1)
        if score >= 0: 
            # put rotated score at location whose size scales with the score
            score_frame = np.zeros_like(blended)
            cv2.putText(score_frame, str(int(score)), score_location, cv2.FONT_HERSHEY_SIMPLEX, 4, score_color, 5, cv2.LINE_AA)
            M = cv2.getRotationMatrix2D(score_location, score_rotation, 1)
            score_frame = cv2.warpAffine(score_frame, M, (score_frame.shape[1], score_frame.shape[0]))
            blended = cv2.add(blended, score_frame)
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