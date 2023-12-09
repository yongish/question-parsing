"""
First try to ask GPT if it can
1. Format a 短文填空 passage in the image to 1 line per paragraph, and remove empty spaces.
2. Read the answer images, and add a "c" in front of the correct choice in each question in the 
formatted text. For example, if a question in the passage was "Q11 (1热情 2陌生 3熟悉 4奇怪)", and the
correct choice is "2", the text should be edited to "Q11(1热情c2陌生3熟悉4奇怪)".
"""
from openai import OpenAI
import base64

from PIL import Image

img = Image.open('./page_processed_duan.jpg')
img.show()

# def encode_image(image_path):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')

# page_processed = encode_image('./page_processed_duan.jpg')
# second_last_page = encode_image('./second_last_page.jpg')
# last_page = encode_image('./last_page.jpg')

# client = OpenAI()
# response = client.chat.completions.create(
#   model="gpt-4-vision-preview",
#   messages=[
#     {
#       "role": "system",
#       "content": [
#         {
#           "type": "text",
#           "text": f"""
#           The user prompt is a list of 3 images, which are pages from a Chinese language 
#           proficiency exam paper. The first image contains a 短文填空 passage, along with 
#           instructions on how to answer the questions. There may be other material that belong to 
#           other sections of the exam paper, which can be ignored. The second and third images may 
#           be the answer keys, and one of these images may contain the answers to the questions. 
#           Format the passage to 1 line per paragraph, remove empty spaces, and exclude the 
#           instructions on how to answer the questions. 
#           Read the answer images, and add a "c" in front of the correct choice in each question in 
#           the formatted text. For example, if a question in the passage was 
#           "Q11 (1热情 2陌生 3熟悉 4奇怪)", and the correct choice is "2", the text should be edited to 
#           "Q11(1热情c2陌生3熟悉4奇怪)". Notice that all spaces have been removed.
#           If the second and third images do not contain the answers to the passage, do not fill in
#           the answers.
#           Your response should contain only the text with the correct choices filled in. Don't 
#           include any other text, such as descriptions of your response. Here is an example 
#           response in triple single quotes '''老师发现王军很久了，感觉的确是聪明人。去上午宣读公文发现了。去上午宣读的Q12(1热情c2感兴趣3尴尬4生气)。不过，他的名模还是非常真挚，宣读着读者都感动。\n学术Q13(1可怜2感激c3充满4幸福)他咳嗽并摆放一些咨询的请求，意境对老王说Q14(1重点c2色斑3严肃4幽默)的审稿。学术对策署策应该得到反响，站进去Q15(1历史c2流通3感慨4讲解)时，学有所长的老王，初本不积囤自己的积累，充满热情，带领大家向擦洗作战，让他们一次次挑战高潮。\n听了学术说的话老师，表面一大人大感兴趣。他这种Q16(1害怕2渴望c3无聊4担心)的精神，确实感动倾听。'''
#           """
#         }
#       ]
#     },
#     {
#       "role": "user",
#       "content": [
#         {
#           "type": "image_url",
#           "image_url": {
#             "url": f"data:image/jpeg;base64,{page_processed}"
#           },
#         },
#         {
#           "type": "image_url",
#           "image_url": {
#             "url": f"data:image/jpeg;base64,{second_last_page}"
#           },
#         },
#         {
#           "type": "image_url",
#           "image_url": {
#             "url": f"data:image/jpeg;base64,{last_page}"
#           },
#         },
#       ],
#     }
#   ],
#   # max_tokens=300,
# )
# # print(response.choices[0].message.content)
# print(response)
