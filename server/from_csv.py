import requests


def get_data_from_file(csv_file):
    data_list = []
    file_data = csv_file.read().split('\n')[2:]
    for string in file_data:
        data = [val if val else None for val in string.split(';')]
        data_list.append({
            "institute": data[0],
            "course": data[1],
            "group": data[2],
            "surname": data[3].split()[0],
            "name": ' '.join(data[3].split()[1:]),
            "sex": data[4],
            "financing_form": data[5],
            "profcard": data[6],
            "student_book": data[7],
            "role": data[8],
            "MP_case": data[9],
        })
    return data_list


if __name__ == '__main__':
    with open(file='Primer.csv') as file:
        print(requests.post('http://0.0.0.0/student/add_many', json={'data': get_data_from_file(file)}).json())
