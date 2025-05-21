"""
Module for creating supplier grid components with selection functionality.
"""

import flet as ft

# @generated module(partially) ChatGPT 4o
def create_supplier_card(name, image_path, on_click):
    """
    Creates a styled supplier card component containing a logo and supplier name.
    """
    return ft.Container(
        content=ft.Column([
            ft.Image(src=image_path, width=200, height=170),
            ft.Text(name, weight="bold", size=13, text_align="center")
        ],
        horizontal_alignment="center",
        spacing=10),
        width=320,
        height=220,
        alignment=ft.alignment.center,
        bgcolor="white",
        border_radius=12,
        border=ft.border.all(2, "black"),
        on_click=on_click
    )

def on_select_factory(page, selected_supplier, supplier_cards):
    """
    Returns a click handler factory that updates the selected supplier index
    and visually highlights the chosen card.
    """
    def on_select(index):
        def handler():
            selected_supplier["index"] = index
            for _, card in enumerate(supplier_cards):
                card.border = ft.border.all(2, "#CCCCCC")
            supplier_cards[index].border = ft.border.all(2, "#00796B")
            page.update()
        return lambda e: handler()
    return on_select

def build_grid(page, suppliers, selected_supplier):
    """
    Creates a grid of supplier cards with selection support,
    arranged in rows of three.
    """
    supplier_cards = []
    on_select = on_select_factory(page, selected_supplier, supplier_cards)

    for i, (name, image_path) in enumerate(suppliers):
        card = create_supplier_card(name, image_path, on_select(i))
        supplier_cards.append(card)

    rows = []
    row_cards = []
    for _, card in enumerate(supplier_cards):
        row_cards.append(card)
        if len(row_cards) == 3 or len(row_cards) == len(supplier_cards)%3:
            rows.append(ft.Row(controls=row_cards, alignment="center", spacing=15))
            row_cards = []
    return rows
