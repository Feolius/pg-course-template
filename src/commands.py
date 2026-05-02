from dataclasses import dataclass, field
from typing import Final, Sequence

from prompt_toolkit.completion import NestedCompleter

# Категории команд
CATEGORY_GENERAL: Final[str] = "ПРОЧЕЕ"
CATEGORY_WAREHOUSES: Final[str] = "СКЛАДЫ"
CATEGORY_PRODUCTS: Final[str] = "ТОВАРЫ"

CATEGORIES: Final[Sequence[str]] = [
    CATEGORY_PRODUCTS,
    CATEGORY_WAREHOUSES,
    CATEGORY_GENERAL,
]


@dataclass(frozen=True)
class Command:
    text: str
    description: str
    category: str
    args: Sequence[str] = field(default_factory=tuple)


# Общие команды
HELP_CMD: Final[Command] = Command("help", "эта справка", CATEGORY_GENERAL)
EXIT_CMD: Final[Command] = Command("exit", "выход", CATEGORY_GENERAL)
CLEAR_CMD: Final[Command] = Command("clear", "очистить экран", CATEGORY_GENERAL)

# Команды для складов
LIST_WAREHOUSES_CMD: Final[Command] = Command(
    "list warehouses", "список всех складов", CATEGORY_WAREHOUSES
)
SHOW_WAREHOUSE_CMD: Final[Command] = Command(
    "show warehouse", "информация о складе", CATEGORY_WAREHOUSES, args=("id",)
)
ADD_WAREHOUSE_CMD: Final[Command] = Command(
    "add warehouse", "добавить склад (интерактивно)", CATEGORY_WAREHOUSES
)
EDIT_WAREHOUSE_CMD: Final[Command] = Command(
    "edit warehouse", "редактировать склад", CATEGORY_WAREHOUSES, args=("id",)
)
DELETE_WAREHOUSE_CMD: Final[Command] = Command(
    "delete warehouse", "удалить склад", CATEGORY_WAREHOUSES, args=("id",)
)

# Команды для товаров
LIST_PRODUCTS_CMD: Final[Command] = Command(
    "list products", "список всех товаров", CATEGORY_PRODUCTS
)
SHOW_PRODUCT_CMD: Final[Command] = Command(
    "show product", "информация о товаре", CATEGORY_PRODUCTS, args=("id",)
)
ADD_PRODUCT_CMD: Final[Command] = Command(
    "add product", "добавить товар (интерактивно)", CATEGORY_PRODUCTS
)
EDIT_PRODUCT_CMD: Final[Command] = Command(
    "edit product", "редактировать товар", CATEGORY_PRODUCTS, args=("id",)
)
DELETE_PRODUCT_CMD: Final[Command] = Command(
    "delete product", "удалить товар", CATEGORY_PRODUCTS, args=("id",)
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


def _build_completer_dict() -> dict:
    result: dict = {}
    for cmd in COMMANDS:
        words = cmd.text.split()
        current = result
        for word in words[:-1]:
            if word not in current:
                current[word] = {}
            current = current[word]
        current[words[-1]] = None
    return result


COMPLETER: Final[NestedCompleter] = NestedCompleter.from_nested_dict(
    _build_completer_dict()
)
