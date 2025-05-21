"""
Module for displaying a confirmation dialog to reset user data
"""
import flet as ft
from src.storage import clear_file

# @generated (partially) ChatGPT 4o
def reset_view(page: ft.Page):
    """
    Builds a modal overlay view that asks the user for confirmation to reset data
    """
    def on_confirm(e):
        clear_file("data/graph_data.json")
        clear_file("data/calculate_data.json")
        clear_file("data/supplier_data.json")
        e.page.go("/supplier-electricity")
    return ft.View(
        route="/confirm-reset",
        controls=[
            ft.Stack(
                controls=[
                    ft.Container(
                        bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
                        expand=True
                    ),
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Container(
                            width=420,
                            padding=25,
                            border_radius=10,
                            bgcolor=ft.colors.WHITE,
                            content=ft.Column(
                                horizontal_alignment="center",
                                controls=[
                                    ft.Text("Opravdu chcete začít znovu?", size=22, weight="bold"),
                                    ft.Text("⛔Vaše aktuální údaje budou ztraceny.", size=17),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.FilledButton("Ano", on_click=on_confirm,
                                                            style=ft.ButtonStyle(
                                                                bgcolor="#00796B",
                                                                color=ft.colors.WHITE
                                                            )),
                                            ft.OutlinedButton("Ne", on_click=lambda _: page.go("/result"),
                                                              style=ft.ButtonStyle(
                                                                  bgcolor="#00796B",
                                                                  color=ft.colors.WHITE
                                                              ))
                                        ],
                                    )
                                ],
                                spacing=20
                            )
                        )
                    )
                ]
            )
        ]
    )
