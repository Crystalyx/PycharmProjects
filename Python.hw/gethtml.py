from urllib.request import urlopen
import os

print('Write Url:')
html = input().replace(' ', '')
filepath = html
while filepath.find('/') != -1:
    filepath = filepath[filepath.find('/')+1:]
with urlopen(html) as h:
    if os.path.exists(html):
        os.remove(html)
    with open(filepath, 'a') as f:
        for html_bytes in h:
            f.write(html_bytes.decode('cp1251'))
