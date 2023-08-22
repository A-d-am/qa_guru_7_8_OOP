"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart
from pytest_check import check


@pytest.fixture
def all_products():
    all_products = {
        'book': Product("book", 100, "This is a book", 1000),
        'car': Product("car", 120, "Super and fast car", 12),
        'pen': Product("pen", 5, "This is a pen", 12939),
    }
    return all_products


@pytest.fixture()
def test_quantity():
    test_quantity = {
        # product_name : [available quantity, more than available quantity]
        'book': [100, 99999990],
        'car': [10, 100],
        'pen': [1293, 12940],
    }
    return test_quantity


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, all_products, test_quantity):
        # напишите проверки на метод check_quantity
        all_products_list = all_products.keys()
        with check:
            for product in all_products_list:
                expected_quantity = test_quantity[product][0]
                assert all_products[product].check_quantity(expected_quantity), \
                    (f'Less product {all_products[product].name} in stock than expected: '
                     f'expected {expected_quantity}, got {all_products[product].quantity}')

    def test_product_buy(self, all_products, test_quantity):
        # напишите проверки на метод buy
        all_products_list = all_products.keys()
        with check:
            for product in all_products_list:
                available_quantity = test_quantity[product][0]
                assert all_products[product].buy(available_quantity) == ValueError, \
                    (f'More product {all_products[product].name} in stock than expected: '
                     f'expected {available_quantity}, got {all_products[product].quantity}')


def test_product_buy_more_than_available(self, all_products, test_quantity):
    #  напишите проверки на метод buy,
    #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
    all_products_list = all_products.keys()
    with check:
        for product in all_products_list:
            more_than_available_quantity = test_quantity[product][1]
            assert all_products[product].buy(more_than_available_quantity) == ValueError, \
                (f'More product {all_products[product].name} in stock than expected: '
                 f'expected {more_than_available_quantity}, got {all_products[product].quantity}')


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
