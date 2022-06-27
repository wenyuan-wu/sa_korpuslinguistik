import os
from tqdm import tqdm
import pandas as pd
import logging


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def load_df(year):
    data_path = os.path.join("data", "WHO-COVID-19-global-data.csv")
    df = pd.read_csv(data_path, sep=',', header=0)
    df = df[df["Country"] == "Germany"]
    start_year = str(int(year) - 1)
    end_year = str(int(year) + 1)
    df = df[(df["Date_reported"] > f'{start_year}-12-31') & (df["Date_reported"] < f'{end_year}-01-01')]
    df = df[["Date_reported", "New_deaths"]]
    return df


def sort_df(df, year):
    df['Date_reported'] = pd.to_datetime(df['Date_reported'], format="%Y-%m-%d")
    first_date = df.iloc[0]['Date_reported']
    first_year = first_date.year
    new_year = pd.Timestamp(f'{year}-01-01T00')
    if first_date == new_year:
        logging.info(f"The first day of year {first_year} already exists!")
    else:
        logging.info(f"Creating placeholder data for the first day of year {first_year}")
        df.loc[-1] = [new_year, 0]
        df.index = df.index + 1
        df = df.sort_index()
    df = df.groupby(pd.Grouper(
        key="Date_reported",
        axis=0,
        freq="10D",
        sort=True))['New_deaths'].apply(list).reset_index(name='New_deaths_list')
    df['Span_total'] = df.apply(lambda row: sum(row["New_deaths_list"]), axis=1)
    return df


def export_data(df, year):
    data_path = os.path.join("data", f"who_{year}.tsv")
    df.to_csv(data_path, sep="\t")
    logging.info(f"data saved in {data_path}")


def main():
    year = ["2020", "2021"]
    for i in year:
        df = load_df(i)
        who_data = sort_df(df, i)
        export_data(who_data, i)


if __name__ == '__main__':
    main()
