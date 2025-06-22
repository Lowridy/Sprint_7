import allure

@allure.feature("Order List")
class TestGetOrdersList:

    @allure.title("Получение списка всех заказов")
    def test_get_orders_list(self, client):
        with allure.step("Отправляем GET /orders"):
            resp = client.get_orders()
        with allure.step("Проверяем, что ответ 200 и возвращается массив orders"):
            assert resp.status_code == 200
            assert isinstance(resp.json().get("orders"), list)
