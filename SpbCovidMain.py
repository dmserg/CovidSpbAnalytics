import argparse
import seaborn as sn
import matplotlib.pyplot as plt
from SpbCovidParser import parse_covid_data, plot_covid_charts_new_cases, plot_covid_charts_active_cases, plot_covid_charts_cured_vs_newcases
from SpbCovidDownload import download_covid_data

def main():
    parser = argparse.ArgumentParser(description='Parse and chart covid data from Spb Telegram Channel')
    parser.add_argument('-skip_download', help='Skip download', action='store_true')
    parser.add_argument('-no_charts', help='Don\'t display charts', action='store_true')
    args = parser.parse_args()

    if not args.skip_download:
        download_covid_data('channel_messages.json')
    df, aggregated_df = parse_covid_data('channel_messages.json')

    df.to_csv('spb_covid_parsed.csv')

    calculateAnalytics(df)

    if not args.no_charts:
        displayCharts(df)
        plt.show()

def calculateAnalytics(df):
    corrMatrix = df[["NewCases", "TestedPerDay", "DiedPerDay", "CuredPerDay", "TotalCases", "Cured", "Died"]].corr()
    print(corrMatrix)
    sn.heatmap(corrMatrix, annot=True)

def displayCharts(df):
    plot_covid_charts_new_cases(df)
    plot_covid_charts_active_cases(df)
    plot_covid_charts_cured_vs_newcases(df)

if __name__ == '__main__':
    main()
