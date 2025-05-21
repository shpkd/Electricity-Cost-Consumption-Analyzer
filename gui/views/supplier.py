"""
Module for building the supplier selection view.
Includes logic for handling selection state,
and scraping tariff data based on the chosen provider.
"""

import flet as ft
from data.constants import SUPPLIERS
from src.errors import InternalError
from src.scraper import scrape_supplier
from src.storage import save_data
from gui.components.button_group import BackButton, ContinueButton
from gui.components.grid import build_grid


def suppl_elect_view(page: ft.Page)->ft.View:
    """
    Builds and returns the electricity supplier selection view with a selectable card
    grid and confirmation button.
    """
    selected_supplier = {"index": -1}
    supplier_rows = build_grid(page, SUPPLIERS, selected_supplier)

    def on_confirm():
        """
        Handles the 'Continue' button click.
        Saves selected supplier and navigates to the next view,
        or shows a warning if none is selected.
        """
        index = selected_supplier["index"]

        if isinstance(index, int):
            supplier = SUPPLIERS[index]
            selected_name = supplier[0]
            try:
                data = scrape_supplier(supplier_link_text=selected_name)
                save_data(data, "data/supplier_data.json")
                page.go("/distributor")
            except InternalError:
                error_text.value = "⛔Nepodařilo se načíst data. Zkontrolujte připojení k internetu"
                page.update()
        else:
            error_text.value = "⛔Vyberte dodavatele"
            page.update()

    error_text = ft.Text("", color=ft.colors.RED)
    return ft.View(
        route="/supplier-electricity",
        controls=[
            ft.Row(
                controls=[BackButton(page, route="/")],
                alignment="start"
            ),
            ft.Text("🔋Vyberte svého dodavatele elektřiny", size=30, weight="bold"),
            ft.Column(
                controls=supplier_rows,
                alignment="center",
                spacing=15
            ),
            ContinueButton(lambda e: on_confirm()),
            error_text,
        ],
        horizontal_alignment="center",
        scroll="auto"
    )
