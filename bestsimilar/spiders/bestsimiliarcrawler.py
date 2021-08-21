from scrapy import Spider
from scrapy_splash import SplashRequest


class BestSimilarCrawler(Spider):
    name = "bestsimilarspider"
    start_urls = ["https://bestsimilar.com/tag/21593-christmas-special"]
    script = """
        while (!document.getElementsByClassName("btn btn-act btn-lg").length == 0) {
            moreTagMovieList()

            await new Promise(r => setTimeout(r, 3000));
        }
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                self.parse,
                endpoint="render.html",
                args=dict(wait=1, js_source=self.script),
            )

    def parse(self, response, **kwargs):
        load_more_button = response.css("div.load-more-btn")
