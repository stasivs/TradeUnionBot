import csv
import os
from datetime import datetime
from pathlib import Path


async def get_list_from_dict(input_data: list[dict]) -> list[list]:
    output_data = []
    for item in input_data:
        output_data.append(
            [
                item["institute"],
                item["course"],
                item["group"],
                " ".join((item["surname"], item["name"], item["second_name"])),
                item["birthdate"],
                item["sex"],
                item["financing_form"],
                item["profcard"],
                item["student_book"],
                item["role"],
                item["MP_case"],
                item["comment"],
                item["telegram_id"],
            ]
        )
    return output_data


async def write_csv(data: list[list]) -> tuple:
    file_name = f"{datetime.now().strftime('%d-%m-%Y-%H-%M')}.csv"
    dir_name = "data_files"
    os.makedirs(dir_name, exist_ok=True)
    path = Path(dir_name, file_name)
    with open(path, "w+") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Институт",
                "Курс",
                "Группа",
                "ФИО",
                "Дата рождения",
                "Пол",
                "Форма финансирования",
                "Профкарта",
                "Зачетная книжка",
                "Роль",
                "Причина получения МП",
                "Комментарий",
                "Телеграм ID",
            ]
        )
        writer.writerows(data)
    return path, file_name
