from __future__ import annotations

from src.class_product import LawnGrass, Product, Smartphone


class Category:
    name: str
    description: str
    __products: list[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list) -> None:
        self.quantity = None
        self.price = None
        self.name = name
        self.description = description
        self.__products = []

        if not isinstance(products, list):
            raise TypeError("products должен быть списком объектов класса Product")

        for product in products:
            if isinstance(product, Product):
                self.__products.append(product)
                Category.product_count += 1
            else:
                raise TypeError(
                    "Список должен содержать только объекты класса Product."
                )

        Category.category_count += 1

    def add_product(self, product: Product) -> None:
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product.")

    def add_product_smartphone(self, product: Smartphone) -> None:
        if isinstance(product, Smartphone):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Смартфон.")

    def add_product_lawngrass(self, product: LawnGrass) -> None:
        if isinstance(product, LawnGrass):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Газонная трава.")

    @property
    def products(self) -> list[Product]:
        """Возвращает копию списка товаров (только для чтения)."""
        return self.__products.copy()

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт)"
