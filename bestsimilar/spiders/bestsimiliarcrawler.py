from re import findall

from bestsimilar.spiders.constants import (
    MOVIE_HREF_QUERY,
    MOVIE_PLOTS_QUERY,
    MOVIE_TITLE_QUERY,
    MOVIES_CURRENT_PAGE_QUERY,
    PAGINATION_QUERY,
    TAG_HREF_QUERY,
    TAGS_QUERY,
)
from scrapy import Request, Spider

from ..items import BestSimilarItem


class BestSimilarSpider(Spider):
    name = "bestsimilar"
    start_urls = ["https://bestsimilar.com/tag"]
    tags_page_count = [1]
    movies_page_count = [1]

    def parse(self, response, **kwargs):
        pagination = response.css(PAGINATION_QUERY)

        self.handle_pagination(
            pagination, self.tags_page_count, response, self.parse
        )

        tags = response.css(TAGS_QUERY)

        for tag in tags:
            tag_href = tag.xpath(TAG_HREF_QUERY).get()

            yield Request(
                url=response.urljoin(tag_href),
                callback=self.handle_movies,
            )

    def handle_movies(self, response):
        pagination = response.css(PAGINATION_QUERY)

        self.handle_pagination(
            pagination, self.movies_page_count, response, self.handle_movies
        )

        movies_current_page = response.css(MOVIES_CURRENT_PAGE_QUERY)

        for movie in movies_current_page:
            movie_href = movie.xpath(MOVIE_HREF_QUERY).get()

            yield Request(
                url=response.urljoin(movie_href), callback=self.parse_movie
            )

    def handle_pagination(
        self, pagination_element, page_count: list, response, callback
    ):
        for page in pagination_element:
            page_href = page.xpath("a/@href").get()
            page_number = page.xpath("a/text()").get()
            page_class = page.xpath("@class").get()

            if page_class is None or "disabled" not in page_class:
                if (
                    page_number
                    and page_number.isnumeric()
                    and int(page_number) not in page_count
                ):
                    page_count.append(int(page_number))

                    yield Request(
                        url=response.urljoin(page_href),
                        callback=callback,
                    )

    def parse_movie(self, movie_current_page):
        movie_tags = (
            movie_current_page.css(MOVIE_PLOTS_QUERY[0])
            .xpath(MOVIE_PLOTS_QUERY[1])
            .xpath(MOVIE_PLOTS_QUERY[2])
            .xpath(MOVIE_PLOTS_QUERY[3])
            .xpath(MOVIE_PLOTS_QUERY[4])
            .get()
        ).strip()

        movie_title = (
            movie_current_page.css(MOVIE_TITLE_QUERY[0])
            .xpath(MOVIE_TITLE_QUERY[1])
            .get()
            .strip()
        )

        normalized_movie_title = self.normalize_title(movie_title)
        normalized_movie_year = self.normalize_year(movie_title)
        normalized_movie_tags = self.normalize_tags(movie_tags)

        movie = BestSimilarItem(
            **dict(
                title=normalized_movie_title,
                tags=normalized_movie_tags,
                year=normalized_movie_year,
            )
        )

        return movie

    @staticmethod
    def normalize_tags(movie_tags) -> list:
        normalized: list = movie_tags.split(", ")
        normalized[-1] = normalized[-1].replace("...", "").strip()

        return normalized

    @staticmethod
    def normalize_title(title):
        normalized: list = title.split(" ")
        normalized.pop()

        return "".join(normalized)

    @staticmethod
    def normalize_year(title) -> str:
        year: str = findall("\((.*?)\)", title)[-1]  # noqa

        return year if year else ""
