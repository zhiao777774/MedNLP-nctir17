import pandas as pd
from drug_named_entity_recognition import find_drugs
import re


def remove_punctuation(sentence):
    

    sentence = "If I take metformin, could I get diabetes?"

    sentence = re.split(r'[^a-zA-Z0-9]', sentence)
    med_ner = find_drugs(sentence, is_ignore_case=True)

    print(med_ner)

def main():

    sentence = "If I take metformin, could I get diabetes?"

if __name__ == '__main__':
    main()

