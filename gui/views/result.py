"""
Module for building the result view of the electricity usage app.
Includes logic for initial data loading, user input handling,
calculations, and graphical display updates.
"""

import flet as ft
from data.constants import CZECH_MONTHS
from src.errors import ValidationError
from src.calculate import calculate_tariff, recalculation, yearly_recalculation, TariffConfig
from src.storage import load_data, save_data, save_data_append
from src.graph import draw_graph
from src.utils import get_month_range, count_months

def format_diff_label(diff, label=None):
    """
    Updates the label with formatted diff value or returns a new Text if label is None.
    """
    if diff >= 0:
        color = "green"
        prefix = "+"
    else:
        color = "red"
        prefix = ""
    value = f"{prefix}{round(diff, 2)} Kč"
    if label is not None:
        label.value = value
        label.color = color
        return label
    return ft.Text(value, color=color, size=20)

def create_tariff_config(data):
    """
    Creates and returns a TariffConfig object using provided input data
    """
    return TariffConfig(
        data["energy_price_per_kwh"],
        data["fixed_supplier_fee"],
        data["distribution_high_tariff"],
        data["distribution_low_tariff"],
        data["high_tariff_ratio"],
        data["breaker_fee"]
    )

def init_graph_data():
    """
    Loads configuration, calculates monthly and total diffs, and stores initial monthly values to graph data.
    """
    data = load_data("data/calculate_data.json")
    months_after = get_month_range(data["start"], data["end"] , CZECH_MONTHS, mark=2)
    months_before = get_month_range(data["end"], data["start"] , CZECH_MONTHS, mark=1)

    start = CZECH_MONTHS[data["end"] - 1]
    end = CZECH_MONTHS[data["start"] - 2]
    value = data["kwh_last"]
    count_before = count_months(data["end"], data["start"])

    config=create_tariff_config(data)
    cost = calculate_tariff(count_before, int(value), config)

    cost_per_month = cost / count_before
    diff_per_month = round(data["user_monthly_charge"] - cost_per_month, 2)
    diff = diff_per_month * count_before

    label = f"{start} - {end}: {value} kWH"
    diff_text = format_diff_label(diff)

    for m in months_before:
        month_number = CZECH_MONTHS.index(m)
        result = {
            "month": m,
            "month_number": month_number,
            "kwh": value,
            "diff": diff_per_month,
            "cost": round(cost_per_month, 2),
            "source": "initial"
        }
        save_data_append(result, "data/graph_data.json")
    return label, diff_text, [months_after]

def add_all_sources(display_column):
    """
    Adds a summary row to display_column for every unique user source
    """
    data = load_data("data/graph_data.json")
    user_sources = []
    for entry in data:
        source = entry.get("source")
        if source != "initial" and source not in user_sources:
            user_sources.append(source)

    for source in user_sources:
        filtered=[entry for entry in data if entry["source"] == source]
        if not filtered:
            continue
        total_cost = round(sum(entry["diff"] for entry in filtered), 2)
        first_month = filtered[0]["month"]
        last_month = filtered[-1]["month"]
        kwh = filtered[0]["kwh"]

        if first_month == last_month:
            label_text = f"{first_month}: {kwh} kWH"
        else:
            label_text = f"{first_month} - {last_month}: {kwh} kWH"

        month_label = ft.Text(label_text, size=20, width=250)
        diff_text = format_diff_label(total_cost)

        display_column.controls.append(ft.Row(controls=[month_label, diff_text], spacing=20))

def init_saved_data():
    """
    Initializes view data from previously saved entries in graph_data.json
    """
    data=load_data("data/graph_data.json")
    initial_entries = [entry for entry in data if entry.get("source") == "initial"]
    first_month = initial_entries[0]["month"]
    last_month = initial_entries[-1]["month"]
    value=initial_entries[0]["kwh"]

    label = f"{first_month} - {last_month}: {value} kWH"
    diff=round(sum(entry.get("diff", 0) for entry in initial_entries), 2)
    diff_text=format_diff_label(diff)

    months_after=get_month_range(data[-1]["month_number"]+2, data[0]["month_number"]+1 , CZECH_MONTHS, mark=2)
    return label, diff_text, [months_after]

def process_kwh_entry(config, entered_months, value, user_monthly_charge, user_index):
    """
    Process a single kWh entry and calculate the cost and difference.
    """
    cost = calculate_tariff(len(entered_months), int(value), config)
    cost_per_month = cost / len(entered_months)

    if entered_months[0]==entered_months[-1]:
        month_label = ft.Text(f"{entered_months[0]}: {value} kWH", size=20, width=250)
    else:
        month_label = ft.Text(f"{entered_months[0]} - {entered_months[-1]}: {value} kWH", size=20, width=250)

    diff = round(user_monthly_charge*len(entered_months) - cost, 2)
    diff_per_month=round(user_monthly_charge-cost_per_month, 2)
    diff_text_new = format_diff_label(diff)

    for m in entered_months:
        month_number = CZECH_MONTHS.index(m)
        result = {
            "month": m,
            "month_number": month_number,
            "kwh": value,
            "diff": diff_per_month,
            "cost": cost_per_month,
            "source": user_index
        }
        save_data_append(result, "data/graph_data.json")
    return month_label, diff_text_new

