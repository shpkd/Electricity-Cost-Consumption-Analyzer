"""
Module for drawing electricity cost graphs using Plotly
"""

import tempfile
import plotly.graph_objects as go
from src.storage import load_data
from src.errors import InternalError


def draw_graph(file, monthly_charge):
    """
    Draws a line graph comparing real monthly electricity costs
    to the user's monthly charge using Plotly, and returns the path
    to the temporary image file.
    """
    data=load_data(file)
    if not data:
        raise InternalError(f"⚠️ File '{file}' is empty")
    months = [entry["month"] for entry in data]
    costs = [entry["cost"] for entry in data]
    diffs = [entry["diff"] for entry in data]

    text = [f"{'+' if d >= 0 else ''}{d} Kč" for d in diffs]
    text_colors = ["green" if d >= 0 else "red" for d in diffs]

    fig=go.Figure()

    fig.add_trace(go.Scatter(
        x=months,
        y=costs,
        text=text,
        mode="lines+markers+text",
        name="Měsíční náklady",
        textposition="top center",
        textfont={"color": text_colors},
        line={"color": "black"}
    ))

    fig.add_trace(go.Scatter(
        x=months,
        y=[monthly_charge] * len(months),
        mode="lines",
        name=f"Poplatky {monthly_charge} Kč",
        line={"color": "red", "dash": "dash"}
    ))

    fig.update_layout(
        title={
            "text": "📈Graf vyúčtování",
            "font": {"size": 20},
            "xanchor": "left",
            "x": 0.1
        },
        xaxis_title="Měsíc",
        yaxis_title="Cena (Kč)",
        template="seaborn",
        width=1000,
        height=550
    )

    # @generated (partially) ChatGPT 4o
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        fig.write_image(tmp.name)
        return tmp.name
