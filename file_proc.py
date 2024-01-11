# # https://pylot.me/article/35-rabota-s-zip-arhivami-s-pomoshyu-python/#
from zipfile import ZipFile
#
# # Files to compress
# files = [r'test.py', r'test1.py']
# # Path to save the zip file
# save_to = r"test.zip"
#
# with ZipFile('test.zip', 'w') as zip:
#     for file in files:
#         zip.write(file)
#
# import zipfile
#
# with zipfile.ZipFile("sample_pwd.zip", mode="r") as archive:
#     archive.setpassword(b"secret")
#     for file in archive.namelist():
#         print(file)
#         print("-" * 20)
#         for line in archive.read(file).split(b"\n"):
#             print(line)

from zipfile import ZipFile


class Files:
    def __init__(self):
        self.local_files = None
        self.global_files = None
        with ZipFile("token.zip", mode="r") as archive:
            archive.setpassword(b"1234")
            self.token = archive.read("token.txt")
            print(self.token)


files = Files()
