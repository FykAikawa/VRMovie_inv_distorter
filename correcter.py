import cv2
import numpy as np
from tqdm import tqdm
import math
import numba
import os

debug=False
guide=False

@numba.jit
def inv_frame(frame,width,height,c0,c1,c2):
    revframe=np.zeros((height, width,3),dtype="uint8")
    a=c2
    b=c1
    c=c0
    if debug:
        for h in range(0,height,60):
            frame[h,:]=254
        for w in range(0,width,60):
            frame[:,w]=254
        frame[height//2,:]=0
        frame[:,width//4]=0
        frame[:,width*3//4]=0

    for h in range(height):
        for w in range(width):
            if w < width //2: #left
                r = ((h-height/2)**2 + (w-width/4)**2)/((width//4)**2+(height//2)**2)
                scale= (c+b*r+a*r*r)
                #print(r/math.sqrt(480**2 + 540**2))
                revframe[h][w]= frame[int((h-height/2)*scale)+height//2][int((w-width/4)*scale)+width//4]
            else: #right
                r = ((h-height/2)**2 + (w-width*3/4)**2)/((width//4)**2+(height//2)**2)
                scale= (c+b*r+a*r*r)
                revframe[h][w]= frame[int((h-height/2)*scale)+height//2][int((w-width*3/4)*scale)+width*3//4]
    if guide:
        for h in range(0,height,60):
            revframe[h,:]=254
        for w in range(0,width,60):
            revframe[:,w]=254
        revframe[height//2,:]=0
        revframe[:,width//4]=0
        revframe[:,width*3//4]=0
    return revframe

#read video
video = cv2.VideoCapture("./Trim_moto.mp4")
print(video.isOpened())
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
wh = (width, height)

frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
frame_rate = int(video.get(cv2.CAP_PROP_FPS))

fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
writer = cv2.VideoWriter('./undistorted.mp4', fmt, frame_rate, wh)
#heuristic value
#assert c0+c1+c2<1 or script will crush
c0= 1
c1= -0.1
c2= -0.1

for i in tqdm(range(frame_count)): #progress bar
    ret, frame = video.read()
    revframe=inv_frame(frame,width,height,c0,c1,c2)
    cv2.imshow("ok",revframe)
    cv2.waitKey(1)
    writer.write(revframe)
writer.release()
video.release()
cv2.destroyAllWindows()
