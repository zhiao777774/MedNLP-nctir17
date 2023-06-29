from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "MedlinePlus"

    def start_requests(self):
        urls = [
            "https://medlineplus.gov/druginfo/meds/a687009.html",
            "https://medlineplus.gov/druginfo/meds/a614007.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        drug_id = response.url.split("/")[-1][:-5]
        filename = f"MedlinePlus-{drug_id}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")