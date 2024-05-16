from requests_html import HTMLSession
import re

# functions
def get_price(value):
    numbers = "".join(re.findall(r"\d+", value))
    return int(numbers)

session = HTMLSession()

url = "https://propertiabali.com/property/stunning-industrial-villa-in-pererenan"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

res = session.get(url, headers=headers)

title = res.html.find("h1", first=True).text
price = res.html.find("ul.item-price-wrap li", first=True).text

property = {
    "title": title,
    "price": get_price(price),
}

print(property)
