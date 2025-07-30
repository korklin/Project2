from typing import Iterator, Tuple, Any

import pytest
from _pytest.capture import CaptureFixture

from src.class_made import Category, Product


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


def test_add_product_to_category(
    products: Tuple[Product, Product, Product, Product],
) -> None:
    """
    Проверяет добавление нового продукта в уже существующую категорию, а также инкремент счётчика продуктов.
    """
    product1, product2, *_ = products
    category: Category = Category("Гаджеты", "Описание", [product1])
    old_count: int = len(category.products)
    Category.product_count = 0  # сброс счётчика

    category.add_product(product2)

    assert len(category.products) == old_count + 1
    assert product2 in category.products
    assert Category.product_count == 1


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


def test_adding_same_product_twice(
    products: Tuple[Product, Product, Product, Product],
) -> None:
    """
    Убеждается, что один и тот же продукт можно добавить в категорию несколько раз,
    и он действительно будет продублирован в списке.
    """
    product1, *_ = products
    category: Category = Category("Повторы", "desc", [product1])
    initial_count: int = len(category.products)

    category.add_product(product1)

    assert category.products.count(product1) == 2
    assert len(category.products) == initial_count + 1


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


def test_category_str(categories: Tuple[Category, Category]) -> None:
    category1, category2 = categories
    assert str(category1) == "Смартфоны, количество продуктов: 27 шт)"
    assert str(category2) == "Телевизоры, количество продуктов: 7 шт)"
