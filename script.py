import mediapipe as mp
import numpy as np
import pyvirtualcam
import cv2
import keyboard
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
#%%
filter_type = "default" # default is no filter. 
default_color = (255,255,255) # white is default. 
poly_flash_speed = 6 # smaller values gives results in faster flashing.
smoothing_factor = 0.2  # Adjust this value for smoother or quicker updates of the head box.
line_thickness = 1
dot_thickness = 1
dot_radius = 1
width = 900
height = 700
#%% Other variables
time = 0
prev_face_position = None
prev_left = None
prev_right = None
prev_face_time = None
poly_color = (255,255,255)
#%%

#########################KEYBINDNINGS FOR FILTERS##############################
# STATIC BOX = 1
# FACE SCAN = 2
# STATIC MESH = 3
# POLYGRAPH EFFECT = 4
# EYE TRACK = 5
# NO FILTER = 0
# EXIT VIRTUAL CAM = q
#########################KEYBINDNINGS FOR FILTERS##############################

vid = cv2.VideoCapture(2) 
print(vid)
#########################VIDEOSTREAM INPUT OPTIONS#############################
# 0 = your actual webcamera - this is used for when you want to play around with the filters yourself, with the videostream from you acutal webcam as input.
# 2 = OBS-plugin virtual cam - used when you want the OBS-capture of participant as input to script. 0q
#########################VIDEOSTREAM INPUT OPTIONS#############################

vid.set(cv2.CAP_PROP_FRAME_HEIGHT,height)


def default(frame):
    return frame

"""
def face_mesh_overlay1(frame):
    global default_color
    default_color = (225,225,225)
    width, height = frame.shape[1], frame.shape[0]
    result = face_mesh.process(frame)
    if result.multi_face_landmarks:
        q
        for facial_landmarks in result.multi_face_landmarks:
            for i in range(0, 468):
                landmark = facial_landmarks.landmark[i]q
                locx = int(landmark.x * width)
                locy = int(landmark.y * height)
                cv2.circle(frame, (locx, locy), 2, default_color, 1)
    return frame

"""

def face_mesh_overlay2(frame):
    global default_color, dot_thickness, line_thickness, dot_radius
    width, height = frame.shape[1], frame.shape[0]
    result = face_mesh.process(frame)
    if result.multi_face_landmarks:
        for facial_landmarks in result.multi_face_landmarks:
            for i in range(0, 468):
                landmark = facial_landmarks.landmark[i]
                locx = int(landmark.x * width)
                locy = int(landmark.y * height)
                cv2.circle(frame, (locx, locy), dot_radius, default_color, dot_thickness)
        connections = mp_face_mesh.FACEMESH_TESSELATION
        for connection in connections:
                start_index, end_index = connection
                start_landmark = facial_landmarks.landmark[start_index]
                end_landmark = facial_landmarks.landmark[end_index]
                start_point = (int(start_landmark.x * width), int(start_landmark.y * height))
                end_point = (int(end_landmark.x * width), int(end_landmark.y * height))
                cv2.line(frame, start_point, end_point, default_color, line_thickness)
    return frame



def face_mesh_dynamic2(frame):
    global time, default_color, line_thickness
    width, height = frame.shape[1], frame.shape[0]
    result = face_mesh.process(frame)
    
    if result.multi_face_landmarks:
        for facial_landmarks in result.multi_face_landmarks:
            for i in range(0, 468):
                landmark = facial_landmarks.landmark[i]
                locx = int(landmark.x * width)
                locy = int(landmark.y * height)
                
                normalized_time = time / 600.0  # Normalize time between 0 and 1
                max_locy = int(height * normalized_time)  # Gradually increase max Y-coordinate
                
                if locy < max_locy:
                    cv2.circle(frame, (locx, locy), dot_radius, default_color, dot_thickness)
                    
        connections = mp_face_mesh.FACEMESH_TESSELATION
        for connection in connections:
            start_index, end_index = connection
            start_landmark = facial_landmarks.landmark[start_index]
            end_landmark = facial_landmarks.landmark[end_index]
            
            start_point = (int(start_landmark.x * width), int(start_landmark.y * height))
            end_point = (int(end_landmark.x * width), int(end_landmark.y * height))
            
            if start_point[1] < max_locy and end_point[1] < max_locy:
                cv2.line(frame, start_point, end_point, default_color, line_thickness)
                
    time += 8 #Adjusts the pace at which the scan takes place.
    if time >= 600:
        time = 0
        
    return frame

