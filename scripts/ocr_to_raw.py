# Convert Document AI JSON files to raw strings, and insert to fill_blanks table.

import csv
import json
import os
import psycopg2

gitlab_prefix = 'https://github.com/yongish/question-parsing/-/raw/main/'
raw_prefix = 'https://raw.githubusercontent.com/yongish/question-parsing/main/'
password = os.environ.get('DB_PASSWORD')
conn = psycopg2.connect(database="postgres", user="postgres",
                        password=password, host="localhost", port="5432")
cur = conn.cursor()

csvfile = open('procesed log yu wen ying yong.csv', 'w')
csvwriter = csv.writer(csvfile)


def insert(exam_name, page_number, raw_string, exercise_type_id):
    cur.execute(
        """
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
            exam_name,
            raw_prefix + 'pdfs/' + exam_name + '.pdf',
            int(page_number[4:]),
            raw_string,
            exercise_type_id,
            raw_prefix + 'exercises_raw/' + exam_name + '/page_processed_duan.jpg',
            raw_prefix + 'exercises_raw/' + exam_name + '/second_last_page.jpg',
            raw_prefix + 'exercises_raw/' + exam_name + '/last_page.jpg',
        )
    )
    conn.commit()


input_dir = '../ocr_output'
for exam_name in os.listdir(input_dir):
    exam_dir = os.path.join(input_dir, exam_name)
    print(exam_name)

    duan_found = False
    xuan_found = False
    for page_file in os.listdir(exam_dir):
        page_number = page_file.split('.')[0]
        with open(os.path.join(exam_dir, page_file), 'r') as f:
            raw_string = f.read()
            if '语文应用' in raw_string:
            # if '短文填空' in raw_string:
                duan_found = True
                insert(exam_name, page_number, raw_string, 0)
            # if '选词填空' in raw_string:
            #     xuan_found = True
            #     insert(exam_name, page_number, raw_string, 1)

    # csvwriter.writerow([exam_name, duan_found, xuan_found])
    csvwriter.writerow([exam_name, duan_found])

csvfile.close()
cur.close()
conn.close()
