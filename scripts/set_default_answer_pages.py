# For pages processed, save the relevant images so we can push them to GitHub.

import os
import PyPDF2
import psycopg2

raw_prefix = 'https://raw.githubusercontent.com/yongish/question-parsing/main/'
raw_output_dir = '../exercises_raw'

password = os.environ.get('DB_PASSWORD')
conn = psycopg2.connect(database="postgres", user="postgres",
                        password=password, host="localhost", port="5432")
cur = conn.cursor()

cur.execute("SELECT source FROM fill_blanks")
rows = cur.fetchall()
for i, row in enumerate(rows):
    print(i, row)
    source = row[0]

    pdf_filename = os.path.join('../pdfs', f'{source}.pdf')
    pdfReader = PyPDF2.PdfReader(pdf_filename)
    totalPages = len(pdfReader.pages)

    cur.execute("UPDATE fill_blanks SET answer_page_number = %s WHERE source = %s", ( totalPages - 1, source,))
    conn.commit()

cur.close()
conn.close()
