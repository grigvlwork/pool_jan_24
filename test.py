# https://ramziv.com/article/2
import yadisk

token = ''
y = yadisk.YaDisk(token=token)
# print(y.check_token())  # Проверим токен
# y.mkdir('files/test')
# y.upload("test.py", "files/test/test.py")
# print('Содержимое папки "test":\n')
# for item in y.listdir('/files/'):
#     print(f"Название: {item['name']}")
#     print(f'Размер: {item["size"]} байт')
#     print(f"Тип файла: {item['type']}")
#     print(f"Тип документа: {item['media_type']}")
#     print(f"Дата создания: {item['created']}\n")

y.download('/files/test/test.py', 'test1.py')