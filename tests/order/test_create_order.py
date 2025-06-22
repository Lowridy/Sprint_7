import pytest
import allure
from tests.utils.client import fake

@allure.feature("Создание заказа")
class TestCreateOrder:
    @pytest.mark.parametrize("color_param", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    @allure.title("Создание заказа с цветом {color_param}")
    def test_create_order_various_colors(self, client, color_param):
        with allure.step("Генерируем данные заказа"):
            order_data = {
                "firstName": fake.first_name(),
                "lastName": fake.last_name(),
                "address": fake.street_address(),
                "metroStation": 4,
                "phone": "+70000000000",
                "rentTime": 5,
                "deliveryDate": "2025-06-22",
                "comment": "Тестовый заказ",
                "color": color_param
            }

        with allure.step("Отправляем POST /orders"):
            resp = client.create_order(**order_data)

        with allure.step("Проверяем код 201 и наличие трека заказа"):
            assert resp.status_code == 201
            body = resp.json()
            assert isinstance(body.get("track"), int)