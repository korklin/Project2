from typing import Self


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

    def __add__(self, other: Self) -> float:
        if type(self) is not type(other):
            raise TypeError(f"Нельзя складывать товары разных типов: {type(self).__name__} и {type(other).__name__}")
        return (self.price * self.quantity) + (other.__price * other.quantity)

    def __str__(self) -> str:
        return f"{self.name} ({self.price} руб., {self.quantity} шт)"

    def __repr__(self) -> str:
        return self.__str__()


class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int, efficiency: float, model: str, memory: int, color: str ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int, country: str, germination_period: str,
                 color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color



if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))
