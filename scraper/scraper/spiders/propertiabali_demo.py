import scrapy


class PropertiabaliDemoSpider(scrapy.Spider):
    name = "propertiabali_demo"
    allowed_domains = ["propertiabali.com"]
    start_urls = ["https://propertiabali.com/bali-villas-for-sale"]

    def parse(self, response):
        
        # find all property urls
        urls = response.css('h2 a[href]::attr(href)').getall()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_detail)

        # find next url
        next_page = response.css("a[aria-label=Next]::attr(href)").get()
        if next_page != response.url:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        property = dict(
                title=response.css("h1::Text").get(),
                price=response.css('ul.item-price-wrap li::Text').get(),
        )
        yield property
