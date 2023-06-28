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


def take_drug_id(drug_info):

    drug_name = []
    drugbank_id = []
    medline_plus_id = []
    mesh_id = []
    nhs_url = []
    wikipedia_url = []

    for item in drug_info:
        drug_name.append(item[0]['name'])

        if 'drugbank_id' not in item[0].keys():
            drugbank_id.append('None')
        else:
            drugbank_id.append(item[0]['drugbank_id'])

        if 'medline_plus_id' not in item[0].keys():
            medline_plus_id.append('None')
        else:
            medline_plus_id.append(item[0]['medline_plus_id'])

        if 'mesh_id' not in item[0].keys():
            mesh_id.append('None')
        else:
            mesh_id.append(item[0]['mesh_id'])

        if 'nhs_url' not in item[0].keys():
            nhs_url.append('None')
        else:
            nhs_url.append(item[0]['nhs_url'])

        if 'wikipedia_url' not in item[0].keys():
            wikipedia_url.append('None')
        else:
            wikipedia_url.append(item[0]['wikipedia_url'])

    if len(drug_name) == 0:

        drug_name = ['None']
        drugbank_id = ['None']
        medline_plus_id = ['None']
        mesh_id = ['None']
        nhs_url = ['None']
        wikipedia_url = ['None']

    return drug_name, drugbank_id, medline_plus_id, mesh_id, nhs_url, wikipedia_url


def main():

    df = load_training_data(TRAINING_DATA_FILE)

    drug_name_list = []
    drugbank_id_list = []
    medline_plus_id_list = []
    mesh_id_list = []
    nhs_url_list = []
    wikipedia_url_list = []

    for i in df['text']:
        drug_info = find_medicine(i)
        drug_name, drugbank_id, medline_plus_id, mesh_id, nhs_url, wikipedia_url = take_drug_id(
            drug_info)
        drug_name_list.append(drug_name)
        drugbank_id_list.append(drugbank_id)
        medline_plus_id_list.append(medline_plus_id)
        mesh_id_list.append(mesh_id)
        nhs_url_list.append(nhs_url)
        wikipedia_url_list.append(wikipedia_url)

    # add columns
    df['drug_name'] = drug_name_list
    df['drugbank_id'] = drugbank_id_list
    df['medline_plus_id'] = medline_plus_id_list
    df['mesh_id'] = mesh_id_list
    df['nhs_url'] = nhs_url_list
    df['wikipedia_url'] = wikipedia_url_list

    # save to csv
    df.to_csv('data/preproc/preproc_en_train.csv')


if __name__ == '__main__':
    main()
