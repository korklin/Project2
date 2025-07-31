from typing import Tuple, Any

import pytest
from _pytest.capture import CaptureFixture

from src.class_product import Product


@pytest.fixture
def products() -> Tuple[Product, Product, Product, Product]:
    """
    Создаёт 4 тестовых продукта.
    """
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    return product1, product2, product3, product4


def test_product_fields(products: Tuple[Product, Product, Product, Product]) -> None:
    """
    Проверяет корректность сохранения полей объектов Product после инициализации.
    """
    product1, product2, product3, _ = products
    assert product1.name == "Samsung Galaxy S23 Ultra"
    assert product1.description == "256GB, Серый цвет, 200MP камера"
    assert product1.price == 180000.0
    assert product1.quantity == 5

    assert product2.name == "Iphone 15"
    assert product2.description == "512GB, Gray space"
    assert product2.price == 210000.0
    assert product2.quantity == 8

    assert product3.name == "Xiaomi Redmi Note 11"
    assert product3.description == "1024GB, Синий"
    assert product3.price == 31000.0
    assert product3.quantity == 14

def test_new_product_creation() -> None:
    """
    Проверяет, что метод new_product создаёт объект класса Product
    с правильными значениями атрибутов: name, description, price и quantity.
    """
    product = Product.new_product(
        name="Наушники",
        description="Беспроводные, с шумоподавлением",
        price=5990.0,
        quantity=12
    )

    assert isinstance(product, Product)
    assert product.name == "Наушники"
    assert product.description == "Беспроводные, с шумоподавлением"
    assert product.price == 5990.0
    assert product.quantity == 12


def test_price_getter() -> None:
    """
    Проверяет, что геттер price возвращает корректное значение.
    """
    product = Product("Кофеварка", "Капельная кофеварка", 4990.0, 5)
    assert product.price == 4990.0


def test_price_setter_valid_value(capsys: CaptureFixture[str]) -> None:
    """
    Проверяет, что сеттер устанавливает новую корректную цену.
    """
    product = Product("Кофеварка", "Капельная кофеварка", 4990.0, 5)
    product.price = 3990.0
    assert product.price == 3990.0

    captured = capsys.readouterr()
    assert captured.out == ""  # Ничего не должно выводиться


def test_price_setter_invalid_value_does_not_change_price(capsys: CaptureFixture[str]) -> None:
    """
    Проверяет, что при попытке установить цену <= 0,
    значение не меняется и выводится предупреждение.
    """
    product = Product("Кофеварка", "Капельная кофеварка", 4990.0, 5)
    product.price = 0.0  # Некорректная цена

    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 4990.0  # Значение не изменилось

    product.price = -100  # Тоже некорректная цена
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 4990.0


def test_add_products(products: Tuple[Product, Product, Product, Product]) -> None:
    p1, p2, *_ = products
    assert p1 + p2 == (180000.0 * 5 + 210000.0 * 8)


def test_add_invalid_type(products: Tuple[Product, Product, Product, Product]) -> None:
    p1, *_ = products
    not_a_product: Any = "не продукт"
    with pytest.raises(TypeError):
        _ = p1 + not_a_product


def test_product_str(products: Tuple[Product, Product, Product, Product]) -> None:
    p1, *_ = products
    assert str(p1) == "Samsung Galaxy S23 Ultra (180000.0 руб., 5 шт)"


def test_product_repr(products: Tuple[Product, Product, Product, Product]) -> None:
    _, p2, *_ = products
    assert repr(p2) == "Iphone 15 (210000.0 руб., 8 шт)"