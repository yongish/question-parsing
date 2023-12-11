from pathlib import Path
from pdf2image import convert_from_path
import datetime
import easyocr
import io
import os

from joblib import Parallel, delayed
# def process(i):
#     return i * i
# results = Parallel(n_jobs=2)(delayed(process)(i) for i in range(10))

reader = easyocr.Reader(['ch_sim','en'])
def getWordList(image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  words = reader.readtext(imgByteArr, detail=0)
  return words


# for i, file in enumerate(os.listdir(input_dir)):
def process(i, file):
  print(f'{datetime.datetime.now()}. file: {file}. index:{i}')

  # todo: Skip files that have already been seen.
  filename = os.fsdecode(file)

  #
  # filename = '2015-P6-Prelims-Chinese-CHIJ.pdf'

  filename_no_extension = Path(filename).stem
  output_folder = os.path.join('raw', filename_no_extension)
  Path(output_folder).mkdir(parents=True, exist_ok=True)

  images = convert_from_path(os.path.join(input_dir, filename), dpi=500)
  for page_number, image in enumerate(images[1:]):
    words = getWordList(image)
    with open(os.path.join(output_folder, f'page{page_number + 1}.txt'), 'w') as f:
      for word in words:
        f.write(f'{word}\n')

input_dir = './pdfs'
Parallel(n_jobs=8)(delayed(process)(i, file) for i, file in enumerate(os.listdir(input_dir)))

