async def csv_parser(data: str) -> list[dict]:
    data_list = []
    data_split = data.lstrip(';\n\r').replace('\r', '').split('\n')[1:-1]
    for string in data_split:
        student_data = [val if val else None for val in string.split(';')]
        data_list.append({
            "institute": student_data[0],
            "course": student_data[1],
            "group": student_data[2],
            "surname": student_data[3].split()[0],
            "name": ' '.join(student_data[3].split()[1:]),
            "sex": student_data[4],
            "financing_form": student_data[5],
            "profcard": student_data[6],
            "student_book": student_data[7],
            "role": student_data[8],
            "MP_case": student_data[9],
        })
    return data_list
