# Old script to prepare files for manual correction. On 3/14/24, we decided to use a custom React
# admin app instead. Need a new script that combines this script with duan.py and xuan.py.
# Backend needs to rerun duan.py and xuan.py everytime an edit is made. 

from pathlib import Path
from pdf2image import convert_from_path
from PyPDF2 import PdfWriter, PdfReader
import csv
import os
import shutil


raw_output_dir = './短文填空raw'
raw_dir = './raw'

csvfile = open('短文填空 procesed log.csv', 'w')
csvwriter = csv.writer(csvfile)

for i, name_dir in enumerate(os.listdir(raw_dir)):
  print(i, name_dir)

  page_dir = os.path.join(raw_dir, name_dir)

  my_file = Path(os.path.join(raw_output_dir, name_dir, 'answer.pdf'))
  if my_file.is_file():
    csvwriter.writerow([name_dir, True]) 
    continue

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
  csvwriter.writerow([name_dir, found]) 

csvfile.close()
