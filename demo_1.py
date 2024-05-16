import requests
import re
from bs4 import BeautifulSoup

# functions
def get_price(value):
    numbers = "".join(re.findall(r"\d+", value))
    return int(numbers)


# deklarasi url dan headers
url = "https://propertiabali.com/property/stunning-industrial-villa-in-pererenan"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

# melakukan HTTP GET requests
respond = requests.get(url, headers=headers)

# mengubah respond menjadi BeautifulSoup object
if respond.status_code == 200:
    soup = BeautifulSoup(respond.text, "html.parser")

    # mengekstrak data yang diinginkan
    title = soup.find("h1").text
    price = soup.select_one("ul.item-price-wrap li").text

    # menyimpan data sebagai csv menggunakan pandas
    property = {
        "title": title,
        "price": get_price(price),
    }

    # print type data dari property
    for key, value in property.items():
        print(key, type(value))

print("done")
