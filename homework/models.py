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
            self.products[product] = new_buy_count
        else:
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

    def buy(self, user_money):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for product in self.products:
            if product.check_quantity(product.quantity) == ValueError:
                raise ValueError

        total_price = self.get_total_price()
        if user_money < total_price:
            user_cart = list()
            for product in self.products:
                user_cart.append(f'{product.name}, {product.quantity}, {product.price}')
            return False, (f"User doesn't have money to buy this cart: {user_cart}. "
                           f"User have {user_money}, but total price is {total_price}")
        else:
            user_money -= total_price
            self.clear()


class User:
    """
    Класс пользователя
    """
    user_money: int
