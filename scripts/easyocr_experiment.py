from pdf2image import convert_from_path
import cv2
import numpy as np
import easyocr
import io

# For each PDF file, 
# 1. Chinese OCR.
# 2. Find '短文填空'.
# 3. 
# 2. English OCR.
# Save the processed img, 2nd last page, last page. 
# 

reader = easyocr.Reader(['ch_sim','en'])
def getWordList(image):
  # imgByteArr = io.BytesIO()
  # image.save(imgByteArr, format=image.format)
  # imgByteArr = imgByteArr.getvalue()
  # words = reader.readtext(imgByteArr, detail=0)
  words = reader.readtext(image, detail=0)
  return words

file = '2015-P6-Prelims-Chinese-Raffles-Girls-4.pdf'
image = convert_from_path(file, dpi=300)[0]

image = np.array(image)
thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)[1]

median = cv2.medianBlur(thresh, 5)

ocr_string = getWordList(median)

# ocr_string = ocr_string.split('从括号中选出最适当的词话。')[1]
# ocr_string = ocr_string.split('一一')[0]
# ocr_string = ocr_string.split('-一')[0]
print(ocr_string)
cv2.imshow('median', median)
cv2.waitKey()


