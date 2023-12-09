# 3/12/24: Apparently pytesseract is less accurate than easyOCR.
# Will go back to easyOCR instead. May try the image processing before OCR.
# Will have to try paid services if easyOCR isn't good enough.

from pdf2image import convert_from_path
import cv2
import pytesseract
import numpy as np

# For each PDF file, 
# 1. Chinese OCR.
# 2. Find '短文填空'.
# 3. 
# 2. English OCR.

file = '2015-P6-Prelims-Chinese-Raffles-Girls-4.pdf'
image = convert_from_path(file, dpi=300)[0]
image = np.array(image)
thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)[1]

x, y, w, h = cv2.boundingRect(thresh)
print('RECTANGLE')
print(x, y, w, h)


median = cv2.medianBlur(thresh, 5)
# ocr_string = pytesseract.image_to_string(median, lang='chi_sim', config='--psm 6')
ocr_string = pytesseract.image_to_string(median, lang='chi_sim')
ocr_string = ocr_string.split('从括号中选出最适当的词话。')[1]
ocr_string = ocr_string.split('一一')[0]
ocr_string = ocr_string.split('-一')[0]
print(ocr_string)
cv2.imshow('median', median)
cv2.waitKey()



# print(pytesseract.image_to_string(image, lang='chi_sim'))
# print(pytesseract.image_to_string(image, lang='eng'))
# Match with regex.
# re.match('短文*空', )

  
# Should use 'en' only to detect answers.
# Detect first question e.g. 'Q11', then parse out the answers.
# Need to record in CSV file which papers were processed successfully, and which ones were not.
# Parse answers.
