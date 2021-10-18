import scrapy
from collections import defaultdict
from chefkoch.items import ChefkochItem


class ChefkochSpider(scrapy.Spider):
    name = "chefkoch"
    #allowed_domains = "chefkoch.de"

    def start_requests(self):
        urls = [
            'https://www.chefkoch.de/rs/s0/Rezepte.html',
            
        ]
        recipe_urls = []
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_hrefs, meta={"recipe_urls": recipe_urls})

    def parse_hrefs(self, response):
        articles = response.css("article")
        recipe_urls = response.meta.get("recipe_urls")
        for article in articles:
            recipe_url = article.css("a::attr(href)").get()
            recipe_urls.append(recipe_url)

        next_page = response.css("a.ds-page-link.bi-paging-next::attr(href)").get()
        if next_page!=None:
            yield scrapy.Request(next_page, callback= self.parse_hrefs, meta={"recipe_urls": recipe_urls})
        else:
            for recipe_url in recipe_urls:
                yield scrapy.Request(recipe_url, callback=self.parse_recipe)

    def parse_recipe(self, response):
        #scrape articles from 3 different sections
        item = ChefkochItem()
        #general info:
        general_info = response.css("article.ds-box.ds-grid-float.ds-col-12.ds-col-m-8.recipe-header")
        title = general_info.css("h1::text").get().strip()
        rating_count = general_info.css("div.ds-rating-stars::attr(title)").getall()[-1] #hard coded last because we get ratings for "weitere Rezepte"
        rating = general_info.css("div.ds-rating-avg > span > strong::text").get().strip()
        prep_time = general_info.css("small.ds-recipe-meta.recipe-meta > span.recipe-preptime.rds-recipe-meta__badge::text").get().strip()
        difficulty = general_info.css("small.ds-recipe-meta.recipe-meta > span.recipe-difficulty.rds-recipe-meta__badge::text").get().strip()
        recipe_date = general_info.css("small.ds-recipe-meta.recipe-meta > span.recipe-date.rds-recipe-meta__badge::text").get().strip()

        
        #scrape ingredients:
        table = response.css("table.ingredients.table-header").css("tbody > tr")
        ingredients = {}

        for row in table:
            try:
                units = " ".join(row.css("td.td-left > span::text").get().strip().split())
            except:
                units = ""
            try:
                ingredient = row.css("td.td-right > span::text").get().strip()
            except:
                ingredient = row.css("td.td-right > span > a::text").get().strip()

            ingredients[ingredient] = units


        #scrape recipe text + labels:
        article = response.css("article.ds-box:nth-child(7)")
        recipe_text = article.css("div.ds-box::text").get()
        recipe_tags =  set(" ".join(article.css("div.ds-box.recipe-tags ::text").getall()).split())

        item["title"] = title
        item["rating_count"] = rating_count
        item["rating"] = rating
        item["prep_time"] = prep_time
        item["difficulty"] = difficulty
        item["recipe_date"] = recipe_date
        item["ingredients"] = ingredients
        item["recipe_text"] = recipe_text
        item["recipe_tags"] = recipe_tags
        item["recipe_url"] = response.url

        yield item


        