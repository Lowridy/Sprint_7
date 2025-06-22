import allure

@allure.feature("Список заказов")
class TestGetOrdersList:
    @allure.title("Получение списка заказов")
    def test_get_orders_list(self, client):
        with allure.step("Отправляем GET /orders для получения списка заказов"):
            resp = client.get_orders()

        with allure.step("Проверяем код 200 и что сервер вернул массив orders"):
            assert resp.status_code == 200
            assert isinstance(resp.json().get("orders"), list)