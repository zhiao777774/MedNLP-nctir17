import pandas as pd
import re
from drug_named_entity_recognition import find_drugs

TRAINING_DATA_FILE = 'data/ntcir17_mednlp-sc_sm_en_train_26_06_23.csv'


def load_training_data(file_path):

    df = pd.read_csv(file_path)
    return df


def find_medicine(sentence):

    sentence = re.split(r'[^a-zA-Z0-9]', sentence)
    med_ner = find_drugs(sentence, is_ignore_case=True)

    return med_ner


def take_drug_name(durg_info):

    drug_name = []
    drugbank_id = []

    try:
        for item in durg_info:
            drug_name.append(item[0]['name'])
            drugbank_id.append(item[0]['drugbank_id'])
    except:
        drug_name = 'None'
        drugbank_id = 'None'

    if len(drug_name) == 0:
        drug_name = 'None'
        drugbank_id = 'None'

    return drug_name, drugbank_id


def main():

    df = load_training_data(TRAINING_DATA_FILE)

    drug_name_list = []
    drugbank_id_list = []

    for i in df['text']:
        durg_info = find_medicine(i)
        drug_name, drugbank_id = take_drug_name(durg_info)
        drug_name_list.append(drug_name)
        drugbank_id_list.append(drugbank_id)

    # add drug name and drugbank id
    df['drug_name'] = drug_name_list
    df['drugbank_id'] = drugbank_id_list

    # save to csv
    df.to_csv('data/preproc/data_with_drug.csv')


if __name__ == '__main__':
    main()
