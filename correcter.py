import cv2
import numpy as np
from tqdm import tqdm
import math
import numba

debug=False

@numba.jit
def inv_frame(frame,c0,c1,c2,c3):
    revframe=np.ones((1080, 1920,3),dtype="uint8")
    for a in range(1080):
        for b in range(1920):
            if b < 960: #left
                r= ((a-540)**2 + (b-480)**2)/(480**2 + 540**2)
                revframe[a][b]= frame[int((a-540)/(1+c0+c1*r+c2*(r**2)+c3*(r**3)))+540][int((b-480)/(1+c0+c1*r+c2*(r**2)+c3*(r**3)))+480]
            else: #right
                r= ((a-540)**2 + (b-1440)**2)/(480**2 + 540**2)
                revframe[a][b]= frame[int((a-540)/(1+c0+c1*r+c2*(r**2)+c3*(r**3)))+540][int((b-1440)/(1+c0+c1*r+c2*(r**2)+c3*(r**3)))+1440]
    if debug:
        for a in range(0,1080,60):
            revframe[a,:]=254
        for b in range(0,1920,60):
            revframe[:,b]=254
        revframe[540,:]=0
        revframe[:,480]=0
        revframe[:,1440]=0
    return revframe

#read video
video = cv2.VideoCapture("./Trim_moto.mp4")
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
wh = (width, height)

frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
frame_rate = int(video.get(cv2.CAP_PROP_FPS))

fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
writer = cv2.VideoWriter('./undistorted.mp4', fmt, frame_rate, wh)
#heuristic value
c0=0.2
c1=0.05
c2=0.05
c3=0.05

for i in tqdm(range(frame_count)): #progress bar
    ret, frame = video.read()
    revframe=inv_frame(frame,c0,c1,c2,c3)
    cv2.imshow("ok",revframe)
    cv2.waitKey(1)
    writer.write(revframe)
writer.release()
video.release()
cv2.destroyAllWindows()