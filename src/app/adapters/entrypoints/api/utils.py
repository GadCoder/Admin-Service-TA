import requests

def check_if_user_is_admin(auth_token: str) -> bool | None:
    url = f"https://users-ms-ta.gadsw.dev/user/user-is-admin/?auth_token={auth_token}"
    response = requests.post(url)
    if response.status_code != 200:
        return None
    user_is_admin = response.json()
    return user_is_admin


def get_teacher_by_code(teacher_code: str) -> dict[str, str] | None:
    url = f"https://localhost:8000/get-by-code/?teacher_code={teacher_code}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    teacher = response.json()
    return teacher