# https://ramziv.com/article/2
# import yadisk
#
# token = ''
# y = yadisk.YaDisk(token=token)
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

# y.download('/files/test/test.py', 'test1.py')

# https://education.yandex.ru/ege/task/0f1bb8de-fe34-40c1-a82e-8d012e8519dc

# https://education.yandex.ru/ege/task/aacb990b-df04-48ee-a3c5-5472a68fd379
# with open('27_A.txt', 'w', encoding='utf-8') as c:
# with open('27_B.txt', 'w', encoding='utf-8') as c:

# https://education.yandex.ru/ege/task/0f1bb8de-fe34-40c1-a82e-8d012e8519dc
# with open('9.ods', 'w', encoding='utf-8') as c:
# with open('9.csv', 'w', encoding='utf-8') as c:

# n_5 = 122
# n = int(n_5, 5)
# print(n)

from file_proc import Files

f = Files()
print(f.upload_solution('ebbc8b9f-d709-47ff-b8f4-2c2e99ccb13b'))
