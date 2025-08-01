from __future__ import annotations

from typing import Self, Any
from abc import ABC, abstractmethod

class BaseProduct:
    @abstractmethod
    def __init__(self) -> None:
        pass


class MixinInfo:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        class_name = self.__class__.__name__
        print(f"Создан объект класса {class_name} с аргументами: args={args}, kwargs={kwargs}")
        super().__init__(*args, **kwargs)


class Product(MixinInfo, BaseProduct):
    name: str
    description: str
    __price: float
    quantity: int

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        if quantity == 0:
            raise ValueError(
                f"Товар с нулевым количеством не может быть добавлен")
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__()


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
    def new_product(
        cls, name: str, description: str, price: float, quantity: int
    ) -> "Product":
        return cls(name, description, price, quantity)

    def __add__(self, other: Self) -> float:
        if type(self) is not type(other):
            raise TypeError(
                f"Нельзя складывать товары разных типов: {type(self).__name__} и {type(other).__name__}"
            )
        return (self.price * self.quantity) + (other.__price * other.quantity)

    def __str__(self) -> str:
        return f"{self.name} ({self.price} руб., {self.quantity} шт)"

    def __repr__(self) -> str:
        return self.__str__()


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        __price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, __price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        __price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, __price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

