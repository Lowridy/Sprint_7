import pytest
import allure
from tests.utils.client import ScooterClient, register_new_courier_and_return, fake

@pytest.fixture(scope="session")
def client():
    with allure.step("Инициализируем экземпляр клиента ScooterClient"):
        client_instance = ScooterClient()
    return client_instance

@pytest.fixture
def new_courier():
    with allure.step("Регистрируем нового курьера через API"):
        creds = register_new_courier_and_return()
        assert creds, "Не удалось зарегистрировать курьера"
    yield creds

@pytest.fixture(params=[["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
def color_param(request):
    with allure.step(f"Выбираем цвет заказа: {request.param}"):
        return request.param
