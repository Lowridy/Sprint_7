import pytest
import allure
from faker import Faker

fake = Faker("ru_RU")

@allure.feature("Order Creation")
class TestCreateOrder:

    @pytest.mark.parametrize("colors", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    @allure.title("Создание заказа с цветами {colors}")
    def test_create_order_various_colors(self, client, colors):
        with allure.step("Генерируем данные заказа через Faker"):
            order_data = {
                "firstName": fake.first_name(),
                "lastName": fake.last_name(),
                "address": fake.street_address(),
                "metroStation": 4,
                "phone": "+70000000000",
                "rentTime": 5,
                "deliveryDate": "2025-06-22",
                "comment": "Тестовый заказ",
                "color": colors
            }

        with allure.step("Отправляем POST /orders"):
            resp = client.create_order(**order_data)

        with allure.step("Проверяем, что ответ 201 и есть поле track"):
            assert resp.status_code == 201
            body = resp.json()
            assert "track" in body and isinstance(body["track"], int)
