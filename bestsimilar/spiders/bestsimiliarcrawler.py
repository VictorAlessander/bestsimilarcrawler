from scrapy import Spider, Request
from ..items import BestsimilarItem


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

    def parse(self, response, **kwargs):
        pagination = response.css("ul.pagination.pagination-lg > li")

        for page in pagination:
            page_href = page.xpath("a/@href").get()
            page_number = page.xpath("a/text()").get()
            page_class = page.xpath("@class").get()

            if page_class is None or "disabled" not in page_class:
                if (
                    page_number
                    and page_number.isnumeric()
                    and int(page_number) not in self.pages
                ):
                    self.pages.append(int(page_number))

                    yield Request(
                        url=response.urljoin(page_href),
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
                url=response.urljoin(movie_href),
                callback=self.parse_movie,
            )

    def parse_movie(self, response):
        movie_content = response.css("div.item.item-big.clearfix")
        movie_tags = response.css("div#best-tags > div > div > div")

        title = (
            movie_content.xpath("div/div")[0].xpath("div/span/text()").get()
        )

        tags = self.parse_movie_tags(movie_tags)

        movie = BestsimilarItem(**dict(title=title, **tags))

        return movie

    def parse_movie_tags(self, movie_tags_element):
        tags = list()

        for tag in movie_tags_element:
            tag_title = tag.xpath(
                "div/div[@class='block-ins-caption']/a/text()"
            ).get()
            tags.append(tag_title)

        return dict(tags=tags)
