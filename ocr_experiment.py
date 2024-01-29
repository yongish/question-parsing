from pdf2image import convert_from_path
import easyocr
import io

# reader = easyocr.Reader(['ch_sim','en'])
reader = easyocr.Reader(['en'])
def getWordList(image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  words = reader.readtext(imgByteArr, detail=0)
  return words

# file = './pdfs/2015-P6-Prelims-Chinese-Nanyang.pdf'
file = './pdfs/2015-P6-Prelims-Chinese-Raffles-Girls.pdf'
images = convert_from_path(file, dpi=300)
print(getWordList(images[18]))

# Should use 'en' only to detect answers.
# Detect first question e.g. 'Q11', then parse out the answers.
# Need to record in CSV file which papers were processed successfully, and which ones were not.
