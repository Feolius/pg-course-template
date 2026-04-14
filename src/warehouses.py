from dataclasses import dataclass

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from psycopg import Connection
from psycopg.rows import class_row
from rich.panel import Panel
from rich.table import Table
from validators import ChoiceValidator, NonEmptyValidator, YesNoValidator

from console import console, render_error


cities = [
    "Москва",
    "Санкт-Петербург",
    "Новосибирск",
    "Екатеринбург",
    "Казань",
    "Нижний Новгород",
    "Челябинск",
    "Самара",
    "Омск",
    "Ростов-на-Дону",
    "Уфа",
    "Красноярск",
    "Воронеж",
    "Пермь",
    "Волгоград"
]

city_completer = WordCompleter(cities, ignore_case=True, sentence=True)
city_validator = ChoiceValidator(cities, message="Город должен быть из списка. Используйте Tab для автодополнения.")


@dataclass
class Warehouse:
    id: int
    city: str
    address: str
    label: str | None


class WarehousesHandler:
    def __init__(self, conn: Connection):
        self.conn = conn

    @staticmethod
    def _render_warehouse(warehouse: Warehouse) -> None:
        table = Table(show_header=False, box=None, padding=(0, 2))

        table.add_column("Поле", style="bold cyan", width=15)
        table.add_column("Значение", style="white")

        table.add_row("ID", str(warehouse.id))
        table.add_row("Город", warehouse.city)
        table.add_row("Адрес", warehouse.address)
        table.add_row("Метка", warehouse.label or "")

        panel = Panel(
            table,
            expand=False,
            title=f"[bold green]Склад #{warehouse.id}[/bold green]",
            border_style="green",
        )

        console.print(panel)

    def list_warehouses(self) -> None:
        table = Table(title="Склады", show_header=True, header_style="bold cyan")

        table.add_column("ID", style="dim", width=6, justify="right")
        table.add_column("Город", style="green", min_width=20)
        table.add_column("Адрес", style="yellow", min_width=30)
        table.add_column("Метка", style="magenta", min_width=15)

        with self.conn.cursor(row_factory=class_row(Warehouse)) as cur:
            cur.execute("SELECT * FROM catalog.warehouses")
            warehouses: list[Warehouse] = cur.fetchall()

        for warehouse in warehouses:
            table.add_row(str(warehouse.id), warehouse.city, warehouse.address, warehouse.label or "")
        console.print(table)

    def show_warehouse(self, _id: int) -> None:
        with self.conn.cursor(row_factory=class_row(Warehouse)) as cur:
            cur.execute("SELECT * FROM catalog.warehouses WHERE id = %s", (_id,))
            warehouse: Warehouse | None = cur.fetchone()

        if warehouse is None:
            render_error(f"Склад с ID {_id} не найден")
            return

        self._render_warehouse(warehouse)

    def add_warehouse(self) -> None:
        city = prompt(
            "Город: ",
            validator=city_validator,
            completer=city_completer
        ).strip()
        address = prompt("Адрес: ", validator=NonEmptyValidator()).strip()
        label = prompt("Метка (необязательно): ").strip() or None
        self.conn.execute(
            "INSERT INTO catalog.warehouses (city, address, label) VALUES (%s, %s, %s)",
            (city, address, label),
        )
        if label:
            console.print(f"[green]Склад в городе {city} ({label}) добавлен [/green]")
        else:
            console.print(f"[green]Склад в городе {city} добавлен [/green]")

    def edit_warehouse(self, _id: int) -> None:
        with self.conn.cursor(row_factory=class_row(Warehouse)) as cur:
            cur.execute("SELECT * FROM catalog.warehouses WHERE id = %s", (_id,))
            warehouse: Warehouse | None = cur.fetchone()

        if warehouse is None:
            render_error(f"Склад с ID {_id} не найден")
            return

        city = prompt(
            "Город: ",
            default=warehouse.city,
            validator=city_validator,
            completer=city_completer
        ).strip()
        address = prompt(
            "Адрес: ", default=warehouse.address, validator=NonEmptyValidator()
        ).strip()
        label = prompt("Метка (необязательно): ", default=warehouse.label or "").strip() or None
        self.conn.execute(
            """UPDATE catalog.warehouses SET city = %s, address = %s, label = %s
            WHERE id = %s""",
            (city, address, label, _id),
        )
        if label:
            console.print(f"[green]Склад в городе {city} ({label}) обновлен [/green]")
        else:
            console.print(f"[green]Склад в городе {city} обновлен [/green]")

    def delete_warehouse(self, _id: int) -> None:
        with self.conn.cursor(row_factory=class_row(Warehouse)) as cur:
            cur.execute("SELECT * FROM catalog.warehouses WHERE id = %s", (_id,))
            warehouse: Warehouse | None = cur.fetchone()

        if warehouse is None:
            render_error(f"Склад с ID {_id} не найден")
            return

        self._render_warehouse(warehouse)

        answer = prompt("Вы уверены? (y/n, д/н): ", validator=YesNoValidator())

        if answer in ["y", "yes", "д", "да"]:
            self.conn.execute("DELETE FROM catalog.warehouses WHERE id = %s", (_id,))
            if warehouse.label:
                console.print(f"[green]Склад в городе {warehouse.city} ({warehouse.label}) удален [/green]")
            else:
                console.print(f"[green]Склад в городе {warehouse.city} удален [/green]")
