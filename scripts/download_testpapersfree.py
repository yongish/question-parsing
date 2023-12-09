import requests
import urllib.request

host = 'https://www.testpapersfree.com/'
headers = {'User-agent': 'Mozilla/5.0'}
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

for page in range(47):
  r = requests.get(
    host + 'p6/?level=P6&year=%25&subject=Chinese&type=%25&school=%25&Submit=Show+Test+Papers&page=' + str(page),
    headers=headers
  )
  for line in r.text.split('\n'):
    if 'testpaperid=' in line and 'a href' in line:
      id = line.split('testpaperid=')[1].split('"')[0]
      r1 = requests.get(host + 'show.php?testpaperid=' + id, headers=headers)
      for line1 in r1.text.split('\n'):
        if '.pdf' in line1:
          id1 = line1.split('href="pdfs/')[1].split('"')[0]
          print(id1)
          urllib.request.urlretrieve(host + 'pdfs/' + id1, 'pdfs/' + id1)
