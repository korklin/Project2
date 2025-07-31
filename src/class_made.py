
class Product:
    name: str
    description: str
    __price: float
    quantity: int

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
       if value <= 0:
           print("Цена не должна быть нулевая или отрицательная")
       else:
           self.__price = value

    @classmethod
    def new_product(cls, name: str, description: str, price: float, quantity: int) -> "Product":
        return cls(name, description, price, quantity)

    def __add__(self, other: 'Product') -> float:
        if isinstance(other, Product):
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Можно складывать только объекты класса Product.")

    def __str__(self) -> str:
        return f"{self.name} ({self.price} руб., {self.quantity} шт)"

    def __repr__(self) -> str:
        return self.__str__()


class Category:
    name: str
    description: str
    __products: list[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list) -> None:
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


    @property
    def products(self) -> list[Product]:
        """Возвращает копию списка товаров (только для чтения)."""
        return self.__products.copy()

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт)"


if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)
