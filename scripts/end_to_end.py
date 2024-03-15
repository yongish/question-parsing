from pathlib import Path
from pdf2image import convert_from_path
import datetime
import easyocr
import io
import os
import PyPDF2


from joblib import Parallel, delayed

reader = easyocr.Reader(['ch_sim','en'])

def ocr(i, file):
  def getWordList(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    words = reader.readtext(imgByteArr, detail=0)
    return words

  def cleanImage(image):
    image = np.array(image)
    thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)[1]
    median = cv2.medianBlur(thresh, 5)
    return median
  
  filename_no_extension, file_extension = os.path.splitext(file)
  if file_extension != '.pdf':
    return

  print(f'index: {i} STARTED at {datetime.datetime.now()}. file: {file}')

  input_dir = './pdfs'
  filepath = os.path.join(input_dir, file)
  pdffile = open(filepath, 'rb')
  pdfReader = PyPDF2.PdfReader(pdffile)
  totalPages = len(pdfReader.pages)

  #
  # filename = '2015-P6-Prelims-Chinese-CHIJ.pdf'

  output_folder = os.path.join('raw', filename_no_extension)
  if os.exists(output_folder):  # Already exists.
    return
  Path(output_folder).mkdir(parents=True, exist_ok=True)

  numFiles = len([name for name in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, name))])
  print(f'No. of files in {output_folder} :{numFiles}')
  print(f'Total pages in {filepath} :{totalPages}')

  if numFiles == totalPages - 1:
    return

  images = convert_from_path(filepath, dpi=300)
  for page_number, image in enumerate(images[1:]):
    words = getWordList(cleanImage(image))
    with open(os.path.join(output_folder, f'page{page_number + 1}.txt'), 'w') as f:
      for word in words:
        f.write(f'{word}\n')
  
  print(f'index: {i} ENDED at {datetime.datetime.now()}. file: {file}')
  
  return output_folder

# todo: Need to record which PDFs were found to contain a particular exercise, and which ones were not.
def duan(raw_dir):
  print(i, name_dir)

  page_dir = os.path.join(raw_dir, name_dir)

  my_file = Path(os.path.join(raw_output_dir, name_dir, 'answer.pdf'))
  if my_file.is_file(): # Already processed.
    csvwriter.writerow([name_dir, True]) 
    return

  # Create this directory.
  output_dirname = os.path.join(raw_output_dir, name_dir)
  Path(output_dirname).mkdir(parents=True, exist_ok=True)

  # 1. Copy original PDF file.
  pdf_filename = os.path.join('./pdfs', f'{name_dir}.pdf')
  shutil.copyfile(pdf_filename, os.path.join(output_dirname, f'{name_dir}.pdf'))

  # 2. Save last 2 pages as a PDF file. Assume they are the answer key. NOT ALWAYS TRUE.
  inputpdf = PdfReader(open(pdf_filename, "rb"))
  output = PdfWriter()
  output.add_page(inputpdf.pages[-2])
  output.add_page(inputpdf.pages[-1])
  with open(os.path.join(output_dirname, "answer.pdf"), "wb") as outputStream:
    output.write(outputStream)

  # 3. Copy last 2 pages to output directory, for possible GPT training.
  num_files = len(os.listdir(page_dir))
  shutil.copyfile(os.path.join(page_dir, f'page{num_files-1}.txt'), os.path.join(output_dirname, '2ndlast.txt'))
  shutil.copyfile(os.path.join(page_dir, f'page{num_files}.txt'), os.path.join(output_dirname, 'last.txt'))

  found = False
  for page_filename in os.listdir(page_dir):
    with open(os.path.join(page_dir, page_filename)) as f:
      contents = f.read()
      if '短文填空' in contents:
        found = True
        page_number = int(page_filename.split('page')[1].split('.txt')[0])

        # 4. Write current file.
        with open(os.path.join(output_dirname, page_filename), 'w') as out:
          out.write(contents)

        # 5. Write current image.
        pages = convert_from_path(pdf_filename, 300)
        pages[page_number].save(os.path.join(output_dirname, 'page-processed.jpg'), 'JPEG')

        break 

  print(found)
  

# for i, file in enumerate(os.listdir(input_dir)):
def process(i, file):
  folder = ocr(i, file)
  
  # 短文填空
  duan(folder)
  
  # Get answers too.
  
  # Write to local DB.
  
  # 选词填空
  

Parallel(n_jobs=8)(delayed(process)(i, file) for i, file in enumerate(os.listdir(input_dir)))
