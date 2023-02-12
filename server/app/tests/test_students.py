import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_empty_list(async_client: AsyncClient):
    response = await async_client.get(url="student/")
    assert response.status_code == 200
    assert response.json() == {
        "data": []
    }


@pytest.mark.asyncio
async def test_create_students(async_client: AsyncClient):
    student_1 = {
        "institute": "PGS",
        "course": 1,
        "group": "PGS-1",
        "surname": "Иванов",
        "name": "Иван Иванович",
        "sex": "муж.",
        "financing_form": "бюджет",
        "profcard": "11-1111",
        "student_book": "11-A-11111",
        "role": "User",
    }
    student_2 = {
        "institute": "IGES",
        "course": 2,
        "group": "IGES-2",
        "surname": "Петров",
        "name": "Иван Петрович",
        "sex": "муж.",
        "financing_form": "бюджет",
        "profcard": "22-2222",
        "student_book": "22-B-22222",
        "role": "User",
    }
    student_3 = {
        "institute": "PGS",
        "course": 3,
        "group": "PGS-3",
        "surname": "Петров",
        "name": "Иван Петрович",
        "sex": "муж.",
        "financing_form": "бюджет",
        "profcard": "33-3333",
        "student_book": "33-C-33333",
        "role": "Admin",
        "telegram_id": "999",
    }
    response = await async_client.post(
        url="student/add_many",
        json={"data": [student_1, student_2, student_3]}
    )
    assert response.status_code == 201
    assert response.json() == {"students_added_counter": 3}


@pytest.mark.asyncio
async def test_get_3_students_list(async_client: AsyncClient):
    response = await async_client.get(url="student/")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "id": response.json()["data"][0]["id"],
                "institute": "PGS",
                "course": 1,
                "group": "PGS-1",
                "surname": "Иванов",
                "name": "Иван Иванович",
                "sex": "муж.",
                "financing_form": "бюджет",
                "profcard": "11-1111",
                "student_book": "11-A-11111",
                "role": "User",
                "MP_case": None,
                "telegram_id": None,
            },
            {
                "id": response.json()["data"][1]["id"],
                "institute": "IGES",
                "course": 2,
                "group": "IGES-2",
                "surname": "Петров",
                "name": "Иван Петрович",
                "sex": "муж.",
                "financing_form": "бюджет",
                "profcard": "22-2222",
                "student_book": "22-B-22222",
                "role": "User",
                "MP_case": None,
                "telegram_id": None,
            },
            {
                "id": response.json()["data"][2]["id"],
                "institute": "PGS",
                "course": 3,
                "group": "PGS-3",
                "surname": "Петров",
                "name": "Иван Петрович",
                "sex": "муж.",
                "financing_form": "бюджет",
                "profcard": "33-3333",
                "student_book": "33-C-33333",
                "role": "Admin",
                "MP_case": None,
                "telegram_id": "999",
            },
        ]
    }


@pytest.mark.asyncio
async def test_get_by_surname(async_client: AsyncClient):
    required_surname = "Иванов"
    response = await async_client.get(url=f"student/by_surname/{required_surname}")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "id": response.json()["data"][0]["id"],
                "institute": "PGS",
                "course": 1,
                "group": "PGS-1",
                "surname": "Иванов",
                "name": "Иван Иванович",
                "sex": "муж.",
                "financing_form": "бюджет",
                "profcard": "11-1111",
                "student_book": "11-A-11111",
                "role": "User",
                "MP_case": None,
                "telegram_id": None,
            },
        ]
    }


@pytest.mark.asyncio
async def test_get_by_surname(async_client: AsyncClient):
    required_fio = "Петров Иван Петрович"
    response = await async_client.get(url=f"student/by_fio/{required_fio}")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "id": response.json()["data"][0]["id"],
                "institute": "IGES",
                "course": 2,
                "group": "IGES-2",
                "surname": "Петров",
                "name": "Иван Петрович",
                "sex": "муж.",
                "financing_form": "бюджет",
                "profcard": "22-2222",
                "student_book": "22-B-22222",
                "role": "User",
                "MP_case": None,
                "telegram_id": None,
            },
            {
                "id": response.json()["data"][1]["id"],
                "institute": "PGS",
                "course": 3,
                "group": "PGS-3",
                "surname": "Петров",
                "name": "Иван Петрович",
                "sex": "муж.",
                "financing_form": "бюджет",
                "profcard": "33-3333",
                "student_book": "33-C-33333",
                "role": "Admin",
                "MP_case": None,
                "telegram_id": "999",
            },
        ]
    }


