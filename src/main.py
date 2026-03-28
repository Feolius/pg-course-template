from prompt_toolkit import PromptSession
from psycopg import Connection
import psycopg
from rich.panel import Panel

from commands import *  # pylint: disable=wildcard-import,unused-wildcard-import
from warehouses import WarehousesHandler
from products import ProductsHandler
from console import console, render_error

DB_NAME: Final[str] = "inventorydb"
DB_USER: Final[str] = "app_user"
DB_PASSWORD: Final[str] = "pass"
DB_HOST: Final[str] = "127.0.0.1"
DB_PORT: Final[int] = 5432


def main() -> None:  # pylint: disable=too-many-statements
    # Подключение к БД
    conn: Connection = psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        autocommit=True,
    )

    warehouses_handler = WarehousesHandler(conn)
    products_handler = ProductsHandler(conn)

    # Вывод заголовка через rich
    console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   Inventory Management System[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]")
    console.print(f"[dim]Подключено к БД: warehouse_db (user: {DB_USER})[/dim]\n")

    # Создаём сессию prompt_toolkit с автодополнением команд.
    # https://python-prompt-toolkit.readthedocs.io/en/stable/pages/asking_for_input.html#the-promptsession-object
    session: PromptSession[str] = PromptSession(completer=COMPLETER)

    # Основной цикл
    while True:
        try:
            # Ввод команды через prompt_toolkit
            _input = session.prompt("inventory> ").strip()

            if not _input:
                continue

            # Обработка команд
            if _input == EXIT_CMD:
                break

            if _input == HELP_CMD:
                show_help()
            elif _input == CLEAR_CMD:
                console.clear()

            # Склады
            elif _input == LIST_WAREHOUSES_CMD:
                warehouses_handler.list_warehouses()
            elif _input.startswith(SHOW_WAREHOUSE_CMD):
                warehouse_id = int(get_args(_input, SHOW_WAREHOUSE_CMD, 1)[0])
                warehouses_handler.show_warehouse(warehouse_id)
            elif _input == ADD_WAREHOUSE_CMD:
                warehouses_handler.add_warehouse()
            elif _input.startswith(EDIT_WAREHOUSE_CMD):
                warehouse_id = int(get_args(_input, EDIT_WAREHOUSE_CMD, 1)[0])
                warehouses_handler.edit_warehouse(warehouse_id)
            elif _input.startswith(DELETE_WAREHOUSE_CMD):
                warehouse_id = int(get_args(_input, DELETE_WAREHOUSE_CMD, 1)[0])
                warehouses_handler.delete_warehouse(warehouse_id)

            # Продукты
            elif _input == LIST_PRODUCTS_CMD:
                products_handler.list_products()
            elif _input.startswith(SHOW_PRODUCT_CMD):
                product_id = int(get_args(_input, SHOW_PRODUCT_CMD, 1)[0])
                products_handler.show_product(product_id)
            elif _input == ADD_PRODUCT_CMD:
                products_handler.add_product()
            elif _input.startswith(EDIT_PRODUCT_CMD):
                product_id = int(get_args(_input, EDIT_PRODUCT_CMD, 1)[0])
                products_handler.edit_product(product_id)
            elif _input.startswith(DELETE_PRODUCT_CMD):
                product_id = int(get_args(_input, DELETE_PRODUCT_CMD, 1)[0])
                products_handler.delete_product(product_id)
            else:
                console.print(f"[red]Неизвестная команда: {_input}[/red]")
                console.print("[dim]Введите 'help' для списка команд[/dim]\n")

        except KeyboardInterrupt:
            break
        except Exception as e:
            render_error(f"Ошибка: {e}")

    conn.close()  # pylint: disable=no-member
    console.print("\n[cyan]До свидания![/cyan]\n")


def show_help():
    """Справка - вывод через rich"""
    help_text = """
[bold cyan]ТОВАРЫ:[/bold cyan]
  [green]list products[/green]          - список всех товаров
  [green]show product <id>[/green]      - информация о товаре
  [green]add product[/green]            - добавить товар (интерактивно)
  [green]edit product <id>[/green]      - редактировать товар
  [green]delete product <id>[/green]    - удалить товар

[bold cyan]СКЛАДЫ:[/bold cyan]
  [green]list warehouses[/green]        - список всех складов
  [green]show warehouse <id>[/green]    - информация о складе
  [green]add warehouse[/green]          - добавить склад (интерактивно)
  [green]edit warehouse <id>[/green]    - редактировать склад
  [green]delete warehouse <id>[/green]  - удалить склад

[bold cyan]ПРОЧЕЕ:[/bold cyan]
  [green]help[/green]                   - эта справка
  [green]clear[/green]                  - очистить экран
  [green]exit[/green]                   - выход
"""

    panel = Panel(help_text, title="📚 Доступные команды", border_style="cyan")

    console.print()
    console.print(panel)
    console.print()


def get_args(_input: str, command: str, expected: int | None = None) -> list[str]:
    """
    Пытается извлечь аргументы для команды из ввода пользователя
    :param _input: ввод пользователя
    :param command: команда
    :param expected: ожидаемое количество аргументов
    :return: список аргументов
    """
    _input = _input.strip()
    if not _input.startswith(command):
        raise ValueError(f"Input is not aligned with {command}")
    command_parts = command.split()
    input_parts = _input.split()
    args = input_parts[len(command_parts) :]
    if expected is not None and len(args) != expected:
        raise ValueError(f"Command {command} expects {expected} argument(s)")
    return args


if __name__ == "__main__":
    main()
