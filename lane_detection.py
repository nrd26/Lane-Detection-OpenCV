import cv2 as cv
import numpy as np

def process(image):
    # h = image.shape[0] #h=480
    # w = image.shape[1] #w=640
    pts = np.array([(0,200),(640,200),(640,480),(0,480)])
    msk = np.zeros_like(image)
    
    cv.fillPoly(msk, np.int32([pts]),(255.255,255))
    
   
    fin = cv.bitwise_and(image,msk)
    #cv.imshow('fin',fin)
    blur = cv.GaussianBlur(fin, (5, 5), 0)
    #cv.imshow('blur',blur)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    #cv.imshow('gray',gray)
    _,thresh = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)
    #cv.imshow('thresh',thresh)
    kernel=np.ones((5,5),np.uint8)
    tophat = cv.morphologyEx(thresh, cv.MORPH_TOPHAT, kernel)
    #cv.imshow('tophat',tophat)
    dilation = cv.dilate(tophat,kernel,iterations=1) 
    # cv.imshow('dilation',dilation)
    canny = cv.Canny(dilation, 150, 200,L2gradient=1)
    # cv.imshow('canny',canny)
    lines = cv.HoughLinesP(canny, rho=2, theta=np.pi/180, threshold=50,lines=np.array([]),minLineLength=5,maxLineGap=40)
    try:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv.line(image, (x1,y1), (x2,y2), (255, 0, 255), thickness=5)
    except:
        pass
    return image
    
cap = cv.VideoCapture('lane.mp4')
while cap.isOpened():
    ret, frame = cap.read()
    frame = process(frame)
    cv.imshow('frame', frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
