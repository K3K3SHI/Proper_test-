import cv2
import mediapipe as mp
import time
import turtle
import sys

number = 5
prev_coords = []

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

t = turtle.Turtle()
t.hideturtle()
t.speed(-30)
t.penup()

def draw(): #draws the image using the turtle module
    tip = i.landmark[8]
    he,w,d = frame.shape
    x,y = int(tip.x * w), int(tip.y * he)

    if len(prev_coords) < number:
        prev_coords.append((x, y))
    else:
        prev_coords.pop(0)
        prev_coords.append((x, y))
            
    avgx, avgy = sum(p[0] for p in prev_coords) / len(prev_coords), sum(p[1] for p in prev_coords) / len(prev_coords)


    t.goto(-avgx,-avgy)
    t.pendown()
        #t.dot()
                


    cv2.circle(frame, (x,y), 10, (0 ,255),-1)


def detect_gesture(hand_map):#detects gestures
    it = hand_map.landmark[8]
    mt = hand_map.landmark[12]
    pt = hand_map.landmark[20]
    tt = hand_map.landmark[4]

    if (it.y < mt.y):
        return "circle"
    elif (it.x > tt.x) and (it.x > pt.x):
        return "square"
    else:
        return None
def detect_stop_gesture(hand_map):#stops program
    lmlist=[]
    for id,ln in enumerate(hand_map.landmark):
        h,w,c = frameRGB.shape
        cx, cy = int(ln.x+w),int(ln.y+h)
        lmlist.append([id,cx,cy])
    ix = 0
    iy = 0
    im = 0
    hbx = 0
    hby = 0
    px = 0
    py = 0
    for i in lmlist:
        if i[0] == 7:
            ix,iy=i[1],i[2]
        elif i[0] == 5:
            ix = i[1]
        elif i[0]==19:
            px,py=i[1],i[2]
        elif i[0] == 0:
            hbx, hby = i[1],i[2]
    if(iy < hby) and (iy > im):
        return "hand"
    


    
while True:
    ret,frame  = cap.read()
    frameRGB = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)

    if results.multi_hand_landmarks:
        for i in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame,i,mpHands.HAND_CONNECTIONS)
            gesture = detect_gesture(i)
            stoprec = detect_stop_gesture(i)
            if gesture == "circle":
                t.pendown()
                t.circle(50,0)
                t.penup()
                continue
            elif gesture == "square":
                t.pendown()
                t.forward(50)
                t.right(90)
                t.forward(50)
                t.right(90)
                t.forward(50)
                t.right(90)
                t.forward(50)
                t.penup()
                continue
            
            else:
                draw()
            if stoprec == "hand":
                sys.exit(0)

    cv2.imshow("Image",frame)
    cv2.waitKey(1)

