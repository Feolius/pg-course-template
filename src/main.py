import logging

from prompt_toolkit import PromptSession
from psycopg import Connection
import psycopg
from rich.panel import Panel

from commands import *  # pylint: disable=wildcard-import,unused-wildcard-import
from setup import setup_logger
from warehouses import WarehousesHandler
from products import ProductsHandler
from console import console, render_error

DB_NAME: Final[str] = "inventorydb"
DB_USER: Final[str] = "app_user"
DB_PASSWORD: Final[str] = "pass"
DB_HOST: Final[str] = "127.0.0.1"
DB_PORT: Final[int] = 5432


# Если нужно получить больше деталей о psycopg, следует изменить log level на DEBUG
setup_logger(psycopg_log_level=logging.INFO)


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
    logging.info("App Started")

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
            if _input == EXIT_CMD.text:
                break

            if _input == HELP_CMD.text:
                show_help()
            elif _input == CLEAR_CMD.text:
                console.clear()

            # Склады
            elif _input == LIST_WAREHOUSES_CMD.text:
                warehouses_handler.list_warehouses()
            elif _input.startswith(SHOW_WAREHOUSE_CMD.text):
                warehouse_id = int(get_args(_input, SHOW_WAREHOUSE_CMD)["id"])
                warehouses_handler.show_warehouse(warehouse_id)
            elif _input == ADD_WAREHOUSE_CMD.text:
                warehouses_handler.add_warehouse()
            elif _input.startswith(EDIT_WAREHOUSE_CMD.text):
                warehouse_id = int(get_args(_input, EDIT_WAREHOUSE_CMD)["id"])
                warehouses_handler.edit_warehouse(warehouse_id)
            elif _input.startswith(DELETE_WAREHOUSE_CMD.text):
                warehouse_id = int(get_args(_input, DELETE_WAREHOUSE_CMD)["id"])
                warehouses_handler.delete_warehouse(warehouse_id)

            # Продукты
            elif _input == LIST_PRODUCTS_CMD.text:
                products_handler.list_products()
            elif _input.startswith(SHOW_PRODUCT_CMD.text):
                product_id = int(get_args(_input, SHOW_PRODUCT_CMD)["id"])
                products_handler.show_product(product_id)
            elif _input == ADD_PRODUCT_CMD.text:
                products_handler.add_product()
            elif _input.startswith(EDIT_PRODUCT_CMD.text):
                product_id = int(get_args(_input, EDIT_PRODUCT_CMD)["id"])
                products_handler.edit_product(product_id)
            elif _input.startswith(DELETE_PRODUCT_CMD.text):
                product_id = int(get_args(_input, DELETE_PRODUCT_CMD)["id"])
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
    categories = {}
    for cmd in COMMANDS:
        if cmd.category not in categories:
            categories[cmd.category] = []
        categories[cmd.category].append(cmd)

    help_lines = []

    for category_name in CATEGORIES:
        if category_name in categories:
            help_lines.append(f"[bold cyan]{category_name}:[/bold cyan]")
            for cmd in categories[category_name]:
                cmd_help = cmd.text
                if cmd.args:
                    cmd_help += " " + " ".join(f"<{arg}>" for arg in cmd.args)
                help_lines.append(
                    f"  [green]{cmd_help}[/green]{' ' * (30 - len(cmd_help))}- {cmd.description}"
                )
            help_lines.append("")

    help_text = "\n".join(help_lines)
    panel = Panel(help_text, title="📚 Доступные команды", border_style="cyan")

    console.print()
    console.print(panel)
    console.print()


def get_args(_input: str, command: Command) -> dict[str, str]:
    """
    Пытается извлечь аргументы для команды из ввода пользователя
    :param _input: ввод пользователя
    :param command: объект команды
    :return: словарь аргументов (ключ - имя аргумента, значение - аргумент)
    """
    _input = _input.strip()
    if not _input.startswith(command.text):
        raise ValueError(f"Input is not aligned with {command.text}")
    command_parts = command.text.split()
    input_parts = _input.split()
    args = input_parts[len(command_parts) :]
    if len(args) != len(command.args):
        raise ValueError(
            f"Command {command.text} expects {len(command.args)} argument(s)"
        )
    return dict(zip(command.args, args))


if __name__ == "__main__":
    main()
