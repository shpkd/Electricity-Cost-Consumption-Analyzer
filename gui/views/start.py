"""
Entry point of the electricity usage calculator app.
"""
import flet as ft

def home_view(page: ft.Page):
    """
    Builds the home view of the electricity calculator app.
    """
    return ft.View(
        route="/",
        bgcolor="#00796B",
        controls=[
            ft.Row(
                controls=[
                    ft.Text(
                        "KALKULAČKA ELEKTŘINY",
                        size=50,
                        weight="bold",
                        font_family="Poppins",
                        text_align="center",
                        color="white"
                    ),
                    ft.ElevatedButton(
                        text="💡",
                        width=150,
                        height=150,
                        on_click=lambda e: page.go("/supplier-electricity"),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                            text_style=ft.TextStyle(size=60)
                        )
                    )
                ],
                spacing=30,
                alignment="center"
            )
        ],
        horizontal_alignment="center",
        vertical_alignment="center"
    )
