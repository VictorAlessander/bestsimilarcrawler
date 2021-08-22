from scrapy import Spider, Request
from scrapy_splash import SplashRequest


class BestSimilarCrawler(Spider):
    name = "bestsimilarspider"
    start_urls = ["https://bestsimilar.com/movies"]
    pages = [1]
    # script = """
    #     while (!document.getElementsByClassName("btn btn-act btn-lg").length == 0) {
    #         moreTagMovieList()

    #         await new Promise(r => setTimeout(r, 3000));
    #     }
    # """

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(
    #             url,
    #             self.parse,
    #             endpoint="render.html",
    #             args=dict(wait=1, js_source=self.script),
    #         )

    def parse(self, response, **kwargs):
        pagination = response.css("ul.pagination.pagination-lg > li")

        for page in pagination:
            page_href = page.xpath("a/@href").get()
            page_number = page.xpath("a/text()").get()
            if page_number and int(page_number) not in self.pages:
                self.pages.append(int(page_number))

                yield Request(
                    url=response.request.urljoin(page_href),
                    callback=self.parse,
                )

        movies = response.css(
            "div.items.row.equal.img-grid.block-ins.block-ins-tag-s1 > div"
        )

        for movie in movies:
            movie_href = movie.xpath(
                "div/div[@class='block-ins-caption']/a/@href"
            ).get()

            yield Request(
                url=response.request.urljoin(movie_href),
                callback=self.parse_movie,
            )

    def parse_movie(self, response, **kwargs):
        movie_content = response.css("div.item.item-big.clearfix")
