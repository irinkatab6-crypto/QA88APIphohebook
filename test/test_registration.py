import token

from conftest import *


class TestRegistration:

    def test_registration_positive(self, session, registration_url, random_user):
        print(random_user)
        body = {
            "username": random_user.username,
            "password": random_user.password,
        }
        headers = {
            "Content-Type": "application/json",
        }
        response = session.post(registration_url, json=body, headers=headers)
        assert response.status_code == 200
        assert "token" in response.json().keys()

    def test_registration_negative_duplicate_user(self, session, registration_url, random_user):
        body = {
            "username": random_user.username,
            "password": random_user.password,
        }
        headers = {
            "Content-Type": "application/json",
        }
        session.post(registration_url, json=body, headers=headers)
        response = session.post(registration_url, json=body, headers=headers)
        print(response.json())
        assert response.status_code in [400, 409]
        assert "User already exists" in response.json().values()

    def test_registration_negative_invalid_email(self, session, registration_url, invalid_email):
        user = User(invalid_email, "Qwerty123$")
        body = {
        "username": user.username,
        "password": user.password,
        }
        headers = {
        "Content-Type": "application/json",
        }
        session.post(registration_url, json=body, headers=headers)
        response = session.post(registration_url, json=body, headers=headers)
        print(response.json())
        assert response.status_code in [400, 409]
        assert "User already exists" in response.json().values()