from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
import re


def get_search():
    search_text = input("შეიყვანე საძიებო სიტყვა:")
    clean_search = search_text.replace(" ", "+")
    return clean_search


def get_title(el):
    return el.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).text


def get_price(el):
    element = el.find("a", {"class": "a-size-base a-link-normal a-text-normal"})
    if element:
        price = element.find("span", {"class": "a-offscreen"}).text
        clean_price = float(re.sub("(\$|,)", "", price))
        return clean_price
    return "Unknown"


def get_rate(el):
    section = el.find("div", {"class": "a-section a-spacing-none a-spacing-top-micro"})
    if section:
        rate = section.find("span", {"class": "a-size-base"})
        if rate:
            return rate.text
    return "Unknown"


def get_next_page(driver):
    pagination = driver.find_element_by_class_name("a-pagination")
    next_page = pagination.find_element_by_class_name("a-last")
    return next_page.click()


def get_soup_list(driver):
    soup = content = driver.page_source

    soup = BeautifulSoup(content, "html.parser")
    soups = soup.find_all(
        "div",
        {
            "class": "s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16"
        },
    )
    return soups


def export_data(titles: list, prices: list, rates: list, file_name: str):
    df = pd.DataFrame({"title": titles, "price": prices, "rate": rates})
    df.to_csv(f"{file_name}.csv")


driver = webdriver.Chrome()

print("ბრაუზერი გაიხსნა")
search = get_search()
driver.get(f"https://www.amazon.com/s?k={search}")
print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
print("///////////////////////////////ძებნა დაიწყო\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
print("/////////////////////////////////////////////////////////////////////////")

soup_list = get_soup_list(driver)

titles = []
prices = []
rates = []

count = 0
item_num = 0
for page in range(5):
    for el in soup_list:
        print(f"----------------ITEM -{item_num}----------------")
        item_num += 1

        title = get_title(el)
        titles.append(title)
        price = get_price(el)
        prices.append(price)
        rate = get_rate(el)
        rates.append(rate)

        print(title)
        print(price)
        print(rate)
        print("------------------------------------------------")
        count += 1
        if count == 15:
            count = 1
            get_next_page(driver)
            sleep(10)
            soup_list = get_soup_list(driver)


export_data(titles, prices, rates, search)
