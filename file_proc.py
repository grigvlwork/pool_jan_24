# https://pylot.me/article/35-rabota-s-zip-arhivami-s-pomoshyu-python/#
from zipfile import ZipFile

# Files to compress
files = [r'test.py', r'test1.py']
# Path to save the zip file
save_to = r"test.zip"

with ZipFile('test.zip', 'w') as zip:
    for file in files:
        zip.write(file)