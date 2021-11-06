import scrapy


class PatentSpider(scrapy.Spider):
    name = "patent"

    def start_requests(self):
        urls = ["https://www.fips.ru/registers-doc-view/fips_servlet?DB=RUPM&DocNumber={}&TypeFile=html".format(
            i) for i in range(7510, 7551)]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            "id": response.css("div#top4 a::text").get(),
            "pageUrl": response.request.url,
            "expirationColor": response.css("tr").xpath('@class').get(),
            "title": response.css("p#B542 b::text").get(),
            "context": response.css("div#Abs > p ~ p::text").get(),
            "imgUrl": "https://www.fips.ru" + response.css("a img::attr(src)").get()
        }
