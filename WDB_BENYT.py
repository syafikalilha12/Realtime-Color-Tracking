import cv2
import numpy as np

frameWidth = 640
frameHeigh = 480 
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeigh)
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
def empty(a):
    pass

cv2.namedWindow("parameters")
cv2.resizeWindow("parameters",640,240)
cv2.createTrackbar("threshold1","parameters",150,255, empty)
cv2.createTrackbar("threshold2","parameters",255,255, empty)
cv2.createTrackbar("area","parameters",300,30000,empty)

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

def getContours(img,imgContour):

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        nilaiarea = cv2.getTrackbarPos("area","parameters")
        if area > nilaiarea:
            cv2.drawContours(imgContour, cnt, -1, (255,0,255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 *peri, True)
            #print(len(approx))
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y ), (x +w, y+h),(0,255,0),5)
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            pus = (cx,cy)
            #centers.append([cx,xy])
            #cv2.circle(imgContour, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(imgContour, "points: "+str(len(approx)), (x+w+20, y+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2) 
            cv2.putText(imgContour, "area: "+str(int(area)), (x+w+20, y+45), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            titik = len(approx)
            if titik == 4:
                cv2.putText(imgContour,"Segi 4", (x+w+20, y+80),cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            
            if titik == 8:
                cv2.circle(imgContour, (cx, cy), 7, (255, 255, 255), -1)
                cv2.putText(imgContour,"Lingkaran", (x+w+20, y+80), cv2.FONT_HERSHEY_COMPLEX,1, (0,255,0), 2)  
                cv2.putText(imgContour,"("+str(pus[0])+","+str(pus[1])+")", (pus[0]+10,pus[1]+15), cv2.FONT_HERSHEY_COMPLEX, 0.4,(0, 255, 0),1)
                print(pus)
while True:
    succes, img= cap.read()
    imgContour = img.copy()

    imgBlur = cv2.GaussianBlur(img,(7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("threshold1","parameters")
    threshold2 = cv2.getTrackbarPos("threshold2","parameters")
    imgCanny = cv2.Canny(imgGray,threshold1,threshold2)
    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)   
    
    getContours(imgDil,imgContour)

    imgStack = stackImages(0.8,([img,imgContour],[imgDil,imgCanny]))
    
    cv2.imshow("Result",imgStack)
    if cv2.waitKey(1) & 0xFF==ord('m'):
        break