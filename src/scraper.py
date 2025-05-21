"""
Scraper module for fetching electricity tariff data from external sources.
Functions rely on BeautifulSoup for HTML parsing and are tailored
to specific structure of the Ušetřeno.cz pricing tables.
"""

from bs4 import BeautifulSoup
import requests
from src.errors import InternalError


def scrape_supplier(supplier_link_text: str, url: str="https://www.usetreno.cz/energie-elektrina/cena-elektriny/"):
    """
    Scrapes electricity tariff data for a specific supplier from the given webpage.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise InternalError("⚠️Error while loading data from the server") from e

    soup = BeautifulSoup(response.text, 'lxml')
    rows = soup.find_all('tr', class_='MuiTableRow-root mui-1f7cxp9')
    results = []

    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 4:
            continue

        link_elem = cells[1].find('a')
        if not link_elem:
            continue

        link_text = link_elem.get_text(strip=True)
        if supplier_link_text not in link_text:
            continue

        tariff_tag = cells[1].find('p', class_='MuiTypography-root MuiTypography-body2 mui-i5he6i')
        if not tariff_tag:
            continue

        price_elem_1 = cells[2].find('b')
        if not price_elem_1:
            continue

        price_elem_2 = cells[3].find('b')
        if not price_elem_2:
            continue

        result={
            "tariff_name": tariff_tag.get_text(strip=True),
            "price_kwh": price_elem_1.get_text(strip=True),
            "price_month": price_elem_2.get_text(strip=True)
        }
        results.append(result)

    if not results:
        raise InternalError("⚠️No matching tariffs found")

    return results


def extract_price(table, distributor: str):
    """
    Extracts the distribution price for a given distributor from the provided HTML table.
    """
    for row in table.find('tbody').find_all('tr'):
        cols = [col.get_text(strip=True) for col in row.find_all('td')]
        if cols and distributor in cols[0]:
            if len(cols)==3:
                result=''.join(cols[2].split()[:2])
                return result
    return None


def scrape_distributor(rate:str, distributor:str, url: str="https://www.usetreno.cz/regulovane-ceny-elektriny-2023/"):
    """
    Scrapes high and low distribution prices for a given tariff and distributor.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise InternalError("⚠️Error while loading data from the server") from e

    soup = BeautifulSoup(response.text, 'lxml')
    headers=soup.find_all(
        lambda tag: tag.name == 'h3' and rate in tag.text and 'Cena za distribuci' in tag.text
    )

    result=[]
    if len(headers)==2:
        table_high=headers[0].find_next('table')
        price_high=extract_price(table_high, distributor)
        table_low=headers[1].find_next('table')
        price_low=extract_price(table_low, distributor)
        if price_high and price_low:
            result=[price_high, price_low]
    elif len(headers)==1:
        table_high=headers[0].find_next('table')
        price_high=extract_price(table_high, distributor)
        if price_high:
            result=[price_high, '0']
    if not result:
        raise InternalError("⚠️No matching tariffs found")
    return result


def scrape_breaker(rate:str, distributor:str, breaker:str, url:str="https://www.usetreno.cz/regulovane-ceny-elektriny-2023/"):
    """
    Scrapes the monthly fee for a given breaker based on tariff and distributor.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise InternalError("⚠️Error while loading data from the server") from e

    soup = BeautifulSoup(response.text, 'lxml')
    headers = soup.find(
        lambda tag: tag.name == 'h3' and rate in tag.text and 'jistič' in tag.text
    )

    table=headers.find_next('table')
    column=0
    for head in table.find('thead').find_all('th'):
        if distributor in head.text:
            break
        column+=1

    for row in table.find('tbody').find_all('tr'):
        cols = [col.get_text(strip=True) for col in row.find_all('td')]
        if cols and breaker in cols[0]:
            return cols[column].split()[0]
    return None
