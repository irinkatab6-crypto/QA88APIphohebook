from dataclasses import asdict
from faker import Faker
import random
import pytest
fake = Faker()

class TestContacts:
    @pytest.mark.smoke
    def test_add_contact_positive(self, session, add_contact_url, auth_headers, random_contact):
        response = session.post(
            add_contact_url,
            headers=auth_headers,
            json=asdict(random_contact)
        )
        print(response.json()["message"])
        assert response.status_code == 200
        assert "Contact was added" in response.json()["message"]
    @pytest.mark.smoke
    def test_get_all_contacts_positive(self, session, add_contact_url, auth_headers):
        response = session.get(
            add_contact_url,
            headers=auth_headers
        )
        print(response.json())
        assert response.status_code == 200
        assert isinstance(response.json()["contacts"], list)

    @pytest.mark.negative
    def test_get_all_contacts_negative_wrong_token(self, session, add_contact_url, auth_headers):
        headers = {"Authorization": "Lorem ipsum dolor sit amet"}
        response = session.get(
            add_contact_url,
            headers=headers)
        print(response.json())
        assert response.status_code == 401
        assert response.json()["error"] == "Unauthorized"

    @pytest.mark.smoke
    def test_update_contact_positive(self, session, add_contact_url, auth_headers, create_contact):
        contact_id = create_contact

        print(">>> Contact ID:", contact_id)
        res1 = session.get(add_contact_url, headers=auth_headers)


        updated_contact = {
            "id": contact_id,
            "name": fake.name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "phone": "0172365517778",
            "address": "address_Lorem",
            "description": "text",
        }

        response = session.put(add_contact_url, headers=auth_headers, json=updated_contact)
        print(response.json())

        assert response.status_code == 200
        assert "Contact was updated" in response.json()["message"]
        res = session.get(add_contact_url, headers=auth_headers)
        print(">>> Here are ONLY HEADERS AFTER UpDate: ", res.json())
        assert res.json()["contacts"][0]["address"] == "address_Lorem"
        assert res.json()["contacts"][0]["phone"] == "0172365517778"

    def test_update_contact_one_field_positive(self, session, add_contact_url, auth_headers, create_contact):
        contact_id = create_contact
        print("Contact ID:", contact_id)

        res1 = session.get(add_contact_url, headers=auth_headers).json()[
            "contacts"][0]
        print(res1)
        res1["name"] = "Robert"

        response = session.put(add_contact_url, headers=auth_headers, json=res1)
        print(response.json())
        assert response.status_code == 200
        assert "Contact was updated" in response.json()["message"]
        res = session.get(add_contact_url, headers=auth_headers)
        print(res.json())

    def test_update_contact_one_field_second_positive(self, session, add_contact_url, auth_headers,
                                                      create_contact_return_contact):
        contact = create_contact_return_contact
        print(contact)
        contact["address"] = "New address"
        response = session.put(add_contact_url, headers=auth_headers, json=contact)
        assert response.status_code == 200
        assert "Contact was updated" in response.json()["message"]

    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    @pytest.mark.smoke
    def test_delete_contact_positive(self, session, add_contact_url, auth_headers, create_contact):
        contact_id = create_contact
        response = session.delete(f"{add_contact_url}/{contact_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "Contact was deleted!" in response.json()["message"]