import scrapy
from scrapy.loader import ItemLoader
from scraper.items import PropertyItem
from datetime import datetime

from itemloaders.processors import MapCompose
from scraper.func import (
    are_to_sqm,
    dimension_remover,
    find_published_date,
)


class PropertiaBaliSpider(scrapy.Spider):
    name = "propertiabali"
    allowed_domains = ["propertiabali.com"]
    start_urls = ["https://propertiabali.com/bali-villas-for-sale"]

    def parse(self, response):
        # get properties urls
        urls = response.css("#module_properties a[target]::attr(href)").getall()

        # loop and parse it to parse_detail
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)

        # get the next page url
        # next_url = response.css(
        #     "ul.pagination li > a[aria-label=Next]::attr(href)"
        # ).get()
        # if next_url:
        #     yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse)

    def parse_test(self, response):
        title = response.css("div.page-title h1::Text").get()
        price_currency = response.css("ul li.item-price::Text").get()
        if len(price_currency) > 3:
            currency = price_currency[:3]
            price = price_currency[3:]
        yield dict(
            url=response.url,
            title=title,
            currency=currency,
            price=price,
        )

    def parse_detail(self, response):
        loader = ItemLoader(item=PropertyItem(), selector=response)

        # values
        loader.add_value("url", response.url)
        loader.add_value("source", "Propertia Bali")
        loader.add_value("scraped_at", datetime.now().strftime(f"%Y-%m-%d %H:%M:%S"))

        # from website

        loader.add_css("title", "h1::Text")
        # loader.add_css(
        #     "list_date",
        #     "script[type='application/ld+json']",
        #     MapCompose(find_published_date),
        # )
        # loader.add_css(
        #     "location",
        #     "div.detail-wrap > ul > li:contains('Area') span::Text",
        # )
        # loader.add_css(
        #     "leasehold_years",
        #     "ul.fave_number-of-years ::Text",
        # )
        # loader.add_css(
        #     "contract_type",
        #     "div.detail-wrap > ul > li:contains('Property Type') span::Text",
        # )
        # loader.add_css(
        #     "bedrooms",
        #     "div.detail-wrap > ul > li:contains('Bedroom') span::Text",
        # )
        # loader.add_css(
        #     "bathrooms",
        #     "div.detail-wrap > ul > li:contains('Bathroom') span::Text",
        # )
        # loader.add_css(
        #     "land_size",
        #     "div.detail-wrap > ul > li:contains('Land Size') span::Text",
        #     MapCompose(are_to_sqm),
        # )
        # loader.add_css(
        #     "build_size",
        #     "div.detail-wrap > ul > li:contains('Building Size') span::Text",
        #     MapCompose(are_to_sqm),
        # )
        # loader.add_css(
        #     "price",
        #     "div.detail-wrap > ul > li:contains('Price') span::Text",
        # )
        # loader.add_value("currency", "IDR")
        # loader.add_css(
        #     "image_url",
        #     "div.property-banner img::attr(src)",
        #     MapCompose(dimension_remover),
        # )

        # badges = loader.selector.css(
        #     "div.wpl_prp_gallery div.wpl-listing-tags-cnt div.wpl-listing-tag::text"
        # ).getall()
        # loader.add_value("availability", badges)
        # loader.add_css(
        #     "description",
        #     "#property-description-wrap div.block-content-wrap p ::Text",
        # )

        item = loader.load_item()
        # if not item.get("title"):
        # yield item

        yield item
