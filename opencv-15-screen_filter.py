import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
 
video=cv2.VideoCapture(0)
video.set(3,320)
video.set(4,180)
loopsvar=True
 
segmen=SelfiSegmentation()
 
def imagechange(image):
    global loopsvar
    if image=="firstimage":
        bgimage=cv2.imread('1-Blue_320x180.png')
 
    elif image=="secondimage":
        bgimage=cv2.imread('1-Red_320x180.png')
 
    elif image=="thirdimage":
        bgimage=cv2.imread('1-Purple_320x180.png')

    elif image=="fourthimage":
        bgimage=cv2.imread('1-Green_320x180.png')
 
    while loopsvar:
        check,frame=video.read()
        videoremovebg=segmen.removeBG(frame,bgimage,threshold=0.8)
        cv2.imshow("video",videoremovebg)
        key=cv2.waitKey(1)
        if key==ord('c'):
            loopsvar=False
        elif key == ord('q'):
            imagechange('firstimage')
        elif key == ord('w'):
            imagechange('secondimage')
        elif key == ord('e'):
            imagechange('thirdimage')
        elif key == ord('r'):
            imagechange('fourthimage')
 
while loopsvar:
    _,frame=video.read()
    cv2.imshow("video",frame)
    key=cv2.waitKey(1)
    if key==ord('c'):
        loopsvar=False
 
    elif key == ord('q'):
        imagechange("firstimage")
    elif key == ord('w'):
        imagechange('secondimage')
    elif key == ord('e'):
        imagechange('thirdimage')
    elif key == ord('r'):
            imagechange('fourthimage')


video.release()
cv2.destroyAllWindows()
