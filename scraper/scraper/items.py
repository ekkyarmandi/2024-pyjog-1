# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from scraper.func import to_number, AnySold, JoinAndStrip


class PropertyItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    source = scrapy.Field(output_processor=TakeFirst())
    scraped_at = scrapy.Field(output_processor=TakeFirst())
    # list_date = scrapy.Field(
    #     input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    # )
    title = scrapy.Field(
        input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    )
    # location = scrapy.Field(
    #     input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    # )
    # contract_type = scrapy.Field(
    #     input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    # )
    # leasehold_years = scrapy.Field(
    #     input_processor=MapCompose(to_number), output_processor=TakeFirst()
    # )
    # bedrooms = scrapy.Field(
    #     input_processor=MapCompose(to_number), output_processor=TakeFirst()
    # )
    # bathrooms = scrapy.Field(
    #     input_processor=MapCompose(to_number), output_processor=TakeFirst()
    # )
    # land_size = scrapy.Field(
    #     input_processor=MapCompose(to_number), output_processor=TakeFirst()
    # )
    # build_size = scrapy.Field(
    #     input_processor=MapCompose(to_number), output_processor=TakeFirst()
    # )
    # price = scrapy.Field(
    #     input_processor=MapCompose(to_number), output_processor=TakeFirst()
    # )
    # currency = scrapy.Field(
    #     input_processor=MapCompose(to_number), output_processor=TakeFirst()
    # )
    # image_url = scrapy.Field(
    #     input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    # )
    # availability = scrapy.Field(
    #     input_processor=MapCompose(str.strip), output_processor=AnySold()
    # )
    # is_off_plan = scrapy.Field(
    #     input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    # )
    # description = scrapy.Field(
    #     input_processor=MapCompose(str.strip), output_processor=JoinAndStrip()
    # )