def poly_mesh(frame):
    global time
    global poly_color
    width, height = frame.shape[1], frame.shape[0]
    result = face_mesh.process(frame)
    if result.multi_face_landmarks:
        for facial_landmarks in result.multi_face_landmarks:
            for i in range(0, 468):
                landmark = facial_landmarks.landmark[i]
                locx = int(landmark.x * width)
                locy = int(landmark.y * height)
                cv2.circle(frame, (locx, locy), dot_radius, poly_color, dot_thickness)
                
        connections = mp_face_mesh.FACEMESH_TESSELATION
        for connection in connections:
                start_index, end_index = connection
                start_landmark = facial_landmarks.landmark[start_index]
                end_landmark = facial_landmarks.landmark[end_index]
                start_point = (int(start_landmark.x * width), int(start_landmark.y * height))
                end_point = (int(end_landmark.x * width), int(end_landmark.y * height))
                cv2.line(frame, start_point, end_point, poly_color, line_thickness)
     
    flashing_intensity = np.sin(time / 8)  # Adjust the divisor for desired flashing speed
    color_interpolation = int((1 + flashing_intensity) * 127)  # Interpolate color intensity
    
    poly_color = (255, 255-color_interpolation,255-color_interpolation)  # White to Red
    
    time += poly_flash_speed
    if time > 100:
        time = 0
          
    return frame


def static_head(frame):
    global default_color, time, prev_face_position, smoothing_factor
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey_frame, 1.3, 5)
    
    if len(faces) > 0:
        # Assuming there's only one face detected, you can modify this if needed
        (x, y, w, h) = faces[0]
        new_y = max(0, y - int(0.3 * h))
        rect_x = x - int(0.1 * w)
        rect_width = w + int(0.2 * w)
        
        # Smoothly update the position of the rectangle
        if prev_face_position is None:
            prev_face_position = (rect_x, new_y, rect_width, y + h + 20)
        else:
            prev_face_position = (
                int((1 - smoothing_factor) * prev_face_position[0] + smoothing_factor * rect_x),
                int((1 - smoothing_factor) * prev_face_position[1] + smoothing_factor * new_y),
                int((1 - smoothing_factor) * prev_face_position[2] + smoothing_factor * rect_width),
                int((1 - smoothing_factor) * prev_face_position[3] + smoothing_factor * (y + h + 20))
            )

        cv2.rectangle(frame, (prev_face_position[0], prev_face_position[1]),
                      (prev_face_position[0] + prev_face_position[2], prev_face_position[3]), default_color, line_thickness)
    elif prev_face_position == None:
        pass
    else:
        cv2.rectangle(frame, (prev_face_position[0], prev_face_position[1]),
                      (prev_face_position[0] + prev_face_position[2], prev_face_position[3]), default_color, line_thickness)
    return frame


#face_left = face[:, :w//2]
#cv2.rectangle(face_left,(ex,ey),(ex+ew,ey+eh),(225,225,255),2)

def eye_rectangle(frame):
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey_frame, 1.2, 8)
    for (x, y, w, h) in faces:
        grey_face = grey_frame[y:y+h, x:x+w] # cut the gray face frame out
        face = frame[y:y+h, x:x+w] # cut the face frame out
        #coords = eye_cascade.detectMultiScale(grey_face)
        left = grey_face[:, :w//2]
        left_coords = eye_cascade.detectMultiScale(left, 1.2,5)
       
        right = grey_face[:, w//2:]
        right_coords = eye_cascade.detectMultiScale(right, 1.2,5)
    
        
        for (ex,ey,ew,eh) in left_coords: 
            if ey+eh > height/2:
                pass
            face_left = face[:, :w//2]
            cv2.rectangle(face_left,(ex,ey),(ex+ew,ey+eh),(225,225,255),2)
            
        for (ex,ey,ew,eh) in right_coords: 
            if ey+eh > height/2:
                pass
            face_right = face[:, w//2:]
            cv2.rectangle(face_right,(ex,ey),(ex+ew,ey+eh),(225,225,255),2)
    return frame



filter_dictionary = {"eye_track": eye_rectangle, "static_mesh": face_mesh_overlay2, "default": default,
                     "head_static": static_head,"face_scan": face_mesh_dynamic2, "poly": poly_mesh}


_,frame1 = vid.read()
with pyvirtualcam.Camera(width=frame1.shape[1], height=frame1.shape[0], fps=60) as cam:
         
    while True:
        # Check for key events to change filter_typer
        
        if keyboard.is_pressed('q'):
            break
        elif keyboard.is_pressed('1'):
            filter_type = "head_static"
        elif keyboard.is_pressed('2'):
            filter_type = "face_scan"
        elif keyboard.is_pressed('3'):
            filter_type = "static_mesh"
        elif keyboard.is_pressed('4'):
            filter_type = "poly"
        elif keyboard.is_pressed('5'):
            filter_type = "eye_track"
        elif keyboard.is_pressed('0'):
            filter_type = "default"
            
            
        # Capture the video frame by frame
        ret, frame = vid.read()

        # Convert the frame to BGR format (if it's not already)
        if frame.shape[-1] == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Apply the selected filter
        frame = filter_dictionary[filter_type](frame)
    
        #cv2.imshow("frame", frame)

        # Display the resulting frame in the virtual camera
        cam.send(frame)

        # Sleep to control frame rate
        cam.sleep_until_next_frame()
    

# Release the video capture and close all windows
vid.release()
cv2.destroyAllWindows()
