from pathlib import Path
import pandas as pd
import scrapy
import ast

DATA_FILE = "../data/preproc/preproc_en_train.csv"


class QuotesSpider(scrapy.Spider):
    name = "MedlinePlus"

    def start_requests(self):

        df = pd.read_csv(DATA_FILE)
        drug_id = df['medline_plus_id'].tolist()

        drug_id_list = []
        urls = []

        for item in drug_id:

            l = ast.literal_eval(item)
            l = [item.strip() for item in l]

            for i in l:
                # print(i)
                if i == 'None':
                    continue
                drug_id_list.append(i)
            drug_id_list = list(set(drug_id_list))
            drug_id_list.sort()

        for i in drug_id_list:
            urls.append(f"https://medlineplus.gov/druginfo/meds/{i}.html")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        drug_id = response.url.split("/")[-1][:-5]
        filename = f"../data/crawler/MedlinePlus/MedlinePlus-{drug_id}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")