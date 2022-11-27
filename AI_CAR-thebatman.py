from unity_utils.unity_utils import Unity
import cv2
import time
import math
from collections import Counter
import numpy as np
# import imutils

unity_api = Unity(11000)
unity_api.connect()
re_speed = 18

def contour(image):
    key = None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    detected_circles = cv2.HoughCircles(gray, 
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
               param2 = 30, minRadius = 1, maxRadius = 40)

    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        print(detected_circles)
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            # Draw the circumference of the circle.
            cv2.circle(image, (a, b), r, (255, 10, 10), 3)
            print(image[b,a])
            if( image[b,a] == [0,0,255]).all():
                key = "di_thang"
            elif( image[b,a] == [0,255,0]).all():
                key = "re_trai"
            elif( image[b,a] == [255,0,0]).all():
                key = "re_phai"
            elif( image[b,a] == [255,0,178]).all():
                key = "cam_di_thang"
            elif( image[b,a] == [255,0,255]).all():
                key = "cam_re_phai"
            elif( image[b,a] == [0,255,255]).all():
                key = "cam_re_trai"
            print(key)


    a=np.all(image[148, :, :] == [0, 0, 0], axis = 1)
    a_check= np.all(image[146, :, :] == [0, 0, 0], axis = 1)

    b=np.all(image[110, :, :] == [0, 0, 0], axis = 1)
    c=np.all(image[112, :, :] == [0, 0, 0], axis = 1)
    d=np.all(image[123, :, :] == [0, 0, 0], axis = 1)   
    e=np.all(image[124, :, :] == [0, 0, 0], axis = 1)
    f=np.all(image[125, :, :] == [0, 0, 0], axis = 1)
    a0 = Counter(a)[0]
    a1 = Counter(a_check)[0]

    countimg = max([a0,a1])
    b1 = Counter(b)[0] 
    c1 = Counter(c)[0] 
    e1 = Counter(e)[0] 
    d1 = Counter(d)[0] 
    f1 = Counter(f)[0] 
    cout_check = max([b1,c1,e1,d1,f1]) 
    return image,countimg,key,cout_check


def caculateSpeed(a,b):
    speed = 22.5*math.exp((25-abs(b-a))/200)
    print("speed: ",speed)
    return speed
    
def caculateAngle(a,b):
    angle = 31*(math.exp((abs(b-a))/270)-1)
    print("angle: " , angle)
    if (b>a):
        return angle
    else:
        return - angle 

prekey = None
t1= time.time()
key_check = False
while True:
    try:
        # cv2.waitKey(50)
        left_image, right_image = unity_api.get_images()
        # cv2.imshow('ff',image)
        # cv2.imwrite('ga.jpg',left_image)
        img_full=cv2.resize(left_image,dsize=(600,150))
        # print('shape',img_full.shape)
        left_image,acountimg,lkey,lcout_check=contour(left_image)
        right_image,bcountimg,rkey,rcout_check=contour(right_image)
        key = rkey
        img_full[:,:300,:]=left_image
        img_full[:,300:600,:]=right_image[:,:,:]
        #cv2.imshow('img',img_full)
        #cv2.waitKey(1)

        if key == None:
            key = prekey
        prekey = key

        print("trai: ", acountimg)
        print("phai: ", bcountimg)
        print("bien bao: ", key)
        if (acountimg + bcountimg) >=540 :
            if key == 're_trai':
                unity_api.set_speed_angle(re_speed, -25)
            elif key == 'di_thang':
                unity_api.set_speed_angle(18, 0)
            elif key == 're_phai':
                unity_api.set_speed_angle(re_speed, 25)
            elif key == 'cam_re_phai':
                unity_api.set_speed_angle(re_speed, -25)
            elif key == 'cam_re_trai':
                unity_api.set_speed_angle(re_speed, 25)
        elif (acountimg + bcountimg) >=500 and (lcout_check>=265):
            if key == 're_trai':
                unity_api.set_speed_angle(re_speed, -25)
            elif key == 'di_thang':
                unity_api.set_speed_angle(18, 0)
            elif key == 're_phai':
                unity_api.set_speed_angle(re_speed, 25)
            elif key == 'cam_di_thang':
                unity_api.set_speed_angle(re_speed, -25)
            elif key == 'cam_re_trai':
                unity_api.set_speed_angle(re_speed, 25)
        elif (acountimg + bcountimg) >=500 and (rcout_check>=265):
            if key == 're_trai':
                unity_api.set_speed_angle(re_speed, -25)
            elif key == 'di_thang':
                unity_api.set_speed_angle(18, 0)
            elif key == 're_phai':
                unity_api.set_speed_angle(re_speed, 25)
            elif key == 'cam_di_thang':
                unity_api.set_speed_angle(re_speed, 25)

            elif key == 'cam_re_phai':
                unity_api.set_speed_angle(18, 0)

        # elif abs(acountimg - bcountimg) <= 80:
        #     data = unity_api.set_speed_angle(18, (bcountimg - acountimg)*0)
        #     continue
        elif (abs(acountimg - bcountimg) >=0):
            data = unity_api.set_speed_angle(caculateSpeed(bcountimg,acountimg), caculateAngle(acountimg, bcountimg))

    except:
        unity_api.set_speed_angle(15, 0)
