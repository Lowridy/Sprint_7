import pytest
import allure

@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Создание и удаление курьера через API")
    def test_create_and_delete_courier(self, client):
        data = client.generate_courier_data()

        with allure.step("Отправляем POST /courier"):
            resp_create = client.register_courier(
                data["login"], data["password"], data["firstName"]
            )
        with allure.step("Проверяем, что ответ 201 и ok=True"):
            assert resp_create.status_code == 201
            assert resp_create.json().get("ok") is True

        with allure.step("Отправляем POST /courier/login"):
            resp_login = client.login_courier(data["login"], data["password"])
        with allure.step("Проверяем, что ответ 200 и извлекаем id"):
            assert resp_login.status_code == 200
            courier_id = resp_login.json().get("id")
            assert isinstance(courier_id, int)

        with allure.step("Отправляем DELETE /courier/{id}"):
            resp_delete = client.delete_courier(courier_id)
        with allure.step("Проверяем, что ответ 200 и ok=True"):
            assert resp_delete.status_code == 200
            assert resp_delete.json().get("ok") is True

    @pytest.mark.parametrize("missing, payload", [
        ("login", {"password": "pwd", "firstName": "Имя"}),
        ("password", {"login": "login", "firstName": "Имя"}),
        ("firstName", {"login": "login", "password": "pwd"}),
    ])
    @allure.title("Создание курьера без поля {missing}")
    def test_create_courier_missing_required(self, client, missing, payload):
        with allure.step(f"Отправляем POST /courier без поля {missing}"):
            resp = client.session.post(f"{client.BASE_URL}/courier", json=payload)
        with allure.step("Проверяем, что ответ 400 и есть ошибка"):
            assert resp.status_code == 400
            assert "error" in resp.json()
