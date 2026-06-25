import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='google.protobuf.symbol_database')
import cv2
import numpy as np
import mediapipe as mp
import math
import time
from SocketConn.Socketconn import next_lock, zoom, rotate_left, rotate_right, rotate_up, rotate_down, sock
import subprocess
from subprocess import Popen

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def calculate_distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def is_finger_up(landmarks, tip_id, pip_id):
    return landmarks.landmark[tip_id].y < landmarks.landmark[pip_id].y

def detect_strict_gesture(landmarks, hand_size_reference):
    thumb_tip = landmarks.landmark[4]
    index_tip = landmarks.landmark[8]
    distance = calculate_distance(thumb_tip, index_tip)
    normalized_distance = distance / hand_size_reference

    index_up = is_finger_up(landmarks, 8, 6)
    middle_up = is_finger_up(landmarks, 12, 10)
    ring_up = is_finger_up(landmarks, 16, 14)
    pinky_up = is_finger_up(landmarks, 20, 18)
    thumb_up = is_finger_up(landmarks, 4, 3)

    fingers_up = [index_up, middle_up, ring_up, pinky_up]

    if normalized_distance < 0.1 and index_up and not any(fingers_up[1:]):
        return "select"
    if index_up and thumb_up and normalized_distance > 0.65 and not any(fingers_up[1:]):
        return "zoom_in"
    if normalized_distance < 0.4 and not any(fingers_up[1:]):
        return "zoom_out"
    if index_up and not any(fingers_up[1:]):
        return "move"

    return None

def run_image_interaction():
    
    time.sleep(3)

    last_gesture = None
    gesture_time = time.time()
    debounce_duration = 0.5
    selection_made = False

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


    if not cap.isOpened():
        print("Error: Webcam not accessible")
        return

    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=1) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            gesture = None

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    hand_size_reference = calculate_distance(hand_landmarks.landmark[0], hand_landmarks.landmark[8])
                    current_gesture = detect_strict_gesture(hand_landmarks, hand_size_reference)

                    if current_gesture == last_gesture:
                        if time.time() - gesture_time > debounce_duration:
                            gesture = current_gesture
                    else:
                        gesture_time = time.time()
                        last_gesture = current_gesture

                    if gesture == "select":
                        selection_made = True
                        cv2.putText(frame, "SELECTED! Gestures enabled.", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                        next_lock(sock)
                        time.sleep(1) 
                        

                    elif selection_made:
                        if gesture == "zoom_in":
                            
                            zoom(sock,1)

                        elif gesture == "zoom_out":
                            
                            zoom(sock,-1)

                        elif gesture == "move":
                        
                            index_tip = hand_landmarks.landmark[8]
                            x, y = index_tip.x, index_tip.y
                        
                            
                            MARGIN = 0.2
                            CENTER_X = 0.5
                            CENTER_Y = 0.5
                            MARGIN_Y = 0.08
                        
                            
                            if x < CENTER_X - MARGIN:
                                rotate_left(sock)
                                
                            elif x > CENTER_X + MARGIN:
                                rotate_right(sock)
                                
                        
                            if y < CENTER_Y - MARGIN_Y:
                                rotate_up(sock)
                            elif y > CENTER_Y + MARGIN_Y:
                                rotate_down(sock)
                                           
            else:
                last_gesture = None

            output = frame.copy()

            if gesture:
                cv2.putText(output, f"Gesture: {gesture}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Image Interaction", output)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
