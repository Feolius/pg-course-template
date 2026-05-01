from dataclasses import dataclass
from typing import Final

from prompt_toolkit.completion import NestedCompleter

# Категории команд
CATEGORY_GENERAL: Final[str] = "ПРОЧЕЕ"
CATEGORY_WAREHOUSES: Final[str] = "СКЛАДЫ"
CATEGORY_PRODUCTS: Final[str] = "ТОВАРЫ"


@dataclass(frozen=True)
class Command:
    text: str
    description: str
    category: str


# Общие команды
HELP_CMD: Final[Command] = Command("help", "эта справка", CATEGORY_GENERAL)
EXIT_CMD: Final[Command] = Command("exit", "выход", CATEGORY_GENERAL)
CLEAR_CMD: Final[Command] = Command("clear", "очистить экран", CATEGORY_GENERAL)

# Команды для складов
LIST_WAREHOUSES_CMD: Final[Command] = Command(
    "list warehouses", "список всех складов", CATEGORY_WAREHOUSES
)
SHOW_WAREHOUSE_CMD: Final[Command] = Command(
    "show warehouse", "информация о складе", CATEGORY_WAREHOUSES
)
ADD_WAREHOUSE_CMD: Final[Command] = Command(
    "add warehouse", "добавить склад (интерактивно)", CATEGORY_WAREHOUSES
)
EDIT_WAREHOUSE_CMD: Final[Command] = Command(
    "edit warehouse", "редактировать склад", CATEGORY_WAREHOUSES
)
DELETE_WAREHOUSE_CMD: Final[Command] = Command(
    "delete warehouse", "удалить склад", CATEGORY_WAREHOUSES
)

# Команды для товаров
LIST_PRODUCTS_CMD: Final[Command] = Command(
    "list products", "список всех товаров", CATEGORY_PRODUCTS
)
SHOW_PRODUCT_CMD: Final[Command] = Command(
    "show product", "информация о товаре", CATEGORY_PRODUCTS
)
ADD_PRODUCT_CMD: Final[Command] = Command(
    "add product", "добавить товар (интерактивно)", CATEGORY_PRODUCTS
)
EDIT_PRODUCT_CMD: Final[Command] = Command(
    "edit product", "редактировать товар", CATEGORY_PRODUCTS
)
DELETE_PRODUCT_CMD: Final[Command] = Command(
    "delete product", "удалить товар", CATEGORY_PRODUCTS
)

# Сам список для автодополнения
COMMANDS: Final[list[Command]] = [
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
