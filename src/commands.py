from typing import Final

from prompt_toolkit.completion import NestedCompleter

# Общие команды
HELP_CMD: Final[str] = "help"
EXIT_CMD: Final[str] = "exit"
CLEAR_CMD: Final[str] = "clear"

# Команды для складов
LIST_WAREHOUSES_CMD: Final[str] = "list warehouses"
SHOW_WAREHOUSE_CMD: Final[str] = "show warehouse"
ADD_WAREHOUSE_CMD: Final[str] = "add warehouse"
EDIT_WAREHOUSE_CMD: Final[str] = "edit warehouse"
DELETE_WAREHOUSE_CMD: Final[str] = "delete warehouse"

# Команды для товаров
LIST_PRODUCTS_CMD: Final[str] = "list products"
SHOW_PRODUCT_CMD: Final[str] = "show product"
ADD_PRODUCT_CMD: Final[str] = "add product"
EDIT_PRODUCT_CMD: Final[str] = "edit product"
DELETE_PRODUCT_CMD: Final[str] = "delete product"

# Сам список для автодополнения
COMMANDS: Final[list[str]] = [
    HELP_CMD,
    EXIT_CMD,
    CLEAR_CMD,
    LIST_WAREHOUSES_CMD,
    SHOW_WAREHOUSE_CMD,
    ADD_WAREHOUSE_CMD,
    EDIT_WAREHOUSE_CMD,
    DELETE_WAREHOUSE_CMD,
    LIST_PRODUCTS_CMD,
    SHOW_PRODUCT_CMD,
    ADD_PRODUCT_CMD,
    EDIT_PRODUCT_CMD,
    DELETE_PRODUCT_CMD,
]

COMPLETER: Final[NestedCompleter] = NestedCompleter.from_nested_dict(
    {
        "help": None,
        "exit": None,
        "clear": None,
        "list": {
            "warehouses": None,
            "products": None,
        },
        "show": {
            "warehouse": None,  # После этого ничего не подсказываем
            "product": None,
        },
        "add": {
            "warehouse": None,
            "product": None,
        },
        "edit": {
            "warehouse": None,
            "product": None,
        },
        "delete": {
            "warehouse": None,
            "product": None,
        },
    }
)
