import numpy as np
from cv2 import cv2
from PIL import Image
from pylab import *
from scipy.ndimage import filters
import pytesseract

def resize(image,percent_width=100,percent_height=100):
    width = int32(image.shape[1] * percent_width / 100)
    height = int32(image.shape[0] * percent_height / 100)
    resized = cv2.resize(image,(width,height))
    return resized

pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
image = cv2.imread('ind_1.jpg')
cv2.imshow("Original", image)
im2 = filters.gaussian_filter(image,0.2)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edged = cv2.Canny(im2, 170, 200)

contours,heirarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:30]

for c in contours:
    length = cv2.arcLength(c,closed=True)
    approx = cv2.approxPolyDP(c, 0.02 * length, closed=True)
    if len(approx) == 4:  # Select the contour with 4 corners
        numberplate = approx #This is our approx Number Plate Contour
        break
    else :
        numberplate = None

# Drawing the selected contour on the original image
#cv2.drawContours(image, [numberplate], -1, (0,255,0), 3)
x = numberplate
a = min(x[0][0][1],x[2][0][1])
b = max(x[0][0][1],x[2][0][1])
c = min(x[2][0][0],x[0][0][0])
d = max(x[2][0][0],x[0][0][0])
roi = image[a:b,c:d]
width = roi.shape[1]
height = roi.shape[0]
pts1 = float32(x)
pts2 = float32([[width,0],[0,0],[0,height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
result = cv2.warpPerspective(image,matrix,(image.shape[0],image.shape[1]))
roi = result[0:height,0:width]
cv2.imshow("numerplate",roi)
gray_ = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) 
# Performing OTSU threshold 
ret, roi = cv2.threshold(gray_, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY) 
#roi = cv2.adaptiveThreshold(gray_, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 12)
roi = resize(roi,100,30)
cv2.imshow("thresholding",roi)
# Specify structure shape and kernelsize.  
# Kernel size increases or decreases the area  
# of the rectangle to be detected. 
# A smaller value like (10, 10) will detect  
# each word instead of a sentence. 
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 
  
# Appplying dilation on the threshold image 
dilation = cv2.dilate(roi, rect_kernel, iterations = 1) 
  
# Finding contours 
contours_, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
cv2.waitKey(0)
# Creating a copy of image 
im3 = roi.copy()
for cnt in contours_: 
    x, y, w, h = cv2.boundingRect(cnt) 
      
    # Drawing a rectangle on copied image 
    rect = cv2.rectangle(im3, (x, y), (x + w, y + h), (0, 255, 0), 2) 
    # Cropping the text block for giving input to OCR 
    cropped = im3[y:y + h, x:x + w] 
    # Apply OCR on the cropped image 
    text = pytesseract.image_to_string(cropped,lang='eng',config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 --psm 7') #psm 7 or 8 or 13 11,12 also works fine
    if text == '':
        continue
    print(text)