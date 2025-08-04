from typing import Tuple

import pytest
from _pytest.capture import CaptureFixture, capfd

from src.class_category import Category
from src.class_product import LawnGrass, Smartphone


@pytest.fixture
def new_products() -> Tuple[Smartphone, Smartphone, Smartphone, LawnGrass, LawnGrass]:
    return (
        Smartphone("Samsung", "desc", 100.0, 1, 90.0, "S1", 128, "black"),
        Smartphone("iPhone", "desc", 200.0, 2, 95.0, "15", 256, "silver"),
        Smartphone("Redmi", "desc", 300.0, 3, 85.0, "Note", 64, "blue"),
        LawnGrass("Газон", "desc", 500.0, 10, "Россия", "7 дней", "зелёный"),
        LawnGrass("Газон2", "desc", 600.0, 5, "США", "5 дней", "тёмно-зелёный"),
    )


def test_add_same_type_products(
    new_products: Tuple[Smartphone, Smartphone, Smartphone, LawnGrass, LawnGrass],
) -> None:
    """
    Проверяет корректность работы оператора сложения (__add__) для объектов одного типа:
    смартфоны складываются друг с другом, газоны с газонами.
    """
    s1, s2, _, g1, g2 = new_products
    assert s1 + s2 == (100.0 * 1 + 200.0 * 2)
    assert g1 + g2 == (500.0 * 10 + 600.0 * 5)


def test_add_different_type_raises(
    new_products: Tuple[Smartphone, Smartphone, Smartphone, LawnGrass, LawnGrass],
) -> None:
    """
    Проверяет, что попытка сложения объектов разных типов вызывает исключение TypeError.
    Например: Smartphone + LawnGrass.
    """
    s1, _, _, g1, _ = new_products
    with pytest.raises(TypeError):
        _ = s1 + g1  # type: ignore[operator]


def test_add_product_smartphone(
    new_products: Tuple[Smartphone, Smartphone, Smartphone, LawnGrass, LawnGrass],
) -> None:
    """
    Проверяет успешное добавление смартфона в категорию методом add_product_smartphone.
    """
    s1, s2, _, _, _ = new_products
    category = Category("Смартфоны", "desc", [s1])
    category.add_product_smartphone(s2)
    assert s2 in category.products


def test_add_product_lawngrass(
    new_products: Tuple[Smartphone, Smartphone, Smartphone, LawnGrass, LawnGrass],
) -> None:
    """
    Проверяет успешное добавление газонной травы в категорию методом add_product_lawngrass.
    """
    _, _, _, g1, g2 = new_products
    category = Category("Травы", "desc", [g1])
    category.add_product_lawngrass(g2)
    assert g2 in category.products


def test_add_invalid_type_to_specific_method(
    new_products: Tuple[Smartphone, Smartphone, Smartphone, LawnGrass, LawnGrass],
) -> None:
    """
    Проверяет, что метод add_product_smartphone вызывает TypeError при попытке добавить
    объект другого типа (LawnGrass).
    """
    s1, _, _, g1, _ = new_products
    category = Category("Смартфоны", "desc", [s1])
    with pytest.raises(TypeError):
        category.add_product_smartphone(g1)  # type: ignore[arg-type] # Нельзя добавлять траву как смартфон


def test_smartphone_creation_logs_output(capfd: CaptureFixture[str]) -> None:
    """
    Проверка, что логгирование работает и для подклассов.
    """
    smartphone = Smartphone("iPhone", "desc", 200.0, 2, 95.0, "15",
                            256, "silver")
    out, _ = capfd.readouterr()
    assert "Создан объект класса Smartphone" in out
