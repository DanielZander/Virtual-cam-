import pyvirtualcam
import keyboard
from filters import *
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

vid = cv2.VideoCapture(0) # number in () is where you input camera index. 

#########################VIDEOSTREAM INPUT OPTIONS#############################
# Index 0 = your actual webcamera - this is used for when you want to play around with the filters yourself, with the videostream from you acutal webcam as input.
# Index 1 or index 2 will be your virtual-camera plugin, if the one doesnt work, try the other. 
#########################VIDEOSTREAM INPUT OPTIONS#############################

vid.set(cv2.CAP_PROP_FRAME_HEIGHT,height)


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
