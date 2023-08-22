import pytest


class User:
    """
    Класс пользователя
    """
    login:str
    user_money: float

    def __init__(self,login, user_money):
        self.login = login
        self.user_money = user_money

    def decrease_user_money(self, value: float):
        self.user_money -= value


class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        if self.quantity >= quantity:
            return True
        else:
            return False

    def buy(self, quantity):
        """
        реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if not self.check_quantity(quantity):
            return ValueError
        self.quantity -= quantity

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
               Метод добавления продукта в корзину.
               Если продукт уже есть в корзине, то увеличиваем количество
               """
        if product in self.products:
            old_buy_count = self.products.pop(product)
            new_buy_count = old_buy_count + buy_count

            assert product.check_quantity(new_buy_count), (f"You can't add to cart more product than store have: "
                                                           f"you want add {new_buy_count} of {product.name},"
                                                           f" but there are only {product.quantity}")
            self.products[product] = new_buy_count
        else:
            assert product.check_quantity(buy_count), (f"You can't add to cart more product than store have: "
                                                       f"you want add {buy_count} of {product.name},"
                                                       f" but there are only {product.quantity}")
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):

        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        current_product_buy_count = self.products[product]
        if remove_count is None:
            del self.products[product]
        elif current_product_buy_count <= remove_count:
            del self.products[product]
        else:
            old_buy_count = self.products.pop(product)
            new_buy_count = old_buy_count - remove_count
            self.products[product] = new_buy_count

    def clear(self):
        self.products.clear()

    def get_total_price(self) -> float:
        total_price = 0
        all_products_list = self.products.keys()
        for product in all_products_list:
            total_price += product.price * self.products[product]
        return total_price

    def buy(self, user: User):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for product in self.products:
            if product.check_quantity(product.quantity) == ValueError:
                pytest.raises(ValueError)

        total_price = self.get_total_price()
        assert user.user_money > total_price, (f"User doesn't have money to buy all his cart: "
                                          f"User have {user.user_money}, but total price is {total_price}")

        user.decrease_user_money(total_price)
        print(f"Thank you for your purchase, {user.login}! The amount of your purchase was {total_price}. "
              f"{user.user_money} left in the account")
        print('Have a nice day')
        self.clear()


