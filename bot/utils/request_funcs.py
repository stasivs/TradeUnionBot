import requests, logging

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


async def get_student_info(pole_name: str, value: [str, int]) -> list[dict]:
    """Получаем информацию о студенте."""
    urls_dict = {
        'Проф карта': 'by_profcard',
        'Фамилия студента': 'by_surname',
        'Студенческий билет': 'by_student_book',
        'ФИО студента': 'by_fio',
        'telegram_id': 'by_telegram_id'
    }
    pole = urls_dict[pole_name]
    response = requests.get(f'{URL}/student/{pole}/{value}').json()
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
        'telegram_id': 'telegram_id'
    }
    pole = urls_dict[pole_name]
    data = {pole: new_value}
    response = requests.put(f'{URL}/student/{bd_id}', json=data).json()
    if response.get('data'):
        stud_info = response['data']
        return stud_info
    return []


async def add_many_student_data(data: list[dict]) -> dict:
    res = requests.post(f'{URL}/student/add_many', json={'data': data})
    logging.info(res.json())
    return res
