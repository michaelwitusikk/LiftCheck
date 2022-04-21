import cv2
import mediapipe as mp
import numpy as np
import datetime
import time

from FormScripts import repClass
from FormScripts import workoutSetClass

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def bicepRendering(max_reps, draw_pose, videoLocation):

    s = workoutSetClass.workout_set()
    Lrep_count = 0
    Rrep_count = 0
    count = 0
    tracking = None
    currentLeftRep = None
    currentRightRep = None
    if videoLocation != "":
        cap = cv2.VideoCapture(videoLocation)
    else:
        count = 90
        cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
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

            # find the angle of the elbows and the angle of the shoulders
            try:
                left_angle = calculate_left_arm(results)
                right_angle = calculate_right_arm(results)
                left_armpit_angle = calculate_left_armpit(results)
                right_armpit_angle = calculate_right_armpit(results)
                # display the angle on the screen
                cv2.putText(image, "Left Bicep: " + str(left_angle),
                            (15, 35), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 55, 255), 2)
                cv2.putText(image, "Right Bicep: " + str(right_angle),
                            (355, 35), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 55, 255), 2)
                cv2.putText(image, "right armpit: " + str(right_armpit_angle),
                            (355, 65), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 55, 255), 2)
                cv2.putText(image, "left armpit: " + str(left_armpit_angle),
                            (15, 65), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 55, 255), 2)
                cv2.putText(image, "Right Count: " + str(Rrep_count),
                            (355, 95), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 55, 255), 2)
                cv2.putText(image, "Left Count: " + str(Lrep_count),
                            (15, 95), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 55, 255), 2)

                # Are we tracking yet?
                if tracking:

                    if left_angle > 150:
                        if currentLeftRep is None:
                            currentLeftRep = repClass.rep()
                            currentLeftRep.which_side_rep = "left"
                            currentLeftRep.timeup = time.time

                    if right_angle > 150:
                        if currentRightRep is None:
                            currentRightRep = repClass.rep()
                            currentRightRep.which_side_rep = "right"
                            currentRightRep.timeup = time.time

                    if currentLeftRep:
                        # Have we finsished the curl?
                        if left_angle < 55:
                            # Curl is finished, add the rep to workout set
                            s.left_reps.append(currentLeftRep)
                            currentLeftRep = None
                            Lrep_count += 1
                        else:
                            # In the middle of a curl, check for form issues?
                            if left_armpit_angle > 35:
                                currentLeftRep.add_form_issue(
                                    "Left elbow too far away from body")

                    if currentRightRep:
                        # Have we finsished the curl?
                        if right_angle < 55:
                            # Curl is finished, add the rep to workout set
                            s.right_reps.append(currentRightRep)
                            currentRightRep = None
                            Rrep_count += 1
                        else:
                            # In the middle of a curl, check for form issues?
                            if right_armpit_angle > 35:
                                currentRightRep.add_form_issue(
                                    "Right elbow too far away from body")

                    print("\nSet:   ")
                    for rep in s.right_reps:
                        print(rep)
                    print("----")
                    for rep in s.left_reps:
                        print(rep)

                    if (len(s.left_reps) >= int(max_reps)) and (len(s.right_reps) >= int(max_reps)):
                        with open('bicepcurlform.txt', 'w') as f:
                            f.write("Left Reps:\n")
                            for i in range(len(s.left_reps)):
                                if len(s.left_reps[i].get_form_issues()) == 0:
                                    f.write("Rep #" + str(i+1)+": Perfect")
                                    f.write("\n")
                                else:
                                    tempStr = ""
                                    for issue in s.left_reps[i].get_form_issues():
                                        tempStr += str(issue)
                                        tempStr += ', '
                                    f.write("Rep #" + str(i+1)+": " + tempStr)
                                    f.write("\n")
                            f.write("Right Reps:\n")
                            for i in range(len(s.right_reps)):
                                if len(s.right_reps[i].get_form_issues()) == 0:
                                    f.write("Rep #" + str(i+1)+": Perfect")
                                    f.write("\n")
                                else:
                                    tempStr = ""
                                    for issue in s.right_reps[i].get_form_issues():
                                        tempStr += str(issue)
                                        tempStr += ', '
                                    f.write("Rep #" + str(i+1)+": " + tempStr)
                                    f.write("\n")
                            f.close()
                        break

                else:
                    # Not tracking, should we be?
                    if count > 0:
                        cv2.putText(image, "Starting in: " + str(round(count/30)),
                                    (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 55, 255), 2)
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


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    C = np.array(c)  # End
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
        np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360-angle
    return round(angle, 2)


def calculate_left_arm(results):
    landmarks = results.pose_landmarks.landmark
    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    # calculate the angle between the shoulders, elbow, and wrists
    angle = calculate_angle(shoulder, elbow, wrist)
    return angle


def calculate_right_arm(result):
    landmarks = result.pose_landmarks.landmark
    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
             landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
             landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    # calculate the angle between the shoulders, elbow, and wrists
    angle = calculate_angle(shoulder, elbow, wrist)
    return angle


def calculate_right_armpit(result):
    landmarks = result.pose_landmarks.landmark
    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
             landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
           landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    angle = calculate_angle(shoulder, elbow, hip)
    return abs(angle - 180).round(0)


def calculate_left_armpit(result):
    landmarks = result.pose_landmarks.landmark
    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    angle = calculate_angle(shoulder, elbow, hip)
    return abs(angle - 180).round(0)
