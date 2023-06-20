import scrapy


class ScraperSpider(scrapy.Spider):
    name = 'scraper'
    allowed_domains = ['clutch.co']
    start_urls = ['https://clutch.co/agencies/creative']

    def parse(self, response):
        all_urls = response.xpath("//a[@class='company_title']/@href").getall()
        for url in all_urls:
            # print(url)
            # print(all_urls.index(url))
            yield response.follow(url=url, callback=self.parse_suburl)

        next_url = response.xpath("//li[@class='page-item next']/a/@href").get()
        if next_url:
            yield response.follow(url=next_url, callback=self.parse)

    def parse_suburl(self, response):
        # pass
        try:
            name = response.xpath("//h1/a[@class='website-link__item']/text()").get()
            name = name.strip()
        except Exception as e:
            print(e)
            name = ' '
        print(f"Name: {name}")
        try:
            rating = response.xpath("//span[@itemprop='ratingValue']/text()").get()
            rating = rating.strip()
        except Exception as e:
            print(e)
            rating = ' '
        print(f"Rating: {rating}")
        try:
            reviews = response.xpath("//span[@itemprop='reviewCount']/text()").get()
            print(f"Reviews: {reviews}")
        except Exception as e:
            print(e)
            reviews = ' '
        try:
            project_size = response.xpath("//div[@data-content='<i>Min. project size</i>']//span/text()").get()
            print(f"Project Size: {project_size}")
        except Exception as e:
            print(e)
            project_size = ' '
        try:
            location = response.xpath("//div[@class='field-location-name']/span/text()").get()
            location = location.strip()
        except Exception as e:
            print(e)
            location = ' '
        print(f"Location: {location}")

        yield {
            "Name": name,
            "Location": location,
            "Rating": rating,
            "Reviews": reviews,
            "Project Size": project_size
        }