# VRMovie_inv_distorter
Correct distorted movie captured in SteamVR's mirror.<br>
OpenCV,OpenCV-ffmpeg,numpy and numba are needed.<br>
This script fixes the distortion of recorded videos you record the screen of Display mirror of SteamVR.<br>
Most VR devices have lenses to magnify image from screen but they also distorts images.<br>
VR application distorts images in advance to compensate distortion by lenses.<br>
When You record the window of SteamVR's Display mirror, pre-distorted images are recorded.<br>
This script simulate post-distortion which is originally　brought by lenses.<br>

How to use<br>
1.Record SteamVR's mirrored display. sample movie(distorted.mp4) is available.<br>
2.put corrector.py and recorded movie(rename distorted.mp4) in the same folder.<br>
3.run corrector.py, then you will get compensated movie. corrected.mp4 is compensated sample movie.<br>
 
corrector.py assume that the pre-distortion is defined (X,Y)= (x,y) * (a * r ** 4 + b * r ** 2 + c) where r ** 2 = (x ** 2 + y ** 2)<br>
You can change coefficients, which are a,b and c ,to get better result.<br>
If debug flag is true, script will give grid to original(distorted) movie. You can check the degree of compensation.<br>
If guide flag is true, script will give grid to compensated movie. You can check whether compensated movie is not distorted.<br>
While corrector.py is making compensated movie, it shows the frames of the movie.<br>

This script is very simple, so you will find some to improve it.<br>
I welcome your idea!<br>