def result_view(page: ft.Page):
    """
    Builds and returns the result view for analyzing electricity usage.
    Loads previously entered data, calculates monthly and yearly cost differences,
    and constructs a user interface with a graph, consumption inputs, and recalculation summaries.
    """
    if load_data("data/graph_data.json"):
        label, diff_text, months_after = init_saved_data()
    else:
        label, diff_text, months_after= init_graph_data()

    data = load_data("data/calculate_data.json")

    kwh_textfield = ft.TextField(width=150)
    display_column = ft.Column(controls=[], spacing=5, horizontal_alignment="start")
    add_all_sources(display_column)
    graph_img = ft.Image(src=draw_graph("data/graph_data.json", data["user_monthly_charge"]))

    user_index = [0]
    actual_recalculation = format_diff_label(round(recalculation("data/graph_data.json"), 2))
    general_recalculation = format_diff_label(yearly_recalculation("data/graph_data.json"))
    from_month_label = ft.Text(f"{months_after[0][0]} - " if months_after[0] else "✅ -", size=20)
    error_text = ft.Text("", color=ft.colors.RED)
    month_dropdown = ft.Dropdown(options=[ft.dropdown.Option(text=m, key=m) for m in months_after[0]], width=150)

    def update_view():
        graph_img.src = draw_graph("data/graph_data.json", data["user_monthly_charge"])
        actual_recalculation.value = format_diff_label(round(recalculation("data/graph_data.json"), 2)).value
        general_recalculation.value = format_diff_label(yearly_recalculation("data/graph_data.json")).value
        month_dropdown.options = [ft.dropdown.Option(text=m, key=m) for m in months_after[0]]
        month_dropdown.value = ""
        from_month_label.value = f"{months_after[0][0]} - " if months_after[0] else "✅ -"
        month_dropdown.update()
        page.update()

    def add_data():
        """
        Handles the '+' button click.
        Adds a new monthly electricity entry: validates input, calculates cost,
        updates graph, recalculations and UI, saves the result.
        """
        try:
            value = kwh_textfield.value.strip()

            if not value:
                raise ValidationError("⛔Zadejte prosím")

            if not value.isdigit():
                raise ValidationError("⛔Zadejte prosím ve formátu čísla")

            if not months_after:
                raise ValidationError("⛔Všechny měsíce již byly zadány")

            config=create_tariff_config(data)

            selected_month=month_dropdown.value
            if not selected_month:
                raise ValidationError("⛔Vyberte měsíc ze seznamu")
            month_ind=months_after[0].index(selected_month)

            month_label, diff_text_new = process_kwh_entry(
                config, months_after[0][:month_ind+1], value, data["user_monthly_charge"], user_index[0]
            )

            months_after[0]=months_after[0][month_ind+1:]
            user_index[0] += 1
            kwh_textfield.value = ""
            error_text.value = ""

            display_column.controls.append(ft.Row(controls=[month_label, diff_text_new], spacing=20))
            update_view()
        except ValidationError as e:
            error_text.value=str(e)
            page.update()

    def delete_data():
        """
        Handles the '-' button click.
        Deletes the last user-added monthly electricity entry: updates graph, recalculations, and UI.
        """
        try:
            user_data = load_data("data/graph_data.json")

            last_source = user_data[-1]["source"]

            if last_source == "initial":
                raise ValidationError("⛔ Nelze odstranit počáteční záznamy")

            while user_data and user_data[-1]["source"] == last_source:
                user_data.pop()

            save_data(user_data, "data/graph_data.json")

            if display_column.controls:
                display_column.controls.pop()
            error_text.value = ""
            months_after[0] = get_month_range(user_data[-1]["month_number"] + 2, user_data[0]["month_number"] + 1, CZECH_MONTHS, mark=2)
            update_view()
        except ValidationError as e:
            error_text.value = str(e)
            page.update()

    return ft.View(
        route="/result",
        controls=[
            ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="🏠",
                                    width=60,
                                    height=60,
                                    on_click=lambda _: page.go("/confirm-reset"),
                                    bgcolor="#00796B"
                                ),
                                ft.Text("📊Analýza vyúčtování", size=30, weight="bold")
                            ],
                            spacing=10
                        ),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.Text(label, size=20),
                                                    diff_text
                                                ],
                                                spacing=20
                                            ),
                                            ft.Text("📆Zadejte hodnotu pro každý měsíc:", size=20),
                                            ft.Row([
                                                from_month_label,
                                                month_dropdown
                                            ]),
                                            ft.Row([
                                                kwh_textfield,
                                                ft.ElevatedButton(
                                                    text="+",
                                                    width=40,
                                                    height=40,
                                                    on_click=lambda _: add_data(),
                                                    bgcolor="green",
                                                    color="white"
                                                ),
                                                ft.ElevatedButton(
                                                    text="-",
                                                    width=40,
                                                    height=40,
                                                    on_click=lambda _: delete_data(),
                                                    bgcolor="red",
                                                    color="white"
                                                )
                                            ]),
                                            error_text,
                                            ft.Divider(),
                                            display_column,
                                            ft.Row(
                                                controls=[
                                                    ft.Text("✅Aktuální vyúčtování", size=24, weight="bold"),
                                                    actual_recalculation
                                                ],
                                                spacing=10
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Text("🔎Přibližné roční vyúčtování", size=25, weight="bold"),
                                                    general_recalculation
                                                ],
                                                spacing=10
                                            )
                                        ],
                                        spacing=10
                                    ),
                                    width=420,
                                    height=700
                                ),
                                ft.Container(
                                    content=graph_img,
                                    width=1000,
                                    height=700,
                                    alignment=ft.alignment.top_center
                                )
                            ],
                            spacing=150
                        )
                    ],
                    spacing=20
                )
            )
        ]
    )
