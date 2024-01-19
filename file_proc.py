import os
import yadisk
import shutil
import glob
from py7zr import SevenZipFile as zf7


class Files:
    def __init__(self):
        self.local_files = None
        self.global_files = None
        self.token = None
        self.load_token()
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

    def load_token(self):
        with zf7('config', 'r', password='config') as archive:
            t = archive.read(['config.tmp'])
            self.token = t['config.tmp'].read().decode('utf-8')

    def get_id_from_url(self, url):
        return url[url.rfind('/') + 1:]

    def get_filename_from_code(self, code):
        il = code.find('open(') + 5
        if il < 5:
            return ''
        if code.find(',', il + 1) > 0:
            ir = min(code.find(',', il + 1), code.find(')', il + 1))
        else:
            ir = code.find(')', il + 1)
        res = code[il:ir].replace('"', '').replace("'", "").strip()
        return res

    # def get_zip_name(self, name):
    #     return name[:name.rfind('.')] + '.zip'

    def get_only_name(self, name):
        return name[:name.rfind('.')]

    def get_local_file(self, id, name):
        if id in self.local_files:
            try:
                file_name = f'{os.getcwd()}/files/{id}/{self.get_only_name(name)}'
                if os.path.isfile(file_name):
                    with zf7(file_name, "r") as archive:
                        if name in archive.getnames():
                            archive.extract(path=os.getcwd(), targets=[name])
                            return 1
                        else:
                            return -1
                else:
                    return -1
            except Exception:
                return -1

    def get_global_file(self, id, name):
        if id in self.global_files:
            try:
                file_name = f'/files/{id}/{self.get_only_name(name)}'
                if self.y.is_file(file_name):
                    if not os.path.isdir(os.getcwd() + '/files'):
                        os.mkdir(os.getcwd() + '/files')
                    os.mkdir(os.getcwd() + f'/files/{id}')
                    self.y.download(file_name, os.getcwd() + file_name)
                    self.local_files.append(id)
                    self.get_local_file(id, name)
                    return 1
                else:
                    return -1
            except Exception:
                return -1

    def save_file(self, id, full_file_name):
        filename = self.get_only_name(os.path.basename(full_file_name))
        file_name = os.getcwd() + f'/files/{id}/{filename}'
        if self.local_files is not None and id in self.local_files and \
                os.path.isfile(file_name):
            with zf7(file_name, "r") as archive:
                if os.path.basename(full_file_name) in archive.getnames():
                    return 1
                else:
                    try:
                        shutil.copy(full_file_name, os.getcwd())
                        with zf7(file_name, "a") as archive_new:
                            archive_new.write(os.path.basename(full_file_name))
                        if not self.y.is_dir(f'/files/{id}/'):
                            self.y.mkdir(f'/files/{id}/')
                        self.y.upload(file_name, f'/files/{id}/{filename}', overwrite=True)
                        os.remove(os.getcwd() + '/' + filename)
                    except Exception:
                        return -1
        if not os.path.isdir(os.getcwd() + '/files'):
            os.mkdir(os.getcwd() + '/files')
        if not os.path.isdir(os.getcwd() + f'/files/{id}'):
            os.mkdir(os.getcwd() + f'/files/{id}')
        try:
            shutil.copy(full_file_name, os.getcwd())
            with zf7(file_name, 'w') as archive:
                archive.write(os.path.basename(full_file_name))
            if self.local_files is None:
                self.local_files = []
            self.local_files.append(id)
            if self.global_files is not None and id in self.global_files:
                if self.y.is_file(f'/files/{id}/{filename}'):
                    return 1
            if not self.y.is_dir(f'/files/{id}/'):
                self.y.mkdir(f'/files/{id}/')
            self.y.upload(file_name, f'/files/{id}/{filename}')
            os.remove(os.getcwd() + '/' + filename)
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
