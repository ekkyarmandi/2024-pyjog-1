import scrapy
from itemloaders.processors import MapCompose
from scraper.items import PropertyItem
from scraper.func import find_published_date, are_to_sqm, dimension_remover
from scrapy.loader import ItemLoader
from datetime import datetime


class PropertiabaliSpider(scrapy.Spider):
    name = "propertiabali"
    allowed_domains = ["propertiabali.com"]
    start_urls = ["https://propertiabali.com/bali-villas-for-sale/"]

    def parse(self, response):

        # get all listings url
        urls = response.css("#module_properties a[href]::attr(href)").getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)

        # find next page urls
        next_page_url = response.css(
            "ul.pagination li > a[aria-label=Next]::attr(href)"
        ).get()
        if next_page_url:
            yield scrapy.Request(
                url=response.urljoin(next_page_url), callback=self.parse
            )

    def parse_detail(self, response):
        now = datetime.now().strftime(r"%Y-%m-%d")
        loader = ItemLoader(item=PropertyItem(), selector=response)
        loader.add_value("url", response.url)
        loader.add_value("source", "Propertia Bali")
        loader.add_value("created_at", now)
        loader.add_css(
            "listed_date",
            "script[type='application/ld+json']",
            MapCompose(find_published_date),
        )

        # find labels and property availability
        labels = loader.selector.css(
            "div.wpl_prp_gallery div.wpl-listing-tags-cnt div.wpl-listing-tag::text"
        ).getall()
        if len(labels) == 0:
            labels = ["Available"]
        loader.add_value("availability", labels)

        loader.add_css(
            "title",
            "h1::text",
        )
        loader.add_css(
            "location",
            "div.detail-wrap > ul > li:contains('Area') span::Text",
        )
        loader.add_css(
            "leasehold_years",
            "ul.fave_number-of-years ::Text",
        )
        loader.add_css(
            "contract_type",
            "div.detail-wrap > ul > li:contains('Property Type') span::Text",
        )
        loader.add_css(
            "bedrooms",
            "div.detail-wrap > ul > li:contains('Bedroom') span::Text",
        )
        loader.add_css(
            "bathrooms",
            "div.detail-wrap > ul > li:contains('Bathroom') span::Text",
        )
        loader.add_css(
            "land_size",
            "div.detail-wrap > ul > li:contains('Land Size') span::Text",
            MapCompose(are_to_sqm),
        )
        loader.add_css(
            "build_size",
            "div.detail-wrap > ul > li:contains('Building Size') span::Text",
            MapCompose(are_to_sqm),
        )
        loader.add_css(
            "price",
            "div.detail-wrap > ul > li:contains('Price') span::Text",
        )
        loader.add_css(
            "image_url",
            "div.property-banner img::attr(src)",
            MapCompose(dimension_remover),
        )
        loader.add_css(
            "description",
            "#property-description-wrap div.block-content-wrap p ::Text",
        )

        item = loader.load_item()
        if item.get("title"):
            yield item
