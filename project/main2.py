# import numpy as np
# import cv2
# from PIL import Image, ImageFont, ImageDraw
# import pytesseract as tess


# def preprocess(img):
# 	cv2.imshow("Input",img)
# 	blur = cv2.GaussianBlur(img, (5,5), 0)
# 	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
# 	sobelx = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
	

# 	ret, thresh = cv2.threshold(sobelx, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)


# 	return thresh


# def cleanPlate(plate):
#     print("CLEANING PLATE. . .")
#     gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)

#     _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
#     contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#     if contours:
#         areas = [cv2.contourArea(c) for c in contours]
#         max_index = np.argmax(areas)
#         max_cnt = contours[max_index]
#         max_cntArea = areas[max_index]

#         x,y,w,h = cv2.boundingRect(max_cnt)

#         if not ratioCheck(max_cntArea, w, h):
#             return plate, None

#         cleaned_final = thresh[y:y+h, x:x+w]

#         return cleaned_final, [x,y,w,h]

#     else:
#         return plate, None


# def extract_contours(thresh):
#     element = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 5))
#     morph = thresh.copy()
#     cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, element, morph)


#     contours, hierarchy = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#     return contours

# def ratioCheck(area, width, height):
# 	ratio = float(width) / float(height)

# 	aspect = 4.7
# 	min = 1*aspect*1  # minimum area
# 	max = 250*aspect*250  # maximum area

# 	rmin = 2
# 	rmax = 5

# 	if (area < min or area > max) or (ratio < rmin or ratio > rmax):
# 		return False
# 	return True


# def putText(img, x,y, text):
# 	fontpath = "font/THSarabunNew.ttf"
# 	font = ImageFont.truetype(fontpath, 48)
# 	img_pil = Image.fromarray(img)
# 	draw = ImageDraw.Draw(img_pil)
# 	draw.text((x, y),  text, font = font, fill=(0,255,0))
# 	img = np.array(img_pil)

# 	return img


# def cleanAndRead(img, contours):
#     for i, cnt in enumerate(contours):
#         min_rect = cv2.minAreaRect(cnt)
#         x, y, w, h = cv2.boundingRect(cnt)
#         plate_img = img[y:y+h, x:x+w]
#         clean_plate, rect = cleanPlate(plate_img)
#         if rect is not None:
#             xt, yt, wt, ht = rect
#             x, y, w, h = x+xt, y+yt, wt, ht

#             plate_im = Image.fromarray(clean_plate)
#             text = tess.image_to_string(plate_im, lang='Thai')
            
#             if text:
#                 print("Detected Text: ", text)
#                 img = cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
#                 img = putText(img, x, y-h, text)
#                 cv2.imshow("Detected Plate", img)
#                 break
#                 cv2.waitKey(0)
                



# if __name__ == '__main__':
# 	print("DETECTING PLATE . . .")

# 	img = cv2.imread("img/d.jpg")
# 	img = cv2.resize(img, (512,256))
# 	print(cv2.__version__)
 
# 	thresh = preprocess(img)
# 	contours = extract_contours(thresh)

# 	cleanAndRead(img, contours)
# 	cv2.waitKey(0)

import requests
import openpyxl
from datetime import datetime


url = "https://api.aiforthai.in.th/lpr-v2"
payload = {'crop': '1', 'rotate': '1'}
files = {'image':open('img/thai3.jpg', 'rb')}
 
headers = {
    'Apikey': "DLKqXKynUWdG6i2FBUNdutFio0MIMYgD",
    }
 
response = requests.post( url, files=files, data = payload, headers=headers)
 
print(response.json()[0]['lpr'])



# Open the workbook (replace filename with the name of your Excel file)
workbook = openpyxl.load_workbook(filename="plate.xlsx")

# Select the worksheet (replace sheetname with the name of your worksheet)
worksheet = workbook["Sheet1"]
worksheet["A1"] = "Plate"
worksheet["B1"] = "Time-in"
worksheet["C1"] = "Time-out"

# Add some data to the worksheet
data = [response.json()[0]['lpr'], datetime.now()]
worksheet.append(data)

# Save the workbook
workbook.save(filename="plate.xlsx")