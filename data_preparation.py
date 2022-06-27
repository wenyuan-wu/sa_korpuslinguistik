import os
from tqdm import tqdm
import pandas as pd
import logging
import csv

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def load_df(year):
    folder_path = os.path.join("data", f"deu_news_{year}_1M")
    sents_path = os.path.join(folder_path, f"deu_news_{year}_1M-sentences.txt")
    sents_col = ["sent_id", "sent"]
    sents_df = pd.read_csv(sents_path, sep='\t', names=sents_col, quoting=csv.QUOTE_NONE)
    logging.info(f"Processing file: {sents_path}")
    source_path = os.path.join(folder_path, f"deu_news_{year}_1M-sources.txt")
    source_col = ["src_id", "src", "date"]
    source_df = pd.read_csv(source_path, sep='\t', names=source_col, quoting=csv.QUOTE_NONE)
    logging.info(f"Processing file: {source_path}")
    inv_src_path = os.path.join(folder_path, f"deu_news_{year}_1M-inv_so.txt")
    inv_src_col = ["src_id", "sent_id"]
    inv_src_df = pd.read_csv(inv_src_path, sep='\t', names=inv_src_col, quoting=csv.QUOTE_NONE)
    logging.info(f"Processing file: {inv_src_path}")
    temp_df = pd.merge(sents_df, inv_src_df, on="sent_id", how="left")
    temp_df = pd.merge(temp_df, source_df, on="src_id", how="left")
    temp_df.drop(["src_id", "src"], axis=1, inplace=True)
    return temp_df


def date_clean_up(df, year):
    counter = 0
    for idx, row in tqdm(df.iterrows()):
        if not row["date"].startswith(year):
            new_val = year + row["date"][-6:]
            df.at[idx, "date"] = new_val
            counter += 1
    logging.info(f"date clean-up for year {year}: {counter} rows affected")
    return df


def sort_df(df, year):
    date_clean_up(df, year)
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
    sent_id_list = df.groupby(pd.Grouper(
        key="date",
        axis=0,
        freq="10D",
        sort=True))['sent_id'].apply(list).reset_index(name='sent_id_list')
    return sent_id_list


def export_data(sent_id_list, df, year):
    folder_path = os.path.join("data", year)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for idx, row in sent_id_list.iterrows():
        out_file = os.path.join(folder_path, f"{str(row['date'])[:10]}.txt")
        sent_list = row["sent_id_list"]
        text_list = []
        for sent_id in sent_list:
            sent = df[df["sent_id"] == sent_id]
            text_list.append(sent["sent"].values[0])
        with open(out_file, 'w', encoding='utf-8') as out_data:
            for sent in text_list:
                out_data.write(sent)
                out_data.write("\n")
            logging.info(f"data saved in {out_file}")


def main():
    year = ["2020", "2021"]
    for i in year:
        df = load_df(i)
        sent_id_list = sort_df(df, i)
        export_data(sent_id_list, df, i)


if __name__ == '__main__':
    main()
