from pathlib import Path
from pdf2image import convert_from_path
from PyPDF2 import PdfWriter, PdfReader
import csv
import easyocr
import io
import os

# Assumes that an exercise is entirely contained in 1 page i.e. image.

reader = easyocr.Reader(['ch_sim','en'], gpu=False)
def getWordList(image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  words = reader.readtext(imgByteArr, detail=0)
  return words

def process_duan(file, output_folder, image, words, last2pages):
  # 1. Current image as raw text file.
  with open(os.path.join(output_folder, 'raw.txt'), 'w') as f:
    for word in words:
      f.write(f'{word}\n')
  
  # 2. Current image as JPEG file.
  image.save(os.path.join(output_folder, 'page-processed.jpg'))
  
  # 3. Last 2 pages as a PDF file. Assume they are the answer key.
  inputpdf = PdfReader(open(file, "rb"))
  output = PdfWriter()
  output.add_page(inputpdf.pages[-2])
  output.add_page(inputpdf.pages[-1])
  with open(os.path.join(output_folder, "answer.pdf"), "wb") as outputStream:
    output.write(outputStream)

  # 4. Last 2 pages as a raw text files, for possible GPT training.
  words = []
  for page in last2pages:
    words.append(getWordList(page))
  with open(os.path.join(output_folder, 'last2pages.txt'), 'w') as f:
    for word in words:
      f.write(f'{word}\n')


input_dir = './pdfs'
f = open('短文填空 procesed log.csv', 'a')
writer = csv.writer(f)

for file in os.listdir(input_dir):
  # todo: Skip files that have already been seen.
  filename = os.fsdecode(file)

  #
  filename = '2015-P6-Prelims-Chinese-CHIJ.pdf'

  filename_no_extension = Path(filename).stem
  output_folder = os.path.join('短文填空raw', filename_no_extension)
  if os.path.exists(os.path.join(output_folder, 'last2pages.txt')):
    continue
  Path(output_folder).mkdir(parents=True)

  
  images = convert_from_path(os.path.join(input_dir, filename), dpi=500)
  found = False
  # for image in images[1:]:
  for image in images[4:]:
    words = getWordList(image)
    for i, word in enumerate(words):
      if '短文填空' in word:
        # Process this words. Skip other images.
        process_duan(os.path.join(input_dir, filename), output_folder, image, words, images[-2:])
        writer.writerow([filename, True])
        found = True
        break
    
    if found:
      break
      
  if ~found:
    writer.writerow([filename, False])
    
  #
  break
 
f.close() 
  
  # filename_no_extension = Path(filename).stem
  # output_folder = './jpegs/' + filename_no_extension
  # Path(output_folder).mkdir(parents=True, exist_ok=True)
  # convert_from_path(
  #   os.path.join(input_dir, filename),
  #   dpi=500,
  #   output_folder=output_folder,
  #   fmt='jpeg',
  #   jpegopt={
  #     'quality': 100,
  #     'progressive': False,
  #     'optimize': False
  #   },
  #   output_file=filename_no_extension,
  #   grayscale=True
  # )
  
  
# pdf_pages.save('temp', "JPEG")
# pdf_pages.save()
# for i, page in pdf_pages:
#   print(page)
#   filename = f"./page_{i}.jpg"
#   page.save(filename, "JPEG")
