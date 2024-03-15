from pathlib import Path
from pdf2image import convert_from_path
import datetime
import easyocr
import io
import os
import PyPDF2


from joblib import Parallel, delayed

reader = easyocr.Reader(['ch_sim','en'])
def getWordList(image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  words = reader.readtext(imgByteArr, detail=0)
  return words


input_dir = './pdfs'
# for i, file in enumerate(os.listdir(input_dir)):
def process(i, file):
  filename_no_extension, file_extension = os.path.splitext(file)
  if file_extension != '.pdf':
    return

  print(f'index: {i} STARTED at {datetime.datetime.now()}. file: {file}')

  filepath = os.path.join(input_dir, file)
  pdffile = open(filepath, 'rb')
  pdfReader = PyPDF2.PdfReader(pdffile)
  totalPages = len(pdfReader.pages)

  #
  # filename = '2015-P6-Prelims-Chinese-CHIJ.pdf'

  output_folder = os.path.join('raw', filename_no_extension)
  #if os.exists(output_folder):
  # return
  Path(output_folder).mkdir(parents=True, exist_ok=True)

  numFiles = len([name for name in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, name))])
  print(f'No. of files in {output_folder} :{numFiles}')
  print(f'Total pages in {filepath} :{totalPages}')

  if numFiles == totalPages - 1:
    return

  images = convert_from_path(filepath, dpi=300)
  for page_number, image in enumerate(images[1:]):
    words = getWordList(image)
    with open(os.path.join(output_folder, f'page{page_number + 1}.txt'), 'w') as f:
      for word in words:
        f.write(f'{word}\n')
  
  print(f'index: {i} ENDED at {datetime.datetime.now()}. file: {file}')

Parallel(n_jobs=8)(delayed(process)(i, file) for i, file in enumerate(os.listdir(input_dir)))
