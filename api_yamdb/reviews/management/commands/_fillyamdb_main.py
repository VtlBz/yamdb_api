import csv
import logging
import os

from django.apps import apps
from reviews.management.commands import _fillyamdb_input_config as conf

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

EXIT_COMMANDS_LIST: tuple = ('no', 'n', 'нет', 'н', 'q', 'quit', 'exit',)
CONTINUE_COMMANDS_LIST: tuple = ('yes', 'y', 'да', 'д',)

ERROR_MESSAGE_FILENOTFOUND: str = ('Ошибка обработки запроса. '
                                   'Файла с именем {} не существует '
                                   'в указанной директории.')
ERROR_MESSAGE_CONSTRAINT: str = ('Для корректной обработки импорта '
                                 'имя файла должно соответствовать '
                                 'указанному в таблице соответствия.')


def confirmation() -> None:
    print('Данный скрипт импортирует данные '
          'из .csv файлов в базу данных проекта.')
    for i, value in enumerate(conf.IMPORT_CONFIG, start=1):
        file_name = value[0]
        app_model = value[1]
        print(f'{i}. {file_name} --> {app_model}')
    print('Импорт будет произведён в указанном выше порядке и'
          'в соответствии со связью <имя_файла> --> <app_name>.<Model_name>')
    print('Проверьте соответствие имён файлов в каталоге '
          'на соответствие указанным выше, прежде чем продолжить.')

    while True:
        q = input('Подтвердить (yes/no)? ') or ''
        if q.lower() in CONTINUE_COMMANDS_LIST:
            break
        if q.lower() in EXIT_COMMANDS_LIST:
            raise SystemExit('Операция отменена пользователем')
        print('Ошибка! Команда не распознана!')
        print('Допустимые значения:')
        print(f'Подтвердить и продолжить - {CONTINUE_COMMANDS_LIST}')
        print(f'Отменить и выйти - {EXIT_COMMANDS_LIST}')


def get_file_path(folder_path, file_name) -> str:
    err_msg = ERROR_MESSAGE_FILENOTFOUND.format
    for root, dirs, files in os.walk(folder_path):
        if file_name in files:
            return str(os.path.join(root, file_name))
        logger.error(err_msg(file_name))
        raise SystemExit(ERROR_MESSAGE_CONSTRAINT)


def process_m2m_field(reader, _model_1, _model_2, file_name) -> None:
    next(reader)
    row_count = 0
    for row in reader:
        title = _model_1.objects.get(id=row[1])
        genre = _model_2.objects.get(id=row[2])
        title.genre.add(genre)
        title.save()
        row_count += 1
    logger.info(f'End processing file {file_name}, '
                f'imported {row_count} row(s).')


def process_table(reader, _model, file_name) -> None:
    header = next(reader)
    row_count = row_success = 0
    for row in reader:
        _object_dict = {key: value for key, value
                        in zip(header, row)}
        _, is_create = _model.objects.get_or_create(**_object_dict)
        row_count += 1
        if is_create:
            row_success += 1
    logger.info(f'End processing file {file_name}, '
                f'imported {row_count} row(s), '
                f'{row_success} successfully.')


def run(folder_path) -> None:
    _model = _model_1 = _model_2 = None
    for current_import in conf.IMPORT_CONFIG:
        file_name, app_model, m2m_flag = current_import
        app_name, model_name = app_model.split('.')
        file_path = get_file_path(folder_path, file_name)

        if m2m_flag == 1:
            model_1_name, model_2_name = model_name.split('_')
            logger.info('Start processing m2m field for '
                        f'{app_name}.{model_1_name} '
                        f'and {app_name}.{model_2_name}')
            _model_1 = apps.get_model(app_label=app_name,
                                      model_name=model_1_name)
            _model_2 = apps.get_model(app_label=app_name,
                                      model_name=model_2_name)
        else:
            logger.info(f'Start processing model {app_name}.{model_name}')
            _model = apps.get_model(app_label=app_name, model_name=model_name)

        logger.info(f'Start processing file {file_name}')
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            if m2m_flag == 1:
                process_m2m_field(reader, _model_1, _model_2, file_name)
            else:
                process_table(reader, _model, file_name)
