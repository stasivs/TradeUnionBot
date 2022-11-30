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


async def get_student_info(pole_name: str, value: str) -> dict:
    """Получаем информацию о студенте."""
    # stud_info = requests.get().json()
    # return stud_info
    return {'inst': "ICTMS", 'curs': '3', 'group': '201', 'fio': 'Фролов Илья Антонович', 'sex': 'Муж.',
            'financing': 'Бюджет', 'prof_id': '20-1901', 'stud_id': '22-Б-07305', 'reason': 'Общежитие'}


async def redact_student_info(stud_id: str, pole_name: str, new_value: str) -> None:
    """Редактируем информацию о студенте в бд."""
    # requests.post()
    pass
