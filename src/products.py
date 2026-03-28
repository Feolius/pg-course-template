from dataclasses import dataclass
from decimal import Decimal

from psycopg import Connection


@dataclass
class Product:
    id: int
    sku: str
    name: str
    price: Decimal
    category: str


class ProductsHandler:
    def __init__(self, conn: Connection):
        self.conn = conn

    def _render_product(self, product: Product):
        """
        Отображает информацию о продукте в виде таблицы внутри панели.
        Используйте rich.table.Table и rich.panel.Panel для форматирования.
        """

    def list_products(self) -> None:
        """
        Выводит список всех продуктов из таблицы catalog.products.
        Используйте rich.table.Table для отображения данных.
        Колонки: ID, SKU, Название, Цена, Категория
        """

    def show_product(self, _id: int) -> None:
        """
        Показывает детальную информацию о продукте по его ID.
        Если продукт не найден, выводит ошибку через _render_error.
        Используйте _render_product для отображения найденного продукта.
        """

    def add_product(self) -> None:
        """
        Добавляет новый продукт в базу данных.
        Запрашивает у пользователя: SKU, название, цену и категорию.
        Используйте prompt с валидаторами для ввода данных.
        """

    def edit_product(self, _id: int) -> None:
        """
        Редактирует существующий продукт.
        Сначала проверяет существование продукта по ID.
        Предлагает текущие значения как default при вводе новых данных.
        """

    def delete_product(self, _id: int) -> None:
        """
        Удаляет продукт из базы данных.
        Сначала показывает информацию о продукте.
        Запрашивает подтверждение перед удалением.
        """
