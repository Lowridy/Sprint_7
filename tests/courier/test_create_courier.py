import pytest
import allure
from tests.utils.client import fake

@allure.feature("Создание курьера")
class TestCreateCourier:
    @allure.title("Успешное создание нового курьера")
    def test_create_courier_success(self, client):
        with allure.step("Генерируем валидные данные курьера"):
            login = fake.user_name()
            password = fake.password(length=12, special_chars=False)
            first_name = fake.first_name()

        with allure.step("Отправляем POST /courier"):
            resp = client.register_courier(login, password, first_name)

        with allure.step("Проверяем код 201 и тело ответа {'ok': True}"):
            assert resp.status_code == 201
            assert resp.json() == {"ok": True}

    @allure.title("Создание курьера с существующим логином")
    def test_create_duplicate_courier(self, client, new_courier):
        with allure.step("Используем существующие логин, пароль и имя"):
            login = new_courier["login"]
            password = new_courier["password"]
            first_name = new_courier["firstName"]

        with allure.step("Повторно отправляем POST /courier"):
            resp = client.register_courier(login, password, first_name)

        with allure.step("Проверяем, что код ответа не 201"):
            assert resp.status_code != 201

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    @allure.title("Создание курьера без обязательного поля: {missing_field}")
    def test_create_courier_missing_field(self, client, missing_field):
        with allure.step(f"Формируем запрос без поля {missing_field}"):
            data = {"login": "a", "password": "b", "firstName": "c"}
            data.pop(missing_field)

        with allure.step("Отправляем POST /courier с неполными данными"):
            resp = client.session.post(f"{client.BASE_URL}/courier", json=data)

        with allure.step("Проверяем, что код ответа не 201"):
            assert resp.status_code != 201