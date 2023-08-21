from homework.models import Product
all_products = [
        Product("book", 100, "This is a book", 1000),
        Product("car", 120, "Super and fast car", 12),
        Product("pen", 5, "This is a pen", 12939),
    ]
all_products_dict = {
        Product("book", 100, "This is a book", 1000) : 12,
        Product("car", 120, "Super and fast car", 12) : 4,
        Product("pen", 5, "This is a pen", 12939):8,
}
all_products_list = all_products_dict.keys()
for product in all_products_list:
    print(all_products_dict[product])

