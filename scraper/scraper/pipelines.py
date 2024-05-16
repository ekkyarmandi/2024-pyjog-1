# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import uuid


class ScraperPipeline:

    def __init__(self):
        self.create_connection("database.db")
        self.create_table_if_not_exists()

    def create_connection(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

    def create_table_if_not_exists(self):
        query = """
        CREATE TABLE IF NOT EXISTS property (
            id TEXT PRIMARY KEY,
            url TEXT,
            source TEXT,
            created_at DATE,
            listed_date TEXT,
            title TEXT,
            location TEXT,
            contract_type TEXT,
            leasehold_years INTEGER,
            bedrooms INTEGER,
            bathrooms INTEGER,
            land_size INTEGER,
            build_size INTEGER,
            price INTEGER,
            image_url TEXT,
            availability BOOLEAN,
            description TEXT
        )"""
        self.cur.execute(query)
        self.con.commit()

    def to_values(self, item):
        property_id = "'{}'".format(uuid.uuid1())
        values = [property_id]
        for _, value in item.items():
            if type(value) == str:
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        return ",".join(values)

    def to_columns(self, item):
        keys = list(item.keys())
        keys.insert(0, "id")
        return ",".join(keys)

    def process_item(self, item, spider):
        columns = self.to_columns(item)
        values = self.to_values(item)
        query = f"""
        INSERT INTO property ({columns}) VALUES ({values});
        """
        self.cur.execute(query)
        self.con.commit()
        return item
