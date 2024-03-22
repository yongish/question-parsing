# Concat extraneous directories from Document AI.
# Then delete empty directories.
# Then keep only document.text in each JSON file.

from pathlib import Path
import os
import json

input_dir = '../ocr_output'
for exam_name in os.listdir(input_dir):
  
  exam_dir = os.path.join(input_dir, exam_name)
  for file in os.listdir(exam_dir):
    if '.json' in file:
      file_name = os.path.join(exam_dir, file)
      document = json.load(open(file_name))
      if 'text' in document:
        output_file = file_name[:-4] + 'txt'
        print(output_file)
        with open(output_file, 'w') as f:
          f.write(document['text'])
    
    # exam_dir = os.path.join(input_dir, exam_name)
    # for file in os.listdir(exam_dir):
    #   curr_name = os.path.join(exam_dir, file)
    #   new_name = os.path.join(exam_dir, file.split('-')[0] + '.json')
    #   os.rename(curr_name, new_name)

# def delete_empty_directories(path):
#     """Recursively delete empty directories."""
#     for root, dirs, files in os.walk(path, topdown=False):
#         for dir in dirs:
#             dir_path = os.path.join(root, dir)
#             if not os.listdir(dir_path):
#                 os.rmdir(dir_path)
# delete_empty_directories(input_dir)


# for exam_name in os.listdir(input_dir):
#     exam_dir = os.path.join(input_dir, exam_name)
#     single_subdir = os.path.join(exam_dir, os.listdir(exam_dir)[0])

#     for subdir in os.listdir(single_subdir):
#       page_name_dir = os.path.join(single_subdir, subdir)
#       page_name_file = os.listdir(page_name_dir)[0]
#       page_number = page_name_file.split('-')[0]
#       page_name_json = os.path.join(page_name_dir, page_name_file)

#       # Move this file 2 levels higher.
#       p = Path(page_name_json).absolute()
#       parent_dir = p.parents[2]
#       p.rename(parent_dir / p.name)
