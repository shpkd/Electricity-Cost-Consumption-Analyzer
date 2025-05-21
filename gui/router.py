"""
Initializes the Flet page, sets up routing between views,
and handles navigation events.
"""
import os
import flet as ft
from src.storage import load_data
from gui.views.start import home_view
from gui.views.supplier import suppl_elect_view
from gui.views.setup import distribut_view
from gui.views.result import result_view
from gui.views.reset import reset_view


def main(page: ft.Page):
    """
    Initializes the application page, sets up the theme,
    and defines route navigation logic.
    """
    page.title = "Energy calculator"
    page.theme_mode = "light"

    def route_change(_):
        page.views.clear()
        if page.route == "/":
            page.views.append(home_view(page))
        elif page.route == "/supplier-electricity":
            page.views.append(suppl_elect_view(page))
        elif page.route =="/distributor":
            page.views.append(distribut_view(page))
        elif page.route=="/result":
            page.views.append(result_view(page))
        elif page.route == "/confirm-reset":
            page.views.append(reset_view(page))
        page.update()

    page.on_route_change = route_change

    if os.path.exists("data/calculate_data.json") and os.path.exists("data/graph_data.json") and load_data("data/calculate_data.json") and load_data("data/graph_data.json"):
        page.go("/result")
    else:
        page.go("/")
ft.app(target=main, assets_dir="gui/assets")
