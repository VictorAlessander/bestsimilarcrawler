# CSS/XPATH QUERIES

MOVIE_PLOTS_QUERY = [
    "div.block-main.block-main-first > div.item-c > div.item.item-big.clearfix > div.is-row.clearfix",
    "div[@class='col-md-10 col-sm-10 col-ms-9 col-xs-12']",
    "div/div/div[@class='col-lg-12 col-md-12 col-sm-12 col-xs-12 column-content']",
    "div/div[@class='attr attr-tag attr-tag-group-1']",
    "span[@class='value']/text()",
]
MOVIES_CURRENT_PAGE_QUERY = "div#tag-movie-list > div"
MOVIE_HREF_QUERY = "div/div/div[@class='name-c']/a/@href"
MOVIE_TITLE_QUERY = [
    "div.block-main.block-main-first > div.item-c > div.item.item-big.clearfix > div.is-row.item-name.clearfix",
    "div/div[@class='name-c']/span/text()",
]
PAGINATION_QUERY = "ul.pagination.pagination-lg > li"
TAGS_QUERY = ".items.row.equal.img-grid.block-ins.block-ins-tag-s1"
TAG_HREF_QUERY = "div/div/div[@class='block-ins-caption']/a/@href"
