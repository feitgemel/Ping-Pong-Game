import mediapipe as mp 
import cv2

#mp_drwaing = mp.solutions.drawing_utils
#mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose

#mp_drwaing.DrawingSpec(color=(0,0,255),thickness=2 ,circle_radius=3 ) # color , thickness , radius

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    #for lndmark in mp_pos.PoseLandmark:
    #    print(lndmark)     


    while cap.isOpened():

        re, frame = cap.read()
        

        # change it to RGB
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image.flags.writeable = False # save memory before the model

        results = pose.process(image)

                
        image.flags.writeable = True
        
        # recolor image back to BGR
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        #print(results.pose_landmarks)
        #print(mp_pose.POSE_CONNECTIONS)

        try:
            # if we have a detection
            landmarks = results.pose_landmarks.landmark
            
            h , w , c = image.shape
            
            rightCx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x * w)
            rightCy = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y * h)
            #cv2.circle(image, (rightCx,rightCy) , 15 , (255,0,255), -1 )
            
            leftCx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x * w)
            leftCy = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y * h)
            
            #cv2.circle(image, (leftCx,leftCy) , 15 , (255,0,255), -1 )
            #print(len(landmarks)) # always 33 points of the pose model

            noseCx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * w)
            noseCy = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * h)
            #cv2.circle(image, (noseCx,noseCy) , 15 , (255,0,255), -1 )

            if leftCy <  noseCy :
                messageText="Left Up"    
                #cv2.rectangle(image, (20, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                cv2.putText(image, "Left Up", (leftCx, leftCy-50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

            if rightCy < noseCy :
                messageText="Right Up"    
                #cv2.rectangle(image, (700, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                cv2.putText(image, "Right Up", (rightCx,rightCy-50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)



        except: # if we cannot find any landmarks 
            pass

        #mp_drwaing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS)
        
        cv2.imshow('image',image)

        #show original frame  
        #cv2.imshow('frame',frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()