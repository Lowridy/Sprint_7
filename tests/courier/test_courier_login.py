import pytest
import allure

@allure.feature("Логин курьера")
class TestCourierLogin:

    @allure.title("Успешный логин курьера")
    def test_login_success(self, client, new_courier):
        login = new_courier["login"]
        password = new_courier["password"]

        with allure.step("Отправляем POST /courier/login с валидными данными"):
            resp = client.login_courier(login, password)
        with allure.step("Проверяем, что ответ 200 и есть поле id"):
            assert resp.status_code == 200
            body = resp.json()
            assert "id" in body and isinstance(body["id"], int)

    @pytest.mark.parametrize("field, exp_status, exp_msg", [
        ("login", 400, "Недостаточно данных для входа"),
        ("password", 400, "Недостаточно данных для входа"),
    ])
    @allure.title("Логин без обязательного поля {field}")
    def test_login_missing_field(self, client, new_courier, field, exp_status, exp_msg):
        payload = {"login": new_courier["login"], "password": new_courier["password"]}
        payload.pop(field)
        with allure.step(f"Отправляем POST /courier/login без поля {field}"):
            resp = client.session.post(f"{client.BASE_URL}/courier/login", json=payload)
        with allure.step("Проверяем статус-код и текст ошибки"):
            assert resp.status_code == exp_status
            assert exp_msg in resp.json().get("message", "")

    @allure.title("Логин с неверными данными возвращает 404")
    def test_login_wrong_credentials(self, client):
        with allure.step("Отправляем POST /courier/login с неверным логином/паролем"):
            resp = client.login_courier("wrong_login", "wrong_pass")
        with allure.step("Проверяем, что код 404 и сообщение 'Учетная запись не найдена'"):
            assert resp.status_code == 404
            assert resp.json().get("message") == "Учетная запись не найдена"
