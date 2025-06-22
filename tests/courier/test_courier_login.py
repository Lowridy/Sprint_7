import pytest
import allure
from tests.utils.client import fake

@allure.feature("Логин курьера")
class TestCourierLogin:
    @allure.title("Успешный логин курьера")
    def test_login_success(self, client, new_courier):
        with allure.step("Отправляем POST /courier/login с валидными данными"):
            resp = client.login_courier(new_courier["login"], new_courier["password"])

        with allure.step("Проверяем код 200 и наличие поля id"):
            assert resp.status_code == 200
            assert isinstance(resp.json().get("id"), int)

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Логин курьера без поля {missing_field}")
    def test_login_missing_field(self, client, missing_field):
        with allure.step(f"Формируем запрос без поля {missing_field}"):
            payload = {"login": "x", "password": "y"}
            payload.pop(missing_field)

        with allure.step("Отправляем POST /courier/login с неполными данными"):
            resp = client.session.post(f"{client.BASE_URL}/courier/login", json=payload)

        with allure.step("Проверяем, что код ответа не 200 и возвращается ошибка"):
            assert resp.status_code != 200

    @allure.title("Логин курьера с неверными данными")
    def test_login_wrong_credentials(self, client):
        with allure.step("Отправляем POST /courier/login с неверным логином/паролем"):
            resp = client.login_courier("nonexist", "wrong")

        with allure.step("Проверяем, что код ответа не 200 и возвращается ошибка"):
            assert resp.status_code != 200