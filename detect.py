import cv2
import os
import time
import numpy as np
import random

def detect_object(img, cascade: cv2.CascadeClassifier)->tuple:
    """
    Detect objects in the input image using the provided cascade classifier.
    returns a list of (x, y, w, h) tuples representing the detected objects' bounding boxes.
    """
    frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)
    faces = cascade.detectMultiScale(frame_gray, 1.3, 5)
    return faces

def detect_faces(img)->tuple:
    """
    Detect faces in the input image.

    :param img: Input image.
    :return: list of (x, y, w, h) tuples representing the detected faces' bounding boxes.
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = detect_object(img, face_cascade)
    return faces

def display_faces(img, faces):
    for (x, y, w, h) in faces:
        # color format: BGR
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2) 
        cv2.putText(img, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
    return img

def is_face_moving(prev_position, curr_position, threshold=10):
    """
    Check if the face has moved significantly between frames.
    
    :param previous_position: Tuple (x, y, w, h) of the previous face position.
    :param current_position: Tuple (x, y, w, h) of the current face position.
    :param threshold: Distance threshold to determine significant movement.
    :return: Boolean indicating if the face has moved.
    """
    prev_x, prev_y, _, _ = prev_position
    curr_x, curr_y, _, _ = curr_position
    
    distance = ((prev_x - curr_x) ** 2 + (prev_y - curr_y) ** 2) ** 0.5
    return distance > threshold

def get_main_face(faces):
    """
    Get the largest face from the detected faces.
    
    :param faces: List of tuples (x, y, w, h) for each detected face.
    :return: Tuple (x, y, w, h) of the largest face.
    """
    if len(faces) == 0:
        return None
    
    # Find the largest face based on the area (width * height)
    main_face = max(faces, key=lambda face: face[2] * face[3])
    return main_face

def is_close_enough(img, face, threshold_percentage=0.18):
    """
    Check if the face is close enough to the camera.

    :param img: Input image.
    :param face: Tuple (x, y, w, h) of the face position.
    :param threshold_percentage: Percentage of the image dimensions to consider as close enough. (0 to 1)
    :return: Boolean indicating if the face is close enough.
    """

    _, _, w, h = face
    img_h, img_w, _ = img.shape
    return w > img_w * threshold_percentage and h > img_h * threshold_percentage
     

def main(output_dir='captured_photos', num_photos=10):

    # Directory to save the captured photos
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    photo_count = 0
    stationary_frames = 0
    prev_face = None
    delay_since = lambda d : time.time() - d

    # Open the camera
    last_photo_time = time.time()
    cap = cv2.VideoCapture(0)
    print(f"delay: {delay_since(last_photo_time)} seconds")

    # Check if the camera is opened correctly
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    while photo_count < num_photos:

        # Capture frame-by-frame
        _, frame = cap.read()

        # Detect faces in the image
        faces = detect_faces(frame)
        face = get_main_face(faces)

        # If a face is detected, check if it is moving
        if face is not None and prev_face is not None:
            if not is_face_moving(prev_face, face) and is_close_enough(frame, face):
                stationary_frames += 1
                if stationary_frames >= 5 and delay_since(last_photo_time) > 2:
                    photo_path = os.path.join(output_dir, f'user_{photo_count:04d}.jpg')
                    
                    cv2.imwrite(photo_path, frame)
                    last_photo_time = time.time()
                    print(f"Photo saved: {photo_path}")
                    photo_count += 1
            else:
                stationary_frames = 0

        # Display the resulting frame
        cv2.imshow('Frame', display_faces(frame, faces))
        prev_face = face

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

main()