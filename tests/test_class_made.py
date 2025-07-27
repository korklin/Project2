from typing import Iterator, Tuple

import pytest

from src.class_made import Category, Product


@pytest.fixture(autouse=True)
def reset_counters() -> Iterator[None]:
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def products() -> Tuple[Product, Product, Product, Product]:
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    return product1, product2, product3, product4


@pytest.fixture
def categories(
    products: Tuple[Product, Product, Product, Product],
) -> Tuple[Category, Category]:
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


def test_product_fields(products: Tuple[Product, Product, Product, Product]) -> None:
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


def test_category_initialization(categories: Tuple[Category, Category]) -> None:
    category1, category2 = categories

    assert category1.name == "Смартфоны"
    assert category1.description.startswith("Смартфоны, как средство")
    assert len(category1.products) == 3

    assert category2.name == "Телевизоры"
    assert category2.description.startswith("Современный телевизор")
    assert len(category2.products) == 1


def test_counters(categories: Tuple[Category, Category]) -> None:
    # category_count должно быть 2 (две категории)
    assert Category.category_count == 2
    # product_count должно быть 4 (3 + 1 товара)
    assert Category.product_count == 4


def test_category_products_objects(
    categories: Tuple[Category, Category],
    products: Tuple[Product, Product, Product, Product],
) -> None:
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


def test_add_product_to_category(
    products: Tuple[Product, Product, Product, Product],
) -> None:
    product1, product2, *_ = products
    category: Category = Category("Гаджеты", "Описание", [product1])
    old_count: int = len(category.products)
    Category.product_count = 0  # сброс счётчика

    category.add_product(product2)

    assert len(category.products) == old_count + 1
    assert product2 in category.products
    assert Category.product_count == 1


def test_category_init_with_non_list_raises() -> None:
    with pytest.raises(
        TypeError, match="products должен быть списком объектов класса Product"
    ):
        Category("Ошибка", "Описание", "не список")  # type: ignore[arg-type]


def test_category_and_product_counters_accumulate() -> None:
    Category.category_count = 0
    Category.product_count = 0

    p1: Product = Product("A", "desc", 10.0, 1)
    p2: Product = Product("B", "desc", 20.0, 2)

    Category("Test1", "desc", [p1])
    Category("Test2", "desc", [p2])
    Category("Test3", "desc", [p1, p2])

    assert Category.category_count == 3
    assert Category.product_count == 4


def test_adding_same_product_twice(
    products: Tuple[Product, Product, Product, Product],
) -> None:
    product1, *_ = products
    category: Category = Category("Повторы", "desc", [product1])
    initial_count: int = len(category.products)

    category.add_product(product1)

    assert category.products.count(product1) == 2
    assert len(category.products) == initial_count + 1
