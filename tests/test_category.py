from typing import Iterator, Tuple

import pytest

from src.class_product import Product
from src.class_category import Category


@pytest.fixture(autouse=True)
def reset_counters() -> Iterator[None]:
    """
    Автоматически сбрасывает счётчики category_count и product_count
    перед каждым тестом, чтобы обеспечить независимость тестов.
    """
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def products() -> Tuple[Product, Product, Product, Product]:
    """
    Создаёт 4 тестовых продукта.
    """
    return (
        Product("Samsung Galaxy", "desc", 100.0, 1),
        Product("Iphone", "desc", 200.0, 2),
        Product("Redmi", "desc", 300.0, 3),
        Product("Телевизор", "desc", 400.0, 4),
    )


@pytest.fixture
def categories(
    products: Tuple[Product, Product, Product, Product],
) -> Tuple[Category, Category]:
    """
    Создаёт 2 категории с соответствующими продуктами.
    """
    product1, product2, product3, product4 = products
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4],
    )
    return category1, category2


def test_category_initialization(categories: Tuple[Category, Category]) -> None:
    """
    Убеждается, что категории создаются с правильными полями и нужным количеством продуктов.
    """
    category1, category2 = categories

    assert category1.name == "Смартфоны"
    assert category1.description.startswith("Смартфоны, как средство")
    assert len(category1.products) == 3

    assert category2.name == "Телевизоры"
    assert category2.description.startswith("Современный телевизор")
    assert len(category2.products) == 1


def test_counters(categories: Tuple[Category, Category]) -> None:
    """
    Проверяет корректную работу счётчиков Category.category_count и Category.product_count
    после создания категорий с продуктами.
    """
    # category_count должно быть 2 (две категории)
    assert Category.category_count == 2
    # product_count должно быть 4 (3 + 1 товара)
    assert Category.product_count == 4


def test_category_products_objects(
    categories: Tuple[Category, Category],
    products: Tuple[Product, Product, Product, Product],
) -> None:
    """
    Удостоверяется, что все продукты в категориях являются экземплярами Product, и что это именно те объекты,
    которые были переданы при создании.
    """
    category1, category2 = categories
    product1, product2, product3, product4 = products

    # Все продукты в категории - объекты класса Product
    for p in category1.products:
        assert isinstance(p, Product)
    for p in category2.products:
        assert isinstance(p, Product)

    # Проверяем, что именно те объекты что мы передали
    assert product1 in category1.products
    assert product2 in category1.products
    assert product3 in category1.products
    assert product4 in category2.products


def test_category_init_with_non_list_raises() -> None:
    """
    Проверяет, что попытка создать категорию с аргументом products, не являющимся списком, вызывает исключение TypeError.
    """
    with pytest.raises(
        TypeError, match="products должен быть списком объектов класса Product"
    ):
        Category("Ошибка", "Описание", "не список")  # type: ignore[arg-type]


def test_category_and_product_counters_accumulate() -> None:
    """
    Тестирует корректность накопления значений счётчиков категорий и продуктов при множественном создании объектов.
    """
    Category.category_count = 0
    Category.product_count = 0

    p1: Product = Product("A", "desc", 10.0, 1)
    p2: Product = Product("B", "desc", 20.0, 2)

    Category("Test1", "desc", [p1])
    Category("Test2", "desc", [p2])
    Category("Test3", "desc", [p1, p2])

    assert Category.category_count == 3
    assert Category.product_count == 4


def test_products_property_returns_copy(categories: Tuple[Category, Category]) -> None:
    """
    Проверяет, что при передаче валидных параметров создаётся экземпляр
    класса Product с корректно установленными атрибутами.
    """
    category1, _ = categories
    original_len = len(category1.products)
    category1.products.append(Product("Test", "desc", 1.0, 1))  # изменит копию

    # Приватный список останется без изменений
    assert len(category1.products) == original_len


def test_category_str(categories: Tuple[Category, Category]) -> None:
    category1, category2 = categories
    assert str(category1) == "Смартфоны, количество продуктов: 6 шт)"
    assert str(category2) == "Телевизоры, количество продуктов: 4 шт)"
