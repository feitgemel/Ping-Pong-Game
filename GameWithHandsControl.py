# Ping-Pong game with turtle module.
# Done by Sri Manikanta Palakollu.
# Version - 3.7.0

import turtle as t
import os
import mediapipe as mp 
import cv2

from activateKeyboard import Akey, Qkey
from activateKeyboard import PressKey, ReleaseKey  


mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
waitTimePressKey=0.2

# Score varibales

player_a_score = 0
player_b_score = 0

win = t.Screen()    # creating a window
win.title("Ping-Pong Game") # Giving name to the game.
win.bgcolor('black')    # providing color to the HomeScreen
win.setup(width=800,height=600) # Size of the game panel 
win.tracer(n=1)   # which speed up's the game.


# Creating left paddle for the game

paddle_left = t.Turtle()
paddle_left.speed(0)
paddle_left.shape('square')
paddle_left.color('red')
paddle_left.shapesize(stretch_wid=5,stretch_len=1)
paddle_left.penup()
paddle_left.goto(-350,0)

# Creating a right paddle for the game

paddle_right = t.Turtle()
paddle_right.speed(0)
paddle_right.shape('square')
paddle_right.shapesize(stretch_wid=5,stretch_len=1)
paddle_right.color('red')
paddle_right.penup()
paddle_right.goto(350,0)

# Creating a pong ball for the game

ball = t.Turtle()
ball.speed(0)
ball.shape('circle')
ball.color('yellow')
ball.penup()
ball.goto(0,0)
ball_dx = 2   # Setting up the pixels for the ball movement.
ball_dy = 2

# Creating a pen for updating the Score

pen = t.Turtle()
pen.speed(0)
pen.color('skyblue')
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write(" Player A: 0                   Player B: 0 ",align="center",font=('Monaco',24,"normal"))


# Moving the left Paddle using the keyboard

def paddle_left_up():
    y = paddle_left.ycor()
    y = y + 15
    paddle_left.sety(y)

# Moving the left paddle down

def paddle_left_down():
    y = paddle_left.ycor()
    y = y - 15
    paddle_left.sety(y)

# Moving the right paddle up

def paddle_right_up():
    y = paddle_right.ycor()
    y = y + 15
    paddle_right.sety(y)

# Moving right paddle down

def paddle_right_down():
    y = paddle_right.ycor()
    y = y - 15
    paddle_right.sety(y)

# Keyboard binding

win.listen()
win.onkeypress(paddle_left_up,"q")
win.onkeypress(paddle_left_down,"a")
win.onkeypress(paddle_right_up,"Up")
win.onkeypress(paddle_right_down,"Down")




# Main Game Loop

with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:

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
            
            rightHipCx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x * w)
            rightHipCy = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * h)

            leftCx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x * w)
            leftCy = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y * h)
            
            #cv2.circle(image, (leftCx,leftCy) , 15 , (255,0,255), -1 )
            #print(len(landmarks)) # always 33 points of the pose model

            leftHipCx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x * w)
            leftHipCy = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y * h)
            cv2.circle(image, (leftHipCx,leftHipCy) , 15 , (255,0,255), -1 )

            noseCx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * w)
            noseCy = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * h)
            cv2.circle(image, (noseCx,noseCy) , 15 , (255,0,255), -1 )

            if leftCy <  noseCy :
                messageText="Left Up"    
                #cv2.rectangle(image, (20, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                cv2.putText(image, "Left Up", (leftCx, leftCy-50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                PressKey(Qkey) # press the U key
                time.sleep(waitTimePressKey) 
                ReleaseKey(Qkey) # press the U key
                print(messageText)


            if leftCy > leftHipCy :
                messageText="Left Down"    
                #cv2.rectangle(image, (700, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                cv2.putText(image, "Left Down", (leftCx,leftCy-50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                PressKey(Akey) # press the A key
                time.sleep(waitTimePressKey) 
                ReleaseKey(Akey) # press the A key

            if leftCy < leftHipCy and leftCy > noseCy:
                messageText="Left center"    
                #cv2.rectangle(image, (700, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                cv2.putText(image, "Left center", (leftCx,leftCy-50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)



            if rightCy < noseCy :
                messageText="Right Up"    
                #cv2.rectangle(image, (700, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                cv2.putText(image, "Right Up", (rightCx,rightCy-50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

            if rightCy > rightHipCy :
                messageText="Right Down"    
                #cv2.rectangle(image, (700, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                cv2.putText(image, "Right Down", (rightCx,rightCy-50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

            if rightCy < rightHipCy and rightCy > noseCy:
                messageText="Right center"    
                #cv2.rectangle(image, (700, 300), (270, 425), (255, 255, 0), cv2.FILLED)
                cv2.putText(image, "Right center", (rightCx,rightCy-50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)


        except: # if we cannot find any landmarks 
            pass

        #mp_drwaing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS)
        
        cv2.imshow('image',image)


        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


        win.update() # This methods is mandatory to run any game

        # Moving the ball
        ball.setx(ball.xcor() + ball_dx)
        ball.sety(ball.ycor() + ball_dy)

        # setting up the border

        if ball.ycor() > 290:   # Right top paddle Border
            ball.sety(290)
            ball_dy = ball_dy * -1
            
        
        if ball.ycor() < -290:  # Left top paddle Border
            ball.sety(-290)
            ball_dy = ball_dy * -1
            

        if ball.xcor() > 390:   # right width paddle Border
            ball.goto(0,0)
            ball_dx = ball_dx * -1
            player_a_score = player_a_score + 1
            pen.clear()
            pen.write("Player A: {}                    Player B: {} ".format(player_a_score,player_b_score),align="center",font=('Monaco',24,"normal"))
            os.system("afplay wallhit.wav&")



        if(ball.xcor()) < -390: # Left width paddle Border
            ball.goto(0,0)
            ball_dx = ball_dx * -1
            player_b_score = player_b_score + 1
            pen.clear()
            pen.write("Player A: {}                    Player B: {} ".format(player_a_score,player_b_score),align="center",font=('Monaco',24,"normal"))
            os.system("afplay wallhit.wav&")


        # Handling the collisions with paddles.

        if(ball.xcor() > 340) and (ball.xcor() < 350) and (ball.ycor() < paddle_right.ycor() + 40 and ball.ycor() > paddle_right.ycor() - 40):
            ball.setx(340)
            ball_dx = ball_dx * -1
            os.system("afplay paddle.wav&")

        if(ball.xcor() < -340) and (ball.xcor() > -350) and (ball.ycor() < paddle_left.ycor() + 40 and ball.ycor() > paddle_left.ycor() - 40):
            ball.setx(-340)
            ball_dx = ball_dx * -1
            os.system("afplay paddle.wav&")



cap.release()
cv2.destroyAllWindows()