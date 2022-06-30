import pandas as pd
import spacy
import logging
import os
from tqdm import tqdm

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def check_occ(lemma_list, count_dict):
    # TODO: refine list
    affect = ["interessant", "traurig", "überraschend", "sicher",
              "neugierig", "glücklich", "uninteressant", "unglücklich"]
    appreciation = ["wichtig", "bedeutend", "wesentlich", "nützlich",
                    "unwichtig", "notwendig", "hilfreich", "sinnvoll"]
    judgement = ["vernünftig", "logisch", "richtig", "rational",
                 "relevant", "unvernünftig", "irrelevant", "falsch"]
    for lem in lemma_list:
        if lem in affect:
            count_dict["affect_count"] += 1
        elif lem in appreciation:
            count_dict["appreciation_count"] += 1
        elif lem in judgement:
            count_dict["judgement_count"] += 1
        count_dict["total_count"] += 1
    return count_dict


def cal_freq_data(year):
    spacy.prefer_gpu()
    nlp = spacy.load("de_dep_news_trf")
    folder_path = os.path.join("data", year)
    file_names = os.listdir(folder_path)
    freq_dict = {}
    for file_name in file_names:
        logging.info(f"Processing: {file_name}")
        file_path = os.path.join(folder_path, file_name)
        in_file = open(file_path, 'r', encoding='utf-8')
        in_file_lines = in_file.readlines()
        in_file.close()
        count_dict = {
            "affect_count": 0,
            "appreciation_count": 0,
            "judgement_count": 0,
            "total_count": 0
        }
        for line in tqdm(in_file_lines):
            doc = nlp(line)
            token_lemma_list = [token.lemma_ for token in doc]
            token_lemma_list = [token for token in token_lemma_list if token != "--"][:-1]
            count_dict = check_occ(token_lemma_list, count_dict)
        affect_freq = count_dict["affect_count"] / count_dict["total_count"]
        appreciation_freq = count_dict["appreciation_count"] / count_dict["total_count"]
        judgement_freq = count_dict["judgement_count"] / count_dict["total_count"]
        freq_dict[file_name[:10]] = {
            "affect_freq": affect_freq,
            "appreciation_freq": appreciation_freq,
            "judgement_freq": judgement_freq
        }
    df = pd.DataFrame.from_dict(freq_dict, orient='index')
    df = df.reset_index().rename(columns={'index': 'Date'})
    return df


def export_data(df, year):
    data_path = os.path.join("data", f"freq_{year}.tsv")
    df.to_csv(data_path, sep="\t")
    logging.info(f"data saved in {data_path}")


def main():
    year = ["2020", "2021"]
    for i in year:
        df = cal_freq_data(i)
        export_data(df, i)


if __name__ == "__main__":
    main()
