from itemloaders.processors import TakeFirst, Join
from datetime import datetime
import re


class AnySold(TakeFirst):
    def __call__(self, values):
        is_sold = lambda f: "sold" in f.lower()
        any_sold = any(list(map(is_sold, values)))
        if any_sold:
            return "Sold"
        return "Available"


class JoinAndStrip(Join):
    def __call__(self, values):
        values = list(map(str.strip, values))
        values = list(filter(lambda v: v != "", values))
        return self.separator.join(values)


def to_number(value):
    if type(value) == str:
        value = re.sub(",", "", value)
        result = re.findall(r"[0-9.]+", value)
        dots = len(re.findall(r"\.", value))
        if len(result) > 0:
            result = "".join(result)
            dec = len(result.split(".")[-1]) if dots == 1 else 0
            if dots > 1 or dec > 2:
                result = result.replace(".", "")
            return eval(result)
        else:
            return ""
    return value


def find_published_date(script):
    result = re.search(r'"datePublished":"(?P<date>[T0-9\-\:\+]+)"', script)
    if result:
        date = result.group("date")
        return datetime.fromisoformat(date).strftime("%m/%d/%y")
    return ""


def dimension_remover(src):
    patterns = [
        r"(-\d+x\d+)\.jpg",
        r"(-\d+x\d+)\.jpeg",
        r"(-\d+x\d+)\.png",
        r"(-\d+x\d+)\.webp",
    ]
    result = re.search("|".join(patterns), src)
    if result:
        for i in range(1, 4):
            dim = result.group(i)
            if dim:
                src = src.replace(dim, "")
    return src


def safe_number(value):
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return None  # Invalid input

    if isinstance(value, (int, float)):
        try:
            if value.is_integer():
                return int(value)
            else:
                rounded = round(value, 2)
                return rounded
        except AttributeError:
            return value
    else:
        return None  # Invalid input


def are_to_sqm(value):
    def asnumber(text):
        digits = re.findall(r"[0-9.]+", text)
        value = next(d for d in digits)
        return eval(value)

    if type(value) == str:
        if "are" in value.lower():
            value = asnumber(value) * 100
            return safe_number(value)
        else:
            return to_number(value)
    return value
