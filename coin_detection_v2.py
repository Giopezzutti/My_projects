#%%
from PIL import Image, ImageEnhance

im = Image.open('/Users/Giovanni/Documents/Python/The_Complete_Python_Programmer_Bootcamp/Resources/3. Capstone/capstone_coins.png')

enhancer = ImageEnhance.Brightness(im)

im_output = enhancer.enhance(0.6)
im_output.save('dark_coins.png')
#%%
import cv2
image = cv2.imread('/Users/Giovanni/Documents/Python/The_Complete_Python_Programmer_Bootcamp/Resources/3. Capstone/capstone_coins.png')
imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurr = cv2.GaussianBlur(imgray,(5,5),0)
thresh = cv2.threshold(imgray, 100, 255, cv2.THRESH_BINARY)[1]
cnts = cv2.findContours(blurr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# print(cnts)
# %%
cv2.imshow('Image',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
# %%
for c in cnts:
    print(len(c))
print(len(cnts))
# %%
image_bright = image + 60
# %%
imgray2 = cv2.cvtColor(image_bright, cv2.COLOR_BGR2GRAY)
thresh2 = cv2.threshold(imgray2, 110, 255, cv2.THRESH_BINARY)[1]
cnts2 = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# %%
