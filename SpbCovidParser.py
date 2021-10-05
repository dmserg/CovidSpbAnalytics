import argparse
import json
import re
from SpbCovidMsgParser import SpbCovidMsgParser
import pandas as pd
import datetime as dt
import dateutil.parser as du_parser
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib as mpl
from datetime import datetime

SKIP_LABELS = 10

def main():
    parser = argparse.ArgumentParser(description='Process JSON with covid messages.')
    parser.add_argument('--filename', help='Messages JSON dump file')
    args = parser.parse_args()

    parse_covid_data(args.filename)


def parse_covid_data(filename):
    with open(filename, 'r', encoding="utf8") as f:
        msg_dict = json.load(f)

    msgFilter = re.compile("Картина дня", re.IGNORECASE)
    list = [(msg["message"], msg["date"]) for msg in msg_dict if
            msg["_"] and msg["_"] == "Message" and msgFilter.match(msg["message"])]

    msgParser = SpbCovidMsgParser()
    for (msg, _) in list:
        parsed_items = msgParser.parse(msg)
        if parsed_items:
            print("Date:{}, New cases:{}, total cases:{}, Tested:{}, cured:{}, died:{}, cured per day:{}, died per day:{}"
                  .format(parsed_items["date"],
                            parsed_items["new_cases"],
                            parsed_items["total_cases"],
                            parsed_items["tested"],
                            parsed_items["cured"],
                            parsed_items["died"],
                            parsed_items["cured_per_day"],
                            parsed_items["died_per_day"]))
        else:
            print("Can't parse: " + msg)

    parsed_items = [(msgParser.parse(msg), msgDate) for (msg, msgDate) in reversed(list)]
    df = pd.DataFrame(
        data=[[(du_parser.parse(date).date() + dt.timedelta(days=-1)).strftime("%d-%m-%Y"), items["date"],
               items["new_cases"], items["total_cases"], items["tested"], items["cured"], items["died"], items["cured_per_day"], items["died_per_day"]] for
              (items, date)
              in parsed_items if items],
        columns=["MsgDate", "ReportDate", "NewCases", "TotalCases", "TestedPerDay", "Cured", "Died", "CuredPerDay", "DiedPerDay"]
    ).apply(pd.to_numeric, errors='ignore')
    cleanup_covid_data(df)

    df["NewCasesRatio"] = df["NewCases"] / df["TestedPerDay"]
    df["ActiveCases"] = df["TotalCases"] - df["Cured"] - df["Died"]
    df["CuredPerDay"] = df["Cured"].diff()
    df["DiedPerDay"] = df["Died"].diff()
    df["MsgDateLabel"] = [a if ind % SKIP_LABELS == 0 or ind==len(df["MsgDate"])-1 else "" for ind, a in enumerate(df["MsgDate"])]
    df["MsgDateWeekNum"] = [datetime.strptime(d, '%d-%m-%Y').isocalendar()[1] for d in df["MsgDate"]]

    print(df.to_markdown())

    aggregated_result = df.groupby("MsgDateWeekNum")[["NewCases", "TestedPerDay"]].sum()
    aggregated_result["NewCasesRatio"] = aggregated_result["NewCases"] / aggregated_result["TestedPerDay"]

    return df, aggregated_result

def cleanup_covid_data(df):
    df.loc[df["MsgDate"] == "01-01-2021", ["TotalCases"]] = 249612
    df.loc[df["MsgDate"] == "06-04-2020", ["NewCases"]] = 69
    df.loc[df["MsgDate"] == "06-04-2020", ["Cured"]] = 36
    df.loc[df["MsgDate"] == "06-04-2020", ["TestedPerDay"]] = 6957
    df.loc[df["MsgDate"] == "06-04-2020", ["TotalCases"]] = 295

    # Fix missing data (data format change since 2021-08-01)
    for i, row in df.iterrows():
        if pd.isnull(row["TotalCases"]):
            df.at[i, "TotalCases"] = df.at[i-1, "TotalCases"] + row["NewCases"]
        if pd.isnull(row["Cured"]):
            df.at[i, "Cured"] = df.at[i - 1, "Cured"] + row["CuredPerDay"]
        if pd.isnull(row["Died"]):
            df.at[i, "Died"] = df.at[i - 1, "Died"] + row["DiedPerDay"]

def plot_covid_charts_cured_vs_newcases(df):
    mpl.style.use('seaborn')
    rc('mathtext', default='regular')

    cured_fig = plt.figure()
    cured_fig.add_subplot(111)

    cured_per_day_ax = df["CuredPerDay"].plot(x="MsgDate", color='#2DA8D8FF', kind='bar', label="Cured per day")
    df["NewCases"].plot(x="MsgDate", ax=cured_per_day_ax, color='#D9514EFF', kind='bar', label="New cases per day")
    df["DiedPerDay"].plot(x="MsgDate", ax=cured_per_day_ax, color='#2A2B2DFF', kind='bar', label="Died per day")
    cured_per_day_ax.set_xticklabels(df["MsgDateLabel"], rotation='vertical')
    cured_per_day_ax.legend()
    plt.title("Covid-19 Spb Cured vs New Cases per Day")

def plot_covid_charts_active_cases(df):
    mpl.style.use('seaborn')
    rc('mathtext', default='regular')

    total_cases_fig = plt.figure()
    total_cases_fig.add_subplot(111)

    total_cases_ax = df["TotalCases"].plot(x="MsgDate", color='#2DA8D8FF', kind='bar', label="Total Cases")
    df["ActiveCases"].plot(x="MsgDate", ax=total_cases_ax, color='#D9514EFF', kind='bar', label="Active Cases")
    df["TestedPerDay"].plot(x=df.index, color='#2A2B2DFF', label="Tested per Day", grid=True, linestyle='-')
    df["Died"].plot(x=df.index, color='brown', label="Died Total", grid=True, linestyle='--', marker='+')
    df["Cured"].plot(x=df.index, color='green', label="Cured Total", grid=True, linestyle='--', marker='+')
    total_cases_ax.set_xticklabels(df["MsgDateLabel"], rotation='vertical')

    total_cases_ax.legend()
    plt.title("Covid-19 Spb Cases")

    #plt.savefig("ActiveCases.png", dpi=190)


def plot_covid_charts_new_cases(df):
    mpl.style.use('seaborn')
    rc('mathtext', default='regular')
    new_cases_fig = plt.figure()
    new_cases_plot = new_cases_fig.add_subplot(111)
    lns_new_cases = new_cases_plot.bar(df["MsgDate"], df["NewCases"], label='New Cases', color='#1f77b4')
    #lns_cured_per_day = new_cases_plot.plot(df["MsgDate"], df["CuredPerDay"], label='Cured per Day', color='#D9514EFF')
    new_cases_ratio_plot = new_cases_plot.twinx()
    lns_new_cases_ratio = new_cases_ratio_plot.bar(df["MsgDate"], df["NewCasesRatio"], label='New Cases Ratio', color='#ff7f0e')
    new_cases_plot.legend((lns_new_cases, lns_new_cases_ratio),
                         (lns_new_cases.get_label(), lns_new_cases_ratio.get_label()))
    new_cases_plot.grid()
    new_cases_plot.set_xlabel("Date")
    new_cases_plot.set_ylabel(r"Number of new cases")
    new_cases_plot.set_xticklabels(df["MsgDateLabel"], rotation='vertical')
    plt.title("Covid-19 Spb New Cases")

    #plt.savefig("NewCases.png", dpi=190)


if __name__ == '__main__':
    main()
