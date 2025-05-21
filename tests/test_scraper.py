"""
Tests for the scraper module used to fetch electricity tariff data.
"""

from unittest.mock import patch, MagicMock
import pytest
from bs4 import BeautifulSoup
import requests
from src.errors import InternalError
from src.scraper import scrape_supplier, extract_price, scrape_distributor, scrape_breaker

# @generated Claude.ai mock HTML contents
#Mock HTML content for supplier tests
MOCK_SUPPLIER_HTML = """
<table>
  <tr class="MuiTableRow-root mui-1f7cxp9">
    <td>1</td>
    <td>
      <a href="#">Test Supplier</a>
      <p class="MuiTypography-root MuiTypography-body2 mui-i5he6i">Standard Tariff</p>
    </td>
    <td><b>5.50 Kč/kWh</b></td>
    <td><b>150 Kč/měsíc</b></td>
  </tr>
  <tr class="MuiTableRow-root mui-1f7cxp9">
    <td>2</td>
    <td>
      <a href="#">Other Supplier</a>
      <p class="MuiTypography-root MuiTypography-body2 mui-i5he6i">Economy Tariff</p>
    </td>
    <td><b>4.80 Kč/kWh</b></td>
    <td><b>120 Kč/měsíc</b></td>
  </tr>
</table>
"""

#Mock HTML content for distributor tests
MOCK_DISTRIBUTOR_HTML = """
<h3>D02d Cena za distribuci vysoký tarif</h3>
<table>
  <thead>
    <tr><th>Distributor</th><th>Price</th><th>Value</th></tr>
  </thead>
  <tbody>
    <tr><td>ČEZ Distribuce</td><td>Value</td><td>2.00 Kč/kWh</td></tr>
    <tr><td>PRE Distribuce</td><td>Value</td><td>2.30 Kč/kWh</td></tr>
  </tbody>
</table>
<h3>D02d Cena za distribuci nízký tarif</h3>
<table>
  <thead>
    <tr><th>Distributor</th><th>Price</th><th>Value</th></tr>
  </thead>
  <tbody>
    <tr><td>ČEZ Distribuce</td><td>Value</td><td>1.00 Kč/kWh</td></tr>
    <tr><td>PRE Distribuce</td><td>Value</td><td>1.20 Kč/kWh</td></tr>
  </tbody>
</table>
"""

#Mock HTML content for breaker tests
MOCK_BREAKER_HTML = """
<h3>D02d hodnota jistič</h3>
<table>
  <thead>
    <tr><th>Jistič</th><th>ČEZ Distribuce</th><th>PRE Distribuce</th></tr>
  </thead>
  <tbody>
    <tr><td>3x25A</td><td>100 Kč/měsíc</td><td>110 Kč/měsíc</td></tr>
    <tr><td>3x32A</td><td>130 Kč/měsíc</td><td>140 Kč/měsíc</td></tr>
  </tbody>
</table>
"""

def test_scrape_supplier_success():
    """Test successful scraping of supplier tariff data."""
    with patch('requests.get') as mock_get:
        mock_response=MagicMock()
        mock_response.text=MOCK_SUPPLIER_HTML
        mock_response.raise_for_status=MagicMock()
        mock_get.return_value=mock_response

        result=scrape_supplier("Test Supplier")

        assert len(result)==1
        assert result[0]["tariff_name"]=="Standard Tariff"
        assert result[0]["price_kwh"]=="5.50 Kč/kWh"
        assert result[0]["price_month"]=="150 Kč/měsíc"


def test_scrape_supplier_no_match():
    """Test scraping when no matching supplier is found."""
    with patch('requests.get') as mock_get:
        mock_response=MagicMock()
        mock_response.text=MOCK_SUPPLIER_HTML
        mock_response.raise_for_status=MagicMock()
        mock_get.return_value=mock_response

        with pytest.raises(InternalError, match="⚠️No matching tariffs found"):
            scrape_supplier("Nonexistent Supplier")


def test_scrape_supplier_request_error():
    """Test handling of request errors during supplier scraping."""
    with patch('requests.get') as mock_get:
        mock_get.side_effect=requests.RequestException("Connection error")

        with pytest.raises(InternalError, match="⚠️Error while loading data from the server"):
            scrape_supplier("Test Supplier")


