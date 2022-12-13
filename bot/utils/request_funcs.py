import requests

from config import URL


def get_request_key() -> str:
    """Получаем ключ для последующих запросов."""
    # key = requests.get()
    # return key
    pass


def get_student_role(telegram_id: int) -> str:
    """Получаем роль студента с сервера."""
    response = requests.get(f'{URL}/get_role/{telegram_id}')
    if response.status_code == 200:
        student_role = response.json()
        return student_role['role']
    return 'No_role'


async def get_student_info(pole_name: str, value: str) -> list[dict]:
    """Получаем информацию о студенте."""
    urls_dict = {'Проф карта': 'by_profcard', 'Фамилия студента': 'by_surname', 'Студенческий билет': 'by_student_book'}
    pole = urls_dict[pole_name]
    response = requests.get(f'{URL}/{pole}/{value}').json()
    if response.get('data'):
        stud_info = response['data']
        return stud_info
    else:
        return []


async def redact_student_info(id: str, pole_name: str, new_value: str) -> list[dict]:
    """Отправляем на сервер номер профкарты, название поля для редактирования и его новое значение."""
    urls_dict = {'Проф карта': 'profcard', 'Причина мат помощи': 'MP_case', 'Студенческий билет': 'student_book'}
    pole = urls_dict[pole_name]
    data = {pole: new_value}
    response = requests.put(f'{URL}/{id}', json=data).json()
    if response.get('data'):
        stud_info = response['data']
        return stud_info
    else:
        return []


# async def add_student():
#     data = {
#         "institute": "string1",
#         "course": 0,
#         "group": "string",
#         "surname": "string1",
#         "name": "string1",
#         "sex": "муж.",
#         "financing_form": "бюджет",
#         "profcard": "str1ing",
#         "student_book": "stri1ng",
#         "role": "User",
#         "MP_case": "string"
#     }
#     requests.post(URL, json=data)


async def add_many_student_data(data: list[dict]) -> dict:
    return requests.post(f'{URL}/add_many', json={'data': data}).json()
