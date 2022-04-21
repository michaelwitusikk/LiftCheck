import cv2
import mediapipe as mp
import numpy as np
import datetime
import time

from threading import Thread

from gtts import gTTS

from playsound import playsound


from FormScripts import repClass
from FormScripts import workoutSetClass

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def pushup_render(max_reps,draw_pose, videoLocation):
    s = workoutSetClass.workout_set()
    rep_count = 0
    count = 0
    tracking = None
    current_rep = None
    if videoLocation != "":
        cap = cv2.VideoCapture(videoLocation)
    else:
        count = 90
        cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    mytext = 'Make sure to go to depth'
    myobj = gTTS(text=mytext, lang='en', slow=False)
    myobj.save("parallelissue.mp3")
    
    myText = "keep back straight"
    myobj = gTTS(text=mytext, lang='en', slow=False)
    myobj.save("backstraight.mp3")
    
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
            if draw_pose:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(
                                            color=(245, 117, 66), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(
                                            color=(245, 66, 230), thickness=2, circle_radius=2)
                                        )
            
            
            #find the angle of the elbows and the angle of the shoulders
            try:

                body_angle = calculate_body_angle(results)
                right_arm = calculate_right_arm_angle(results)
                left_arm = calculate_left_arm_angle(results)
                #display the angle on the screen

                cv2.rectangle(image, (0,0), (280,100), (0,0,0), -1)

                cv2.putText(image, "Count: " + str(rep_count), (15, 82), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 55, 255), 2)
                cv2.putText(image, "body angle: " + str(body_angle), (15, 35), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 55, 255), 2)
                cv2.putText(image, "left angle: " + str(left_arm), (15, 100), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 55, 255), 2)
                
                # Are we tracking yet?
                if tracking:
                    if current_rep is None and (right_arm > 160 or left_arm > 160):
                        current_rep = repClass.rep()
                    if current_rep:
                        if body_angle > 25:
                            current_rep.add_form_issue("Straight back")
                            thread = Thread(target = say_issue, args = ('./backstraight.mp3',))
                            thread.start()

                        if (left_arm < 90):
                            rep_count += 1
                            s.left_reps.append(current_rep)
                            current_rep = None


                    if (len(s.left_reps) >= int(max_reps)) :
                        with open('pushupForm.txt', 'w') as f:
                            f.write("Reps:\n")
                            for i in range(len(s.left_reps)):
                                if len(s.left_reps[i].get_form_issues()) == 0:
                                    f.write("Rep #" + str(i+1)+": Perfect! Depth Angle: " + str(s.left_reps[i].min_angle))
                                    f.write("\n")
                                else:
                                    tempStr = ""
                                    for issue in s.left_reps[i].get_form_issues():
                                        tempStr += str(issue)
                                        tempStr += ', '
                                    f.write("Rep #" + str(i+1)+": " + tempStr + " Depth Angle: "+ str(s.left_reps[i].min_angle))
                                    f.write("\n")
                            f.close()
                        break
                

                else:
                    # Not tracking, should we be?
                    if count > 0:
                        cv2.putText(image, "Starting in: " + str(round(count/30)), (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 55, 255), 2)
                        count -= 1
                    else:
                        tracking = True

            except:
                pass
            

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

def calculate_body_angle(results):
    landmarks = results.pose_landmarks.landmark
    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    #calculate the angle between the shoulders, elbow, and wrists
    angle = calculate_angle(ankle, hip, shoulder)
    return abs(180-angle).round(0)

def calculate_right_arm_angle(results):
    landmarks = results.pose_landmarks.landmark
    wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    #calculate the angle between the shoulders, elbow, and wrists
    angle = calculate_angle(shoulder, elbow, wrist)
    return abs(180-angle).round(0)

def calculate_left_arm_angle(results):
    landmarks = results.pose_landmarks.landmark
    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    #calculate the angle between the shoulders, elbow, and wrists
    angle = calculate_angle(elbow, shoulder, wrist)
    return abs(180-angle).round(0)

def say_issue(mp3):
    playsound(mp3)
