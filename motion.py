import cv2
import time
from datetime import datetime
import pandas

df=pandas.DataFrame(columns=["Start","End"])
status_list=[None,None]
time_list=[]
video=cv2.VideoCapture(0)
time.sleep(3)
first_frame=None
while True:

    check, frame=video.read()
    status=0


    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)


    if first_frame is None:
        first_frame=gray
        continue
    delta_frame=abs(first_frame-gray)
    tresh_frame=cv2.threshold(delta_frame,30,255, cv2.THRESH_BINARY)[1]
    tresh_frame=cv2.dilate(tresh_frame,None,iterations=2)
    (_,cnts,_)=cv2.findContours(tresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contours in cnts:
        if cv2.contourArea(contours) < 100000:
            continue
        status=1
        (x, y, w, h)=cv2.boundingRect(contours)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),3)
    status_list.append(status)
    #cv2.imshow("Grey Frame",gray)
    #cv2.imshow("Difference Frame",delta_frame)
    #cv2.imshow("Thresh Frame", tresh_frame)

    cv2.imshow("Color Frame", frame)
    if status_list[-1]==1 and status_list[-2]==0:
        time_list.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        time_list.append(datetime.now())
    key=cv2.waitKey(1)
    if key==ord('q'):
        if status==1:
            time_list.append(datetime.now())
        break

#for i in range(0,len(time_list),2):
#    df=df.append({"Start":time_list[i],"End":time_list[i+1]}, ignore_index=True)

#df.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows
