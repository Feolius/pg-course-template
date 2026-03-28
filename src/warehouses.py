from dataclasses import dataclass

from prompt_toolkit import prompt
from psycopg import Connection
from psycopg.rows import class_row
from rich.panel import Panel
from rich.table import Table
from validators import NonEmptyValidator, YesNoValidator

from console import console, render_error


@dataclass
class Warehouse:
    id: int
    name: str
    address: str


class WarehousesHandler:
    def __init__(self, conn: Connection):
        self.conn = conn

    @staticmethod
    def _render_warehouse(warehouse: Warehouse) -> None:
        table = Table(show_header=False, box=None, padding=(0, 2))

        table.add_column("Поле", style="bold cyan", width=15)
        table.add_column("Значение", style="white")

        table.add_row("ID", str(warehouse.id))
        table.add_row("Название", warehouse.name)
        table.add_row("Адрес", warehouse.address)

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
        table.add_column("Название", style="green", min_width=20)
        table.add_column("Адрес", style="yellow", min_width=30)

        with self.conn.cursor(row_factory=class_row(Warehouse)) as cur:
            cur.execute("SELECT * FROM catalog.warehouses")
            warehouses: list[Warehouse] = cur.fetchall()

        for warehouse in warehouses:
            table.add_row(str(warehouse.id), warehouse.name, warehouse.address)
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
        name = prompt("Название склада: ", validator=NonEmptyValidator()).strip()
        address = prompt("Адрес: ", validator=NonEmptyValidator()).strip()
        self.conn.execute(
            "INSERT INTO catalog.warehouses (name, address) VALUES (%s, %s)",
            (name, address),
        )
        console.print(f"[green]Склад {name} добавлен [/green]")

    def edit_warehouse(self, _id: int) -> None:
        with self.conn.cursor(row_factory=class_row(Warehouse)) as cur:
            cur.execute("SELECT * FROM catalog.warehouses WHERE id = %s", (_id,))
            warehouse: Warehouse | None = cur.fetchone()

        if warehouse is None:
            render_error(f"Склад с ID {_id} не найден")
            return

        name = prompt(
            "Название склада: ",
            default=warehouse.name,
            validator=NonEmptyValidator(),
        ).strip()
        address = prompt(
            "Адрес: ", default=warehouse.address, validator=NonEmptyValidator()
        ).strip()
        self.conn.execute(
            """UPDATE catalog.warehouses SET name = %s, address = %s
            WHERE id = %s""",
            (name, address, _id),
        )
        console.print(f"[green]Склад {name} обновлен [/green]")

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
            console.print(f"[green]Склад {warehouse.name} удален [/green]")
