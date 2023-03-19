import logging


async def csv_parser(data: str) -> list[dict]:
    data_list = []
    data_split = data.lstrip(';\n\r').replace('\r', '').split('\n')[1:-1]
    for string in data_split:
        student_data = [val if val else None for val in string.split(';')]
        logging.warning(student_data)
        surname, name, *second_name = student_data[3].split()
        parsed_student_data = {
            "institute": student_data[0],
            "course": student_data[1],
            "group": student_data[2],
            "surname": surname,
            "name": name,
            "second_name": " ".join(second_name),
            "birthdate": student_data[4],
            "sex": student_data[5],
            "financing_form": student_data[6],
            "profcard": student_data[7],
            "student_book": student_data[8],
            "role": student_data[9],
            "MP_case": student_data[10],
            "comment": student_data[11],
            "telegram_id": student_data[12],
        }
        if not all([
            parsed_student_data["institute"],
            parsed_student_data["course"],
            parsed_student_data["group"],
            parsed_student_data["surname"],
            parsed_student_data["name"],
            parsed_student_data["sex"],
            parsed_student_data["financing_form"],
            parsed_student_data["role"],
        ]):
            continue
        parsed_student_data = {
            key: val.strip() if type(val) == str else val
            for key, val in parsed_student_data.items()
        }
        data_list.append(parsed_student_data)
    return data_list
