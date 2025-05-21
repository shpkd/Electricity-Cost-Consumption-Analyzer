# 💡Electricity Cost & Consumption Analyzer

This project is a desktop application that helps Czech households analyze their electricity consumption and costs. By combining user input with real-time tariff data scraped from supplier websites, the app calculates monthly expenses, compares them with actual payments, and visualizes overpayments or debts using interactive graphs. Built using Python with Flet for the GUI, BeautifulSoup for web scraping, and Plotly for visualization, the tool enables users to plan budgets more accurately and track trends over time. 

# 🔧Features

**User Input Integration:** Allows users to specify their region, electricity supplier, tariff type, breaker size, and monthly consumption.

**Automatic Tariff Retrieval:** Fetches up-to-date electricity and distribution tariffs based on user input from supplier websites (e.g., ušetřeno.cz).

**Temporary Data Storage:** Saves scraped and calculated data in JSON files for further use and graph generation; updates on every user input change.

**Cost Calculation:** Calculates monthly and estimated annual electricity costs using real pricing data.

**Payment Comparison:** Compares actual costs with user-defined monthly payments to identify overpayments or outstanding debts.

**Interactive Graphs:** Visualizes consumption trends, cost dynamics, and payment differences using Plotly.

# ✅Usage

Installing system dependencies

```
sudo apt install -y libmpv1
```

The project uses the **Flet Desktop** library to create a native window interface.  
Flet relies on the `libmpv` multimedia library under the hood to render the application window and UI.

Setting up virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```
Installing Python dependencies

```
pip install -r requirements.txt
``` 

Setup complete. To run the app

```
python3 -m gui.router
```

# 📂Project Structure
**``src/``**

Core logic of the application:

- ``calculate.py``: Handles all tariff and cost calculations.

- ``errors.py``: Custom error classes for exception handling.

- ``graph.py``: Generates graphs for visualizing electricity usage.

- ``scraper.py``: Fetches online tariff data from supplier websites.

- ``storage.py``: Loads and saves user consumption data in JSON format.

- ``utils.py``: Utility functions used across the application.

**``gui/``**

Graphical user interface:

- ``assets/logos/``: Supplier logos used in the UI.

- ``components/``: Reusable Flet UI components.

- ``views/:`` Page-specific UI views.

- ``router.py:`` Entry point for launching the application interface.

**``tests/``**

Unit tests for core functionality.

**``data/``**

Stores temporary JSON files used during program execution.

**``requirements.txt``**

List of Python dependencies required to run the project.

**``shpakdia.pdf``**

General report of the project.

**``README.md``**

Project documentation.
