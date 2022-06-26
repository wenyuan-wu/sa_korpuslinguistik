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


def sort_df(df):
    print(df)
    

def main():
    year = ["2019", "2020", "2021"]
    df_1999 = load_df(year[0])
    sort_df(df_1999)


if __name__ == '__main__':
    main()
