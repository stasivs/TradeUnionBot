from config import URL

import requests


def get_request_key() -> str:
    """Получаем ключ для последующих запросов."""
    # key = requests.get()
    # return key
    pass


def get_admin_list() -> list:
    """Получаем список id админов с сервера."""
    # admin_list = requests.get()
    # return admin_list
    return [1003082911]


async def get_student_info(pole_name: str, value: str, message) -> list[dict]:
    """Получаем информацию о студенте."""
    urls_dict = {'Проф карта': 'by_profcard', 'Фамилия студента': 'by_surname', 'Студенческий билет': 'by_student_book'}
    pole = urls_dict[pole_name]
    response = requests.get(f'{URL}/{pole}/{value}').json()
    print(response)
    if response['code'] == 200:
        stud_info = response['data']
        return stud_info
    else:
        return []


async def redact_student_info(id: str, pole_name: str, new_value: str) -> None:
    """Отправляем на сервер номер профкарты, название поля для редактирования и его новое значение."""
    urls_dict = {'Проф карта': 'profcard', 'Причина мат помощи': 'MP_case', 'Студенческий билет': 'student_book'}
    pole = urls_dict[pole_name]
    data = {pole: new_value}
    info = requests.put(f'{URL}/{id}', json=data)


async def add_student():
    data = {
        "institute": "string1",
        "course": 0,
        "group": "string",
        "surname": "string1",
        "name": "string1",
        "sex": "муж.",
        "financing_form": "бюджет",
        "profcard": "str1ing",
        "student_book": "stri1ng",
        "role": "User",
        "MP_case": "string"
    }
    requests.post(URL, json=data)
