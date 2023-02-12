async def csv_parser(data: str) -> list[dict]:
    data_list = []
    data_split = data.lstrip(';\n\r').replace('\r', '').split('\n')[1:-1]
    for string in data_split:
        student_data = [val if val else None for val in string.split(';')]
        parsed_student_data = {
            "institute": student_data[0].strip(),
            "course": student_data[1].strip(),
            "group": student_data[2].strip(),
            "surname": student_data[3].split()[0].strip(),
            "name": ' '.join(student_data[3].split()[1:]).strip(),
            "sex": student_data[4].strip(),
            "financing_form": student_data[5].strip(),
            "profcard": student_data[6].strip(),
            "student_book": student_data[7].strip(),
            "role": student_data[8].strip(),
            "MP_case": student_data[9].strip(),
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
        data_list.append(parsed_student_data)
    return data_list
