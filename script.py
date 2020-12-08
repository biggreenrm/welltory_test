import json
from jsonschema import validate
import os

""""Это все файлы json"""
path_event = "./event/"
list_events = os.listdir(path=path_event)
print(len(list_events))
"""Это все файлы схем"""
path_schema = "./schema/"
list_schemas = os.listdir(path=path_schema)

# для log'a используется множество, чтобы избежать возможного дублирования строк
log = set() 

# тут начинается основная процедура прогона json-файлов через соответствующие схемы
# я прошу прощения за такое неприличное количество уровней вложенности и обязательно отрефакторю этот момент на досуге
# это не составит труда

# по очереди читается каждый файл json
for event in list_events:
    event_file = path_event + event
    with open(event_file, 'r') as f:
        data = json.loads(f.read())

        # попытка найти соответствующую схему
        try:
            if data.get("event"):
                schema_needed = data["event"]
                list_schemas = [schema.rstrip('.schema') for schema in list_schemas]

                # сценарий для случая, если схема найдена
                if schema_needed in list_schemas:
                    schema_needed = schema_needed + '.schema'
                    schema_adress = "./schema/" + schema_needed

                    # схема считывается, происходит валидация
                    # в случае ошибки - она добавляется в log
                    with open(schema_adress, 'r') as file:
                        schema_map = json.loads(file.read())
                        try:
                            validate(data['data'], schema_map)
                            log.add(f"*[{event_file}]* Все ок")
                        except Exception as err:
                            log.add(f"*[{event_file}]* {err.message}")

                # сценарий для случая, если подходящая схема не найдена            
                else:
                    log.add(f"*[{event_file}]* Необходимая схема не может быть определена: для данного типа 'event' нет подходящей схемы")

        # сценарий для случая, если подходящую схему нельзя найти (тип не указан)            
        except:
            log.add(f"*[{event_file}]* Необходимая схема не может быть определена: тип 'event' не указан в файле")


""" Из задания невозможно досконально определить требования к тому, как должны выглядеть ошибки для не разработчиков, но уверен они знают
английский и типовые ошибки будут для них понятны. Если описание нужно расширить, то первое, что приходит на ум - создать словарь с
типовыми фразами, где ключи - это то, что есть в логе на данный момент, а значения - расширенное описание с переводом. Проитерироваться и
сделать replace для совпадений. Можно и на этапе записи в множество это сделать, тут как уже сеньоры попросят. """

# запись log'а в файл
with open('log.txt', 'a') as f:
    for i in log:
        row = i + '\n'
        f.write(row)