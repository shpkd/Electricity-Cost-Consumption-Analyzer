"""
Module for creating button components used in the application navigation.
"""
import flet as ft

def BackButton(page, route):
    """
    Create a back navigation button with predefined styling.
    """
    return ft.ElevatedButton(
        text="⬅",
        on_click=lambda e: page.go(route),
        width=60,
        height=60,
        bgcolor="#00796B",
        color="white"
    )

def ContinueButton(on_click_fn):
    """
    Create a continue button with predefined styling.
    """
    return ft.ElevatedButton(
        text="Pokračovat",
        width=240,
        height=60,
        on_click=on_click_fn,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor="#00796B",
            color="white"
        )
    )