def test_extract_price():
    """Test extraction of price from a table for a specific distributor."""
    soup=BeautifulSoup(MOCK_DISTRIBUTOR_HTML, 'lxml')
    table=soup.find('table')

    price=extract_price(table, "ČEZ Distribuce")
    assert price=="2.00Kč/kWh"

    price=extract_price(table, "PRE Distribuce")
    assert price=="2.30Kč/kWh"

    price=extract_price(table, "Nonexistent Distributor")
    assert price is None


def test_scrape_distributor_dual_tariff():
    """Test scraping of distributor data with both high and low tariffs."""
    with patch('requests.get') as mock_get:
        mock_response=MagicMock()
        mock_response.text=MOCK_DISTRIBUTOR_HTML
        mock_response.raise_for_status=MagicMock()
        mock_get.return_value=mock_response

        result=scrape_distributor("D02d", "ČEZ Distribuce")

        assert len(result) == 2
        assert result[0]=="2.00Kč/kWh"
        assert result[1]=="1.00Kč/kWh"


def test_scrape_distributor_no_match():
    """Test scraping distributor data when no matching rate is found."""
    with patch('requests.get') as mock_get:
        mock_response=MagicMock()
        mock_response.text = "<html></html>"
        mock_response.raise_for_status=MagicMock()
        mock_get.return_value=mock_response

        with pytest.raises(InternalError, match="⚠️No matching tariffs found"):
            scrape_distributor("D01d", "ČEZ Distribuce")


def test_scrape_distributor_request_error():
    """Test handling of request errors during distributor scraping."""
    with patch('requests.get') as mock_get:
        mock_get.side_effect=requests.RequestException("Connection error")

        with pytest.raises(InternalError, match="⚠️Error while loading data from the server"):
            scrape_distributor("D02d", "ČEZ Distribuce")


def test_scrape_breaker_success():
    """Test successful scraping of breaker data."""
    with patch('requests.get') as mock_get:
        mock_response=MagicMock()
        mock_response.text=MOCK_BREAKER_HTML
        mock_response.raise_for_status=MagicMock()
        mock_get.return_value=mock_response

        result=scrape_breaker("D02d", "ČEZ Distribuce", "3x25A")

        assert result=="100"


def test_scrape_breaker_no_match():
    """Test scraping breaker data when no matching breaker is found."""
    with patch('requests.get') as mock_get:
        mock_response=MagicMock()
        mock_response.text=MOCK_BREAKER_HTML
        mock_response.raise_for_status=MagicMock()
        mock_get.return_value=mock_response

        result=scrape_breaker("D02d", "ČEZ Distribuce", "3x40A")

        assert result is None


def test_scrape_breaker_request_error():
    """Test handling of request errors during breaker scraping."""
    with patch('requests.get') as mock_get:
        mock_get.side_effect=requests.RequestException("Connection error")

        with pytest.raises(InternalError, match="⚠️Error while loading data from the server"):
            scrape_breaker("D02d", "ČEZ Distribuce", "3x25A")


# Integration-style test with a more complex HTML mock
def test_integration_with_complex_html():
    """Test scraping with more complex HTML structure."""
    # @generated Claude.ai
    complex_html = """
    <html>
      <body>
        <table>
          <tr class="MuiTableRow-root mui-1f7cxp9">
            <td>1</td>
            <td>
              <a href="#">Complex Supplier</a>
              <p class="MuiTypography-root MuiTypography-body2 mui-i5he6i">Premium Tariff</p>
            </td>
            <td><b>6.25 Kč/kWh</b></td>
            <td><b>180 Kč/měsíc</b></td>
          </tr>
          <tr class="MuiTableRow-root mui-1f7cxp9">
            <td>2</td>
            <td>
              <a href="#">Complex Supplier</a>
              <p class="MuiTypography-root MuiTypography-body2 mui-i5he6i">Basic Tariff</p>
            </td>
            <td><b>4.15 Kč/kWh</b></td>
            <td><b>120 Kč/měsíc</b></td>
          </tr>
        </table>
      </body>
    </html>
    """

    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.text = complex_html
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = scrape_supplier("Complex Supplier")

        assert len(result) == 2
        assert result[0]["tariff_name"] == "Premium Tariff"
        assert result[0]["price_kwh"] == "6.25 Kč/kWh"
        assert result[0]["price_month"] == "180 Kč/měsíc"
        assert result[1]["tariff_name"] == "Basic Tariff"
        assert result[1]["price_kwh"] == "4.15 Kč/kWh"
        assert result[1]["price_month"] == "120 Kč/měsíc"
