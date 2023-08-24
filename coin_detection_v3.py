#%%
import cv2
import numpy as np
%matplotlib inline

#%%
def get_radius(circles):    
    radii = []
    for i in range(len(circles[0])):
        radii.append(circles[0][i][2])
    return radii

#%%
def av_pix(img, circles,size):
    av_value = []
    for coords in circles[0,:]:
        col = np.mean(img[coords[1]-size:coords[1]+size, coords[0]-size:coords[0]+size])
        av_value.append(col)
    return av_value

#%%

image = cv2.imread('/Users/Giovanni/Documents/Python/The_Complete_Python_Programmer_Bootcamp/Resources/3. Capstone/capstone_coins.png')
imgray = cv2.imread('/Users/Giovanni/Documents/Python/The_Complete_Python_Programmer_Bootcamp/Resources/3. Capstone/capstone_coins.png', cv2.IMREAD_GRAYSCALE)
blurr = cv2.GaussianBlur(imgray,(5,5),0)



circles = cv2.HoughCircles(blurr, cv2.HOUGH_GRADIENT, 0.9, 120, param1=50, param2=27, minRadius=60, maxRadius=120)


circles = np.uint16(np.around(circles))

radii = get_radius(circles)
print(radii)

bright_values = av_pix(image,circles,20)
print(bright_values)
#%%
values = []
for a,b in zip(bright_values,radii):
    if a > 151 and b > 101:
        values.append(10)
    elif a > 151 and b < 101:
        values.append(5)
    elif a < 151 and b > 113:
        values.append(2)
    elif a < 151 and b < 113:
        values.append(1)
print(values)
#%%
count = 0
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)
    cv2.putText(image, str(values[count]) + 'p', (i[0],i[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)
    count += 1
cv2.putText(image, 'Estimated Total Value: ' + str(sum(values)) + 'p', (200,100), cv2.FONT_HERSHEY_SIMPLEX, 1.3, 255)
cv2.imshow('detected circles',image)
cv2.waitKey(0)
cv2.destroyAllWindows()



# %%
radius = []
for coords in circles[0,:]:
    radius.append(coords[2])
    print(coords)
print(radius)

