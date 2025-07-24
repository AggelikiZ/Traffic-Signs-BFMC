import cv2
import numpy as np

def empty(a):
    pass
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x=0
    y=0
    w=0
    h=0
    objectType = "None"
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area>600: #600
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            print(len(approx))
            objCor = len(approx)
            print(objCor)
            x, y, w, h = cv2.boundingRect(approx)

            if objCor ==3: objectType ="Tri"
            elif objCor == 4:
                aspRatio = w/float(h)
                if aspRatio >0.98 and aspRatio <1.03: objectType= "Square"
                else:objectType="Rectangle"
            elif objCor>4 and objCor<9: objectType= "Hexagon"
            elif objCor>=9 : objectType= "Circles"
            else:objectType="None"



            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2) #get this to detect color
            cv2.putText(imgContour,objectType,
                        (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,
                        (0,0,0),2)
            return x,y,w,h,objectType




try:
    #------------------SHAPE DETECTION-----------------------------------#
    path = 'priority2.png'
    img = cv2.imread(path)
    dimensions = img.shape
    h = int(dimensions[0])
    w = int(dimensions[1])
    #img = img[0: int(h/3) , int(w/2):w]
    img = img[0: int(h/2) , int(w/2):w]
    imgContour = img.copy()

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(7,7),2) # the originals are at trafficSigns.py
    imgCanny = cv2.Canny(imgBlur,60,70)
    cv2.imshow("hshs",img)
    #cv2.imshow("blur",imgBlur)
    cv2.imshow("ss",imgCanny)
    cv2.waitKey(0)
    x,y,w,h,shape = getContours(imgCanny)

    imgBlank = np.zeros_like(img)
    imgStack = stackImages(0.5,([img,imgGray,imgBlur],
                                [imgCanny,imgContour,imgBlank]))

    cv2.imshow("Stack", imgStack)

    cv2.waitKey(0)




    #####################color detection#####################################


    path = 'priority2.png'
    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars",640,240)
    cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)
    cv2.createTrackbar("Hue Max","TrackBars",19,179,empty)
    cv2.createTrackbar("Sat Min","TrackBars",110,255,empty)
    cv2.createTrackbar("Sat Max","TrackBars",240,255,empty)
    cv2.createTrackbar("Val Min","TrackBars",153,255,empty)
    cv2.createTrackbar("Val Max","TrackBars",255,255,empty)


    img_cropped = img[y-20:y + h +20, x-20:x + w+20]
    imgHSV = cv2.cvtColor(img_cropped,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    color = "None"
    #------RED MASK--------
    lower = np.array([0,79,97]) #[124,90,75]
    upper = np.array([179,205,185]) #[179,213,171]
    red_mask = cv2.inRange(imgHSV,lower,upper)
    red_imgResult = cv2.bitwise_and(img_cropped,img_cropped,mask=red_mask)
    #print(imgResult.size)
    print(red_imgResult.size,"red")

    #detect color
    number_of_black_pix = np.sum(red_imgResult == 0)
    if number_of_black_pix<red_imgResult.size-200:
        color ="red"

    # ------BLUE MASK--------
    lower = np.array([105, 176, 33]) #[109, 205, 22]
    upper = np.array([141, 218, 137]) # [114, 232, 208]
    blue_mask = cv2.inRange(imgHSV, lower, upper)
    blue_imgResult = cv2.bitwise_and(img_cropped, img_cropped, mask=blue_mask)
    print(blue_imgResult.size,"blue")

    # detect color
    number_of_black_pix = np.sum(blue_imgResult == 0)
    print(number_of_black_pix)
    if number_of_black_pix < blue_imgResult.size - 100:
        color = "blue"
        print("yes")


    # cv2.imshow("Original",img)
    # cv2.imshow("HSV",imgHSV)
    # cv2.imshow("Mask", mask)
    # cv2.imshow("Result", imgResult)

    if(shape=="Hexagon" and color=="red"):
        print("stop")
    elif(shape=="Tri" and color=="blue"):
        print("crosswalk")
    elif(shape=="Hexagon" and color=="blue"):
        print("parking")
    if (shape == "Rectangle" and color == "red"):
        print("no entry")


    imgStack = stackImages(0.6,([img_cropped,imgHSV],[red_mask,red_imgResult]))
    cv2.imshow("Stacked Images", imgStack)

    cv2.waitKey(0)

except:
    print("SHIT")



