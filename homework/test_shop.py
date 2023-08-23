"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart, User
from pytest_check import check


@pytest.fixture
def all_products():
    all_products = {
        'book': Product("book", 10, "This is a book", 1000),
        'car': Product("car", 1200, "Super and fast car", 12),
        'pen': Product("pen", 5, "This is a pen", 12939),
    }
    return all_products


@pytest.fixture()
def quantity_for_tests():
    quantity_for_tests = {
        # product_name : [available quantity, more than available quantity]
        'book': [100, 99999990],
        'car': [10, 100],
        'pen': [1293, 12940],
    }
    return quantity_for_tests


@pytest.fixture()
def user():
    test_user = User(
        login='Vov4ik',
        user_money=100000)
    return test_user


cart = Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, all_products, quantity_for_tests):
        # напишите проверки на метод check_quantity
        all_products_list = all_products.keys()
        with check:
            for product in all_products_list:
                expected_quantity = quantity_for_tests[product][0]
                assert all_products[product].check_quantity(expected_quantity), \
                    (f'Less product {all_products[product].name} in stock than expected: '
                     f'expected {expected_quantity}, got {all_products[product].quantity}')

    def test_product_buy(self, all_products, quantity_for_tests):
        # напишите проверки на метод buy
        all_products_list = all_products.keys()
        with check:
            for product in all_products_list:
                available_quantity = quantity_for_tests[product][0]
                assert all_products[product].buy(available_quantity) is not ValueError, \
                    (f'More product {all_products[product].name} in stock than expected: '
                     f'expected {available_quantity}, got {all_products[product].quantity}')

    def test_product_buy_more_than_available(self, all_products, quantity_for_tests):
        #  напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        all_products_list = all_products.keys()
        with check:
            for product in all_products_list:
                more_than_available_quantity = quantity_for_tests[product][1]
                assert all_products[product].buy(more_than_available_quantity) is ValueError, \
                    (f'More product {all_products[product].name} in stock than expected: '
                     f'expected {more_than_available_quantity}, got {all_products[product].quantity}')


class TestCart:
    """
     Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_user_can_add_product_to_cart(self, all_products):
        cart.clear()
        book = all_products['book']
        car = all_products['car']
        pen = all_products['pen']

        cart.add_product(book, buy_count=12)
        cart.add_product(car, buy_count=10)
        cart.add_product(pen, buy_count=12)
        with check:
            assert pen in cart.products, f'Add to cart error: there is no {pen} in the cart {cart.products.keys()}'
            assert book in cart.products, f'Add to cart error: there is no {book} in the cart {cart.products.keys()}'
            assert car in cart.products, f'Add to cart error: there is no {car} in the cart {cart.products.keys()}'

    def test_user_can_remove_position_from_cart_apiece(self, all_products):
        cart.clear()
        book = all_products['book']
        buy_count = 120
        remove_count = 11

        cart.add_product(book, buy_count=buy_count)
        cart.remove_product(book, remove_count=remove_count)

        assert cart.products[book] == buy_count - remove_count, (f'Removing from cart error: '
                                                                 f'expected {buy_count - remove_count} product count, '
                                                                 f'got {cart.products[book]}')


    def test_user_can_remove_whole_position(self, all_products):
        cart.clear()
        book = all_products['book']
        buy_count = 120
        remove_count = 120

        cart.add_product(book, buy_count=buy_count)
        cart.remove_product(book, remove_count=remove_count)

        assert book not in cart.products.keys(), \
            f'Expected, that there is no {book.name} in the cart, but it is'

    def test_user_can_buy_all_cart(self, all_products, user):
        cart.clear()
        book = all_products['book']
        car = all_products['car']
        pen = all_products['pen']
        user_money_before_buying = user.user_money
        cart.add_product(book, 123)
        cart.add_product(car, 3)
        cart.add_product(pen, 3)

        cart.buy(user)
        assert len(cart.products) == 0, f'Something went wrong, some product still in cart'
        assert user_money_before_buying > user.user_money, f"Money wasn't debited from the user account"

    @pytest.mark.xfail(strict=True)
    def test_user_cant_buy_without_enough_money(self, all_products, user):
        cart.clear()
        car = all_products['car']
        user.user_money = 1
        cart.add_product(car, 12)

        cart.buy(user)
