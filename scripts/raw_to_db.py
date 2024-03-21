from pathlib import Path
from pdf2image import convert_from_path
import csv
import os
import psycopg2

# Need a script just for parsing the string to JSON.

# Find 短文填空.
# Write to CSV file.
# Write to DB.

csvfile = open('procesed log.csv', 'a')
csvwriter = csv.writer(csvfile)
raw_output_dir = '../exercises_raw'
raw_dir = '../raw'

# https://gitlab.com/yongish/question-parsing/-/raw/main/raw/2015-P6-Prelims-Chinese-Methodist-Girls/page10.txt
gitlab_prefix = 'https://gitlab.com/yongish/question-parsing/-/raw/main/'

password = os.environ.get('DB_PASSWORD')
conn = psycopg2.connect(database="postgres", user="postgres",
                        password=password, host="localhost", port="5432")
cur = conn.cursor()

dir_list = [f for f in os.listdir(raw_dir) if not f.startswith('.')]
for i, name_dir in enumerate(dir_list):
# for i, name_dir in enumerate(['2015-P6-Prelims-Chinese-Henry-Park']):
# for i, name_dir in enumerate(['P6-Chinese-SA2-2007-Nanyang']):
  print('{}, {} of {}'.format(name_dir, i, len(dir_list)))

  output_dirname = os.path.join(raw_output_dir, name_dir)

  # Create this directory.
  Path(output_dirname).mkdir(parents=True, exist_ok=True)
  
  # Save last 2 pages as image files. Assume they are the answer key, which isn't always true.
  pdf_filename = os.path.join('../pdfs', f'{name_dir}.pdf')
  pages = convert_from_path(pdf_filename, 300)
  second_last_page_filename = os.path.join(output_dirname, 'second_last_page.jpg')
  pages[-2].save(second_last_page_filename, 'JPEG')
  last_page_filename = os.path.join(output_dirname, 'last_page.jpg')
  pages[-1].save(last_page_filename, 'JPEG')
  
  duan_found = False
  xuan_found = False
  page_dir = os.path.join(raw_dir, name_dir)
  for page_filename in os.listdir(page_dir):
    page_path = os.path.join(page_dir, page_filename)
    with open(os.path.join(page_dir, page_filename)) as f:
      contents = f.read()
      page_number = int(page_filename.split('page')[1].split('.txt')[0])
      if '短文填空' in contents:
        duan_found = True
        page_processed_filename = os.path.join(output_dirname, 'page_processed_duan.jpg')
        pages[page_number].save(page_processed_filename, 'JPEG')
        cur.execute("""
          INSERT INTO fill_blanks (
            source,
            source_url,
            page_number,
            raw_string,
            exercise_type_id,
            page_url,
            second_last_page_url,
            last_page_url
          ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
          ON CONFLICT ON CONSTRAINT exercise_type DO NOTHING
          """,
          (
            name_dir,
            gitlab_prefix + page_path[3:],
            page_number,
            contents,
            0,
            gitlab_prefix + page_processed_filename[3:],
            gitlab_prefix + second_last_page_filename[3:],
            gitlab_prefix + last_page_filename[3:],
          )
        )
        conn.commit()

      if '选词填空' in contents:
        xuan_found = True
        page_processed_filename = os.path.join(output_dirname, 'page_processed_xuan.jpg')
        pages[page_number].save(page_processed_filename, 'JPEG')
        cur.execute("""
          INSERT INTO fill_blanks (
            source,
            source_url,
            page_number,
            raw_string,
            exercise_type_id,
            page_url,
            second_last_page_url,
            last_page_url
          ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
          ON CONFLICT ON CONSTRAINT exercise_type DO NOTHING
          """,
          (
            name_dir,
            gitlab_prefix + page_path[3:],
            page_number,
            contents,
            1,
            gitlab_prefix + page_processed_filename[3:],
            gitlab_prefix + second_last_page_filename[3:],
            gitlab_prefix + last_page_filename[3:],
          )
        )
        conn.commit()

  csvwriter.writerow([name_dir, duan_found, xuan_found]) 

csvfile.close()
cur.close()
conn.close()