@pytest.mark.asyncio
async def test_get_by_profcard(async_client: AsyncClient):
    required_profcard = "11-1111"
    response = await async_client.get(url=f"student/by_profcard/{required_profcard}")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "id": response.json()["data"][0]["id"],
                "institute": "PGS",
                "course": 1,
                "group": "PGS-1",
                "surname": "Иванов",
                "name": "Иван Иванович",
                "sex": "муж.",
                "financing_form": "бюджет",
                "profcard": "11-1111",
                "student_book": "11-A-11111",
                "role": "User",
                "MP_case": None,
                "telegram_id": None,
            },
        ]
    }
    response = await async_client.get(url=f"student/by_profcard/11-111")
    assert response.status_code == 404
    response = await async_client.get(url=f"student/by_profcard/11-11")
    assert response.status_code == 422
    response = await async_client.get(url=f"student/by_profcard/11-11111")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_by_studentbook(async_client: AsyncClient):
    required_studentbook = "22-B-22222"
    response = await async_client.get(url=f"student/by_student_book/{required_studentbook}")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "id": response.json()["data"][0]["id"],
                "institute": "IGES",
                "course": 2,
                "group": "IGES-2",
                "surname": "Петров",
                "name": "Иван Петрович",
                "sex": "муж.",
                "financing_form": "бюджет",
                "profcard": "22-2222",
                "student_book": "22-B-22222",
                "role": "User",
                "MP_case": None,
                "telegram_id": None,
            },
        ]
    }


@pytest.mark.asyncio
async def test_get_by_telegram_id(async_client: AsyncClient):
    required_telegram_id = "999"
    response = await async_client.get(url=f"student/by_telegram_id/{required_telegram_id}")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "id": response.json()["data"][0]["id"],
                "institute": "PGS",
                "course": 3,
                "group": "PGS-3",
                "surname": "Петров",
                "name": "Иван Петрович",
                "sex": "муж.",
                "financing_form": "бюджет",
                "profcard": "33-3333",
                "student_book": "33-C-33333",
                "role": "Admin",
                "MP_case": None,
                "telegram_id": "999",
            },
        ]
    }


@pytest.mark.asyncio
async def test_try_to_update_incorrect_student(async_client: AsyncClient):
    incorrect_student_id = "123"
    student_update = {"course": 3}
    response = await async_client.put(
        url=f"student/{incorrect_student_id}",
        json=student_update,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_student(async_client: AsyncClient):
    required_profcard = "11-1111"
    student = await async_client.get(url=f"student/by_profcard/{required_profcard}")
    student_id = student.json()["data"][0]["id"]
    student_update = {"course": 3, "group": "PGS-3"}
    response = await async_client.put(
        url=f"student/{student_id}",
        json=student_update,
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "id": response.json()["data"][0]["id"],
                "institute": "PGS",
                "course": 3,
                "group": "PGS-3",
                "surname": "Иванов",
                "name": "Иван Иванович",
                "sex": "муж.",
                "financing_form": "бюджет",
                "profcard": "11-1111",
                "student_book": "11-A-11111",
                "role": "User",
                "MP_case": None,
                "telegram_id": None,
            },
        ]
    }


@pytest.mark.asyncio
async def test_check_update_student(async_client: AsyncClient):
    required_profcard = "11-1111"
    response = await async_client.get(url=f"student/by_profcard/{required_profcard}")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "id": response.json()["data"][0]["id"],
                "institute": "PGS",
                "course": 3,
                "group": "PGS-3",
                "surname": "Иванов",
                "name": "Иван Иванович",
                "sex": "муж.",
                "financing_form": "бюджет",
                "profcard": "11-1111",
                "student_book": "11-A-11111",
                "role": "User",
                "MP_case": None,
                "telegram_id": None,
            },
        ]
    }


@pytest.mark.asyncio
async def test_try_to_delete_incorrect_student(async_client: AsyncClient):
    incorrect_student_id = "123"
    response = await async_client.delete(url=f"student/{incorrect_student_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_student(async_client: AsyncClient):
    required_profcard = "11-1111"
    student = await async_client.get(url=f"student/by_profcard/{required_profcard}")
    student_id = student.json()["data"][0]["id"]
    response = await async_client.delete(url=f"student/{student_id}")
    assert response.status_code == 200
    assert response.json() == {"data": "Deleted successful"}


@pytest.mark.asyncio
async def test_try_to_get_deleted_student(async_client: AsyncClient):
    required_profcard = "11-1111"
    response = await async_client.get(url=f"student/by_profcard/{required_profcard}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_2_students(async_client: AsyncClient):
    required_profcard = "22-2222"
    student = await async_client.get(url=f"student/by_profcard/{required_profcard}")
    student_id = student.json()["data"][0]["id"]
    response = await async_client.delete(url=f"student/{student_id}")
    assert response.status_code == 200
    required_profcard = "33-3333"
    student = await async_client.get(url=f"student/by_profcard/{required_profcard}")
    student_id = student.json()["data"][0]["id"]
    response = await async_client.delete(url=f"student/{student_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_empty_list_after_deleting(async_client: AsyncClient):
    response = await async_client.get(url="student/")
    assert response.status_code == 200
    assert response.json() == {
        "data": []
    }


"""
for future:
try to create student twice
"""
