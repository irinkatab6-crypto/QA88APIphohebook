import token
import pytest
from conftest import *
from faker import Faker
fake = Faker()

class TestRegistration:

    @pytest.mark.smoke
    @pytest.mark.auth
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

    @pytest.mark.auth
    @pytest.mark.negative
    def test_registration_negative_duplicate_user(self, session, registration_url, random_user):
        body = {
            "username": random_user.username,
            "password": random_user.password,
        }
        headers = {
            "Content-Type": "application/json",
        }

        response = session.post(registration_url, json=body, headers=headers)
        data = response.json()
        print(response.json())
        assert response.status_code in [400, 409]
        assert "User already exists" in response.json().values()

    @pytest.mark.auth
    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_email", [
        "vbgyt123.tgy.gbj",
        "bnhjyi67@",
        "@gmail.com",
        "dfgrt679@gmail",
        "fgvty56@@ghyu.vbh",
        "fgth67 @cvg.bn",
    ])

    def test_registration_negative_invalid_email(self, session, registration_url, invalid_email):
        user = User(invalid_email, "Qwerty123$")
        body = {
        "username": user.username,
        "password": user.password,
        }
        headers = {
        "Content-Type": "application/json",
        }

        response = session.post(registration_url, json=body, headers=headers)
        data = response.json()
        print(response.json())
        assert response.status_code == 400
        assert data ["message"] ["username"] == "must be a well-formed email address"

    @pytest.mark.auth
    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_password", [
        "qwerty123$",
        "QWERTY123$!",
        "Qwerty!$",
        "Qwerty123",
        "Qwer ty1",
        "Qwerty!123",
    ])
    def test_registration_negative_invalid_password(self, session, registration_url, invalid_password):
        user = User(fake.email(), invalid_password)
        body = {
            "username": user.username,
            "password": user.password,
        }
        headers = {
            "Content-Type": "application/json",
        }
        response = session.post(registration_url, json=body, headers=headers)
        data = response.json()
        print(response.json())
        assert response.status_code == 400
        assert "Must contain at" in data["message"]["password"]
        #