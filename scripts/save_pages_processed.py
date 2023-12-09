# For pages processed, save the relevant images so we can push them to GitHub.

from joblib import Parallel, delayed
from pdf2image import convert_from_path
import os
import requests
import psycopg2

raw_prefix = 'https://raw.githubusercontent.com/yongish/question-parsing/main/'
raw_output_dir = '../exercises_raw'

password = os.environ.get('DB_PASSWORD')
conn = psycopg2.connect(database="postgres", user="postgres",
                        password=password, host="localhost", port="5432")
columns = ["source",
           "page_number",
           "exercise_type_id",
           "page_url",
           "second_last_page_url",
           "last_page_url"]
cur = conn.cursor()
cur.execute("SELECT {} FROM fill_blanks".format(','.join(columns)))
rows = cur.fetchall()

# for i, row in enumerate(rows):
def process(i, row):
    print(i, row)
    source = row[0]
    page_number = row[1]
    exercise_type_id = row[2]
    page_url = row[3]
    second_last_page_url = row[4]

    response = requests.get(page_url)
    print(page_url, response.status_code)
    if response.status_code != 200:
        pdf_filename = os.path.join('../pdfs', f'{source}.pdf')
        pages = convert_from_path(pdf_filename, 300)

        output_dirname = os.path.join(raw_output_dir, source)

        page_processed_name = 'duan' if exercise_type_id == 0 else 'xuan'
        page_processed_filename = os.path.join(
            output_dirname, 'page_processed_{}.jpg'.format(page_processed_name))
        pages[page_number - 1].save(page_processed_filename, 'JPEG')

    response = requests.get(second_last_page_url)
    print(second_last_page_url, response.status_code)
    if response.status_code != 200:
        second_last_page_filename = os.path.join(
            output_dirname, 'second_last_page.jpg')
        pages[-2].save(second_last_page_filename, 'JPEG')
        last_page_filename = os.path.join(output_dirname, 'last_page.jpg')
        pages[-1].save(last_page_filename, 'JPEG')
    print()

Parallel(n_jobs=8)(delayed(process)(i, row) for i, row in enumerate(rows))
