import requests
import uuid
from cryptography.fernet import Fernet

from config import URL
from common_key import COMMON_KEY

async def get_request_key(pole="token") -> str:
    """Получаем ключ для последующих запросов."""
    answer = requests.get(f"{URL}/student/{pole}") # Synchronize URL
    json = answer.json()
    secret_uuid = json["data"]
    common_key = Fernet(COMMON_KEY) # Here is COMMON_KEY
    token = common_key.decrypt(secret_uuid) 
    return uuid.UUID(token.hex())


async def get_profcome_schedule(course_name: str) -> dict:
    """Получаем расписание приёма доков для института."""
    token = await get_request_key()
    params = {"token": token}

    response = requests.get(f'{URL}/timetable/{course_name}', params=params)

    if response.status_code == 200:
        profcome_schedule = response.json()
        return profcome_schedule
    return {}


async def get_student_info(pole_name: str, value: [str, int]) -> list[dict]:
    """Получаем информацию о студенте."""

    urls_dict = {
        'Проф карта': 'by_profcard',
        'Фамилия студента': 'by_surname',
        'Студенческий билет': 'by_student_book',
        'ФИО студента': 'by_fio',
        'telegram_id': 'by_telegram_id'
    }

    token = await get_request_key()
    params = {"token": token}
    pole = urls_dict[pole_name]
    response = requests.get(f'{URL}/student/{pole}/{value}', params=params).json()

    if response.get('data'):
        stud_info = response['data']
        return stud_info
    return []


async def redact_student_info(bd_id: str, pole_name: str, new_value: str) -> list[dict]:
    """Отправляем id в базе данных пользователя, название поля для редактирования и его новое значение."""

    urls_dict = {
        'Проф карта': 'profcard',
        'Причина мат помощи': 'MP_case',
        'Студенческий билет': 'student_book',
        'telegram_id': 'telegram_id',
        'Роль пользователя': 'role'
    }

    token = await get_request_key()
    params = {"token": token}
    pole = urls_dict[pole_name]
    data = {pole: new_value}
    response = requests.put(f'{URL}/student/{bd_id}', json=data, params=params).json()

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
            token = await get_request_key()
            params = {"token": token}
            res = requests.post(
                f'{URL}/student/add_many',
                json={'data': data_100_items_package},
                params=params
            ).json()
            if not res:
                return None
            students_added += res["students_added_counter"]
            data_100_items_package = []
    token = await get_request_key()
    params = {"token": token}
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
