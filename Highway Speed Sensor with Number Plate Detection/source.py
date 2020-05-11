from cv2 import cv2
from pylab import *
from scipy.ndimage import filters
import pytesseract

def resize(image,percent_width=100,percent_height=100): #function to resize image
    width = int32(image.shape[1] * percent_width / 100)
    height = int32(image.shape[0] * percent_height / 100)
    resized = cv2.resize(image,(width,height))
    return resized

def printf(text): #function to print detected numberplate in a nice way
    for i in text:
        if i == ' ':
            pass
        else :
            print(i,end='')
    print()

pytesseract.tesseract_cmd = '/usr/local/bin/tesseract' #specify path to your tesseract executable file
image = cv2.imread('ind_2.jpg')
cv2.imshow("Original", image)

im2 = filters.gaussian_filter(image,0.2) #applying gaussian blur to image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #grayscaling image
edged = cv2.Canny(im2, 170, 200) #canny edge detection

contours,heirarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #finding contours
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:30] #sorting contours more than area of 30 units

for c in contours:
    length = cv2.arcLength(c,closed=True)
    approx = cv2.approxPolyDP(c, 0.02 * length, closed=True) #approx polygon covering contour
    if len(approx) == 4:  # Select the contour with 4 corners
        numberplate = approx #This is our approx Number Plate Contour
        break
    else :
        numberplate = None

# Drawing the selected contour on the original image
#cv2.drawContours(image, [numberplate], -1, (0,255,0), 3)

# the following method is to straighten a numberplate that is slant or skewed

x = numberplate
a = min(x[0][0][1],x[2][0][1])
b = max(x[0][0][1],x[2][0][1])
c = min(x[2][0][0],x[0][0][0])
d = max(x[2][0][0],x[0][0][0])
roi = image[a:b,c:d]
width = roi.shape[1]
height = roi.shape[0]
pts1 = float32(x)
for i in range(4):
    if (x[i][0][1] < x[(i+1)%4][0][1] and x[i][0][0] < x[(i-1)%4][0][0]):
        flag = 1
        break

for j in range(4):
    if flag == 1 :
        break
    if (x[j][0][1] < x[(j-1)%4][0][1] and x[j][0][0] < x[(j+1)%4][0][0]):
        flag = -1
        break

if flag == 1 :
    if i == 0 :
        pts2 = float32([[0,0],[0,height],[width,height],[width,0]])
    elif i == 1 :
        pts2 = float32([[width,0],[0,0],[0,height],[width,height]])
    elif i == 2 :
        pts2 = float32([[width,height],[width,0],[0,0],[0,height]])
    elif i == 3 :
        pts2 = float32([[0,height],[width,height],[width,0],[0,0]])

elif flag == -1 :
    if j == 0 :
        pts2 = float32([[0,0],[width,0],[width,height],[0,height]])
    elif j == 1 :
        pts2 = float32([[0,height],[0,0],[width,0],[width,height]])
    elif j == 2 :
        pts2 = float32([[width,height],[0,height],[0,0],[width,0]])
    elif j == 3 :
        pts2 = float32([[width,0],[width,height],[0,height],[0,0]])

matrix = cv2.getPerspectiveTransform(pts1,pts2)
result = cv2.warpPerspective(image,matrix,(image.shape[0],image.shape[1]))
roi = result[0:height,0:width]
cv2.imshow("numerplate",roi)

#text detection starts here

gray_ = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) #preparing image for thresholding
ret, roi = cv2.threshold(gray_, 200, 255, cv2.THRESH_BINARY) #thresholding image
roi = resize(roi,100,89) #using resize function for better text detection
cv2.imshow("threshold",roi)

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) #creating rectangular kernel  
dilation = cv2.dilate(roi, rect_kernel) #dilating thresholded image
cv2.waitKey(0)

contours_, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #fincing contours
im3 = roi.copy() #creating copy of the image

for cnt in contours_: 
    x, y, w, h = cv2.boundingRect(cnt) 

    rect = cv2.rectangle(im3, (x, y), (x + w, y + h), (0, 255, 0), 2) #drawing rectangle on copied image
    cropped = im3[y:y + h, x:x + w] #cropping the image for input to ocr 
    # applying tesseract-ocr
    text = pytesseract.image_to_string(cropped,lang='eng',config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 --psm 7')
    if text == '':
        continue
    printf(text)