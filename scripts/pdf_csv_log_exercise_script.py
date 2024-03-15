import csv
import os

# Script to implement logic to record which PDFs were found to contain a particular exercise, and
# which ones were not. Will use this logic inside duan.py and xuan.py.

csvfile = open('短文填空 procesed log.csv', 'w')
csvwriter = csv.writer(csvfile)

page_dir = '2015-P6-Prelims-Chinese-Henry-Park'
full_page_dir = '../raw/2015-P6-Prelims-Chinese-Henry-Park'
found = False
for page_filename in os.listdir(full_page_dir):
  with open(os.path.join(full_page_dir, page_filename)) as f:
    contents = f.read()
    if '短文填空' in contents: 
      found = True
      break
    
csvwriter.writerow([page_dir, Found])
