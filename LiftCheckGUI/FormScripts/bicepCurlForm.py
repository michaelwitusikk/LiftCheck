import cv2
import mediapipe as mp
import numpy as np
import time
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

##TODO##
#figure out a way for the user to start and stop a set.
#implement a way to get the rest time (figure out what angle the person is at while resting)
#implement a way to get the rep time (figure out what angle the person is at while doing the rep)
#getters and setters for rep class
#possible different data representation for set class (currently lists)

def bicepRendering():


    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            # Make detection
            results = pose.process(image)
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(
                                        color=(245, 117, 66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(
                                        color=(245, 66, 230), thickness=2, circle_radius=2)
                                    )
            
            
            #find the angle of the elbows and the angle of the shoulders
            try:
                s = set()
                left_angle = calculate_left_arm(results)
                right_angle = calculate_right_arm(results)
                #display the angle on the screen
                cv2.putText(image, "Left Bicep: " + str(left_angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 55, 255), 2)
                cv2.putText(image, "Right Bicep: " + str(right_angle), (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 55, 255), 2)

                ##add one new rep to the set, when the left_angle is less than 150, begin timing the timeup of the rep
                ##when the left_angle is greater than 150, stop timing the timeup of the rep and add the rep to the set.
                ##create a new rep object and begin timing the timedown of the rep object.        
                 
                # if left_angle < 150:
                #         r = rep()
                #         timeup = time.time
                # else:
                #     r.timeup = time.time - timeup
                #     set.left_reps.append(r)
                
                # for i in set.left_reps:
                #     cv2.putText(image, "Left Reps: " + str(i.timeup), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 55, 255), 2)   
                    
                    
            except:
                pass
            
                if left_angle < 150:
                        r = rep()
                        timeup = time.time
                else:
                    r.timeup = time.time - timeup
                    set.left_reps.append(r)
                
                for i in set.left_reps:
                    cv2.putText(image, "Left Reps: " + str(i.timeup), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 55, 255), 2)
            

            cv2.imshow('Mediapipe Feed', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        
        
        
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array (b) # Mid
    C = np.array (c) # End
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle >180.0:
        angle = 360-angle
    return round(angle, 2)

def calculate_left_arm(results):
    landmarks = results.pose_landmarks.landmark
    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    #calculate the angle between the shoulders, elbow, and wrists
    angle = calculate_angle(shoulder, elbow, wrist)
    return angle

def calculate_right_arm(result):
    landmarks = result.pose_landmarks.landmark
    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    #calculate the angle between the shoulders, elbow, and wrists
    angle = calculate_angle(shoulder, elbow, wrist)
    return angle

def calculate_right_armpit(result):
    landmarks = result.pose_landmarks.landmark
    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    hip =  [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

def calculate_left_armpit(result):
    landmarks = result.pose_landmarks.landmark
    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    
    
class set():
    def __init__(self):
        #total reps
        self.reps = self.left_reps + self.right_reps
        #list of all reps on right hand
        self.right_reps = []
        #list of all reps on left hand
        self.left_reps = []
        #left arm reps
        self.left_reps = len(self.left_reps)
        #right arm reps
        self.right_reps = len(self.right_reps)
      
        
class rep():
    def __init__(self):
        #how much time was the person doing the rep
        self.timeup = 0
        #how much time did the person rest
        self.timedown = 0
        
    #uses the time module to see how long a rep is taking up or resting    
    def timeCounter(self):
        time = time.time()
        return time
            
        
