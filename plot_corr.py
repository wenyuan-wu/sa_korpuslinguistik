import os
from tqdm import tqdm
import pandas as pd
import logging
import seaborn as sns
import matplotlib.pyplot as plt


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def cal_corr_df(year):
    who_data_path = os.path.join("data", f"who_{year}.tsv")
    who_df = pd.read_csv(who_data_path, sep='\t', header=0, index_col=0)
    freq_data_path = os.path.join("data", f"freq_{year}.tsv")
    freq_df = pd.read_csv(freq_data_path, sep='\t', header=0, index_col=0)
    freq_df = freq_df.rename(columns={'Date': 'Date_reported'})
    df = pd.merge(who_df, freq_df, on="Date_reported", how="left")
    col_1 = ['affect_freq', 'appreciation_freq', 'judgement_freq']
    col_2 = ['New_cases_total', 'New_deaths_total']
    entry_list = []
    corr_list = []
    for i in col_1:
        for j in col_2:
            corr = cal_corr(df, i, j)
            entry = f"{i[:-5]}" + "_" + f"{j[:-6]}"
            entry_list.append(entry)
            corr_list.append(corr)
    entry_list.append("who_case_death")
    corr_list.append(cal_corr(df, "New_cases_total", "New_deaths_total"))
    corr_df = pd.DataFrame(list(zip(entry_list, corr_list)), columns=["Entry", "val"])
    return df, corr_df


def cal_corr(df, col_1, col_2):
    corr = df[col_1].corr(df[col_2], method="pearson")
    return corr


def export_data(df, year):
    data_path = os.path.join("data", f"freq_combi_{year}.tsv")
    df[0].to_csv(data_path, sep="\t")
    logging.info(f"data saved in {data_path}")
    data_path = os.path.join("data", f"corr_{year}.tsv")
    df[1].to_csv(data_path, sep="\t")
    logging.info(f"data saved in {data_path}")


def export_corr_plot(df, year):
    col_1 = ['affect_freq', 'appreciation_freq', 'judgement_freq']
    col_2 = ['New_cases_total', 'New_deaths_total']
    folder_path = os.path.join("info", year)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for i in col_1:
        for j in col_2:
            plt.clf()
            plot_corr(df[0], i, j)
            entry = f"{i[:-5]}" + "_" + f"{j[:-6]}"
            file_path = os.path.join(folder_path, f"{entry}.png")
            plt.savefig(file_path)
            logging.info(f"plot saved in {file_path}")
    plt.clf()
    plot_corr(df[0], "New_cases_total", "New_deaths_total")
    file_path = os.path.join(folder_path, f"who_corr.png")
    plt.savefig(file_path)
    logging.info(f"plot saved in {file_path}")


def plot_corr(df, col_1, col_2):
    sns.regplot(x=df[col_1], y=df[col_2])


def main():
    year = ["2020", "2021"]
    for i in year:
        df = cal_corr_df(i)
        export_data(df, i)
        export_corr_plot(df, i)


if __name__ == '__main__':
    main()
