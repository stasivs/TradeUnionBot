import logging

import requests

from config import URL


def get_request_key() -> str:
    """Получаем ключ для последующих запросов."""
    pass


async def get_profcome_schedule(course_name: str) -> dict:
    """Получаем расписание приёма доков для института."""

    response = requests.get(f'{URL}/timetable/{course_name}')

    if response.status_code == 200:
        profcome_schedule = response.json()
        return profcome_schedule
    return {}


async def redact_profcome_schedule(institute_name: str, image_id: str) -> dict:
    """Редактируем расписание приёма доков для института."""

    response = requests.post(f'{URL}/timetable/', json={'institute': institute_name, 'timetable': image_id})

    if response.status_code == 201:
        profcome_schedule = response.json()
        return profcome_schedule
    return {}


async def get_student_info(pole_name: str, value: [str, int]) -> list[dict] | int:
    """Получаем информацию о студенте."""

    urls_dict = {
        'Проф карта': 'by_profcard',
        'Фамилия студента': 'by_surname',
        'Студенческий билет': 'by_student_book',
        'ФИО студента': 'by_fio',
        'Телеграм ID': 'by_telegram_id',
        'bd_id': 'by_student_id',
    }

    pole = urls_dict[pole_name]
    response = requests.get(f'{URL}/student/{pole}/{value}')

    if response.status_code == 200:
        stud_info = response.json()
        return stud_info['data']

    return response.status_code


async def redact_student_info(bd_id: str, pole_name: str, new_value: str) -> list[dict]:
    """Отправляем id в базе данных пользователя, название поля для редактирования и его новое значение."""

    urls_dict = {
        'Фамилия студента': 'surname',
        'Имя студента': 'name',
        'Отчество студента': 'second_name',
        'Проф карта': 'profcard',
        'Причина мат помощи': 'MP_case',
        'Студенческий билет': 'student_book',
        'Телеграм ID': 'telegram_id',
        'Роль пользователя': 'role',
        'Комментарий': 'comment'
    }

    pole = urls_dict[pole_name]
    data = {pole: new_value}
    response = requests.put(f'{URL}/student/{bd_id}', json=data).json()

    if response.get('data'):
        stud_info = response['data']
        return stud_info
    return []


async def add_many_student_data(data: list[dict]) -> dict | None:
    data_100_items_package = []
    students_added = 0
    for num, item in enumerate(data):
        data_100_items_package.append(item)
        if num % 100 == 0:
            res = requests.post(
                f'{URL}/student/add_many',
                json={'data': data_100_items_package}
            ).json()
            if not res:
                return None
            students_added += res["students_added_counter"]
            data_100_items_package = []
    res = requests.post(
        f'{URL}/student/add_many',
        json={'data': data_100_items_package}
    ).json()
    if not res:
        return None
    students_added += res["students_added_counter"]
    # logging.info(res.json())
    if not students_added:
        return None
    return {"students_added_counter": students_added}


async def get_database():
    response = requests.get(f'{URL}/student/get_data')
    if response.status_code == 200:
        return response
    return {}
