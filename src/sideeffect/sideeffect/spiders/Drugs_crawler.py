import json
import pandas as pd
import scrapy
import ast

DATA_FILE = "../../data/preproc/preproc_en_train.csv"


class DrugsSpider(scrapy.Spider):
    name = "Drugs"
    allowed_domains = ["www.drugs.com"]
    start_urls = ["https://www.drugs.com/"]

    def start_requests(self):
        df = pd.read_csv(DATA_FILE)
        drug_names = df['drug_name'].tolist()
        drug_names = list(set(drug_names))

        for item in drug_names:
            drugs = ast.literal_eval(item)

            for drug in drugs:
                if drug == 'None':
                    continue

                yield scrapy.Request(
                    url=
                    f"https://www.drugs.com/sfx/{drug.lower()}-side-effects.html",
                    callback=self.parse)

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)

        drug_name = response.url.split('/')[-1].split('-')[0].capitalize()
        side_effects = {'normal': [], 'serious': []}

        xpath = lambda id: f'//h2[@id="{id}"]/following-sibling::h3[text()="More common"]/following-sibling::ul[1]'
        # Series: Series side effects / More Common
        ul = response.xpath(xpath('serious-side-effects'))
        side_effects['serious'] = ul.xpath('.//li//text()').getall()

        #　Normal: Other side effects / More common
        ul = response.xpath(xpath('other-side-effects'))
        side_effects['normal'] = ul.xpath('.//li//text()').getall()

        side_effects['normal'] = [
            li.strip() for li in side_effects['normal'] if li.strip()
        ]
        side_effects['serious'] = [
            li.strip() for li in side_effects['serious'] if li.strip()
        ]

        # self.logger.info(side_effects)
        yield {drug_name: side_effects}
