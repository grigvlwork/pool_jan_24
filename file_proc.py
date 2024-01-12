# # https://pylot.me/article/35-rabota-s-zip-arhivami-s-pomoshyu-python/#
# from zipfile import ZipFile
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
import zlib
import base64
import os
import yadisk
import shutil
import glob


class Files:
    def __init__(self):
        self.local_files = None
        self.global_files = None
        text = b'eJyrNIh3THcEAR8fswgXR8fiRCMw18W4LMC0yC0gxNPCO7csWDfV3zU/xyksxc/TO9HfyaUkGwD/6xHx'
        t = base64.b64decode(text)
        self.token = zlib.decompress(t).decode('utf-8')
        if os.path.isdir(os.getcwd() + '/files'):
            self.local_files = []
            for dirname, dirnames, filenames in os.walk(os.getcwd() + '/files'):
                # print path to all subdirectories first.
                for subdirname in dirnames:
                    self.local_files.append(subdirname)
        self.y = yadisk.YaDisk(token=self.token)
        for item in self.y.listdir('/files/'):
            if item['type'] == 'dir':
                if self.global_files is None:
                    self.global_files = []
                self.global_files.append(item['name'])

    def get_id_from_url(self, url):
        # https://education.yandex.ru/ege/task/aacb990b-df04-48ee-a3c5-5472a68fd379
        return url[url.rfind('/') + 1:]

    def get_filename_from_code(self, code):
        il = code.find('open(') + 5
        if il == -1:
            return ''
        ir = min(code.find(',', il + 1), code.find(')', il + 1))
        return code[il:ir].replace('"', '').replace("'", "").strip()

    def get_zip_name(self, name):
        return name[:name.rfind('.')] + '.zip'

    def get_only_name(self, name):
        return name[:name.rfind('.')]

    def get_local_file(self, id, name):
        if id in self.local_files:
            try:
                file_name = f'{os.getcwd()}/files/{id}/{self.get_zip_name(name)}'
                if os.path.isfile(file_name):
                    with ZipFile(file_name, mode="r") as archive:
                        if name in archive.filelist:
                            archive.extract(name, path=os.getcwd())
                            return 1
                        else:
                            return -1
                else:
                    return -1
            except Exception:
                # self.correct_output_lb.setText('Файл не найден')
                return -1

    def get_global_file(self, id, name):
        if id in self.global_files:
            try:
                file_name = f'/files/{id}/{self.get_only_name(name)}'
                file_name_zip = f'/files/{id}/{self.get_zip_name(name)}'
                if self.y.is_file(file_name):
                    if not os.path.isdir(os.getcwd() + '/files'):
                        os.mkdir(os.getcwd() + '/files')
                    os.mkdir(os.getcwd() + f'/files/{id}')
                    self.y.download(file_name, os.getcwd() + file_name_zip)
                    self.local_files.append(id)
                    self.get_local_file(id, name)
                    return 1
                else:
                    return -1
            except Exception:
                # self.correct_output_lb.setText('Файл не найден')
                return -1

    def save_file(self, id, full_file_name):
        file_name = os.getcwd() + f'/files/{id}/{self.get_only_name(os.path.basename(full_file_name))}'
        file_name_zip = os.getcwd() + f'/files/{id}/{self.get_zip_name(os.path.basename(full_file_name))}'
        if self.local_files is not None and id in self.local_files and \
                os.path.isfile(file_name_zip):
            with ZipFile(file_name, mode="r") as zip:
                if os.path.basename(full_file_name) in zip.filelist:
                    return 1
                else:
                    try:
                        shutil.copy(full_file_name, os.getcwd())
                        zip.write(os.path.basename(full_file_name))
                        if not self.y.is_dir(f'/files/{id}/'):
                            self.y.mkdir(f'/files/{id}/')
                        self.y.upload(file_name, f'/files/{id}/{file_name_zip}', overwrite=True)
                    except Exception:
                        return -1
        if not os.path.isdir(os.getcwd() + '/files'):
            os.mkdir(os.getcwd() + '/files')
        if not os.path.isdir(os.getcwd() + f'/files/{id}'):
            os.mkdir(os.getcwd() + f'/files/{id}')
        try:
            shutil.copy(full_file_name, os.getcwd())
            with ZipFile(file_name, 'w') as zip:
                zip.write(os.path.basename(full_file_name))
            if self.local_files is None:
                self.local_files = []
            self.local_files.append(id)
            if self.global_files is not None and id in self.global_files:
                if self.y.is_file(f'/files/{id}/{self.get_zip_name(os.path.basename(full_file_name))}'):
                    return 1
            if not self.y.is_dir(f'/files/{id}/'):
                self.y.mkdir(f'/files/{id}/')
            self.y.upload(file_name, f'/files/{id}/{self.get_zip_name(os.path.basename(full_file_name))}')
            # os.remove(os.getcwd() + f'/{os.path.basename(full_file_name)}')
            os.remove(full_file_name)
            if self.global_files is None:
                self.global_files = []
            self.global_files.append(id)
            return 1
        except Exception:
            return -1

files = Files()
# files.get_global_file('aacb990b-df04-48ee-a3c5-5472a68fd379', "27_A.txt")
# files.save_file('aacb990b-df04-48ee-a3c5-5472a68fd379',
#                  'C:/Users/grigorovich/Downloads/27_A.txt')
# print(files.get_id_from_url('https://education.yandex.ru/ege/task/aacb990b-df04-48ee-a3c5-5472a68fd379'))
