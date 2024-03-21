from pathlib import Path
from pdf2image import convert_from_path
import os
from joblib import Parallel, delayed

# Split the PDF files to png.

raw_output_dir = '../pngs_raw'
raw_dir = '../raw'

dir_list = [f for f in os.listdir(raw_dir) if not f.startswith('.')]
# for i, name_dir in enumerate(dir_list):
# for i, name_dir in enumerate(['2015-P6-Prelims-Chinese-Henry-Park']):
# for i, name_dir in enumerate(['P6-Chinese-SA2-2007-Nanyang']):
def process(i, name_dir):
  print('{}, {} of {}'.format(name_dir, i, len(dir_list)))

  output_dirname = os.path.join(raw_output_dir, name_dir)
  # Create this directory.
  Path(output_dirname).mkdir(parents=True, exist_ok=True)
  
  # Save last 2 pages as image files. Assume they are the answer key, which isn't always true.
  pdf_filename = os.path.join('../pdfs', f'{name_dir}.pdf')
  pages = convert_from_path(pdf_filename, 300)
  for j, page in enumerate(pages):
    page_filename = os.path.join(output_dirname, 'page{}.png'.format(j + 1))
    page.save(page_filename, 'PNG')
  
Parallel(n_jobs=8)(delayed(process)(i, file) for i, file in enumerate(dir_list))
