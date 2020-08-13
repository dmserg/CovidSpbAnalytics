import argparse
import json
import re
from MsgParser import MsgParser
import pandas as pd
import datetime as dt
import dateutil.parser as du_parser
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib as mpl


def main():
    parser = argparse.ArgumentParser(description='Process JSON with covid messages.')
    parser.add_argument('--filename', help='Messages JSON dump file')
    args = parser.parse_args()

    parse_and_display(args.filename)
    # df.to_csv("covid_parsed.csv")


def parse_and_display(filename):
    with open(filename, 'r', encoding="utf8") as f:
        msg_dict = json.load(f)

    msgFilter = re.compile("Картина дня", re.IGNORECASE)
    list = [(msg["message"], msg["date"]) for msg in msg_dict if
            msg["_"] and msg["_"] == "Message" and msgFilter.match(msg["message"])]

    msgParser = MsgParser()
    for (msg, _) in list:
        parsed_items = msgParser.parse(msg)
        if parsed_items:
            print("Date:{}, New cases:{}, total cases:{}, Tested:{}, cured:{}, died:{}".format(parsed_items["date"],
                                                                                        parsed_items["new_cases"],
                                                                                        parsed_items["total_cases"],
                                                                                        parsed_items["tested"],
                                                                                        parsed_items["cured"],
                                                                                        parsed_items["died"]))
        else:
            print("Can't parse: " + msg)

    parsed_items = [(msgParser.parse(msg), d) for (msg, d) in reversed(list)]
    df = pd.DataFrame(
        data=[[(du_parser.parse(date).date() + dt.timedelta(days=-1)).strftime("%d-%m-%Y"), items["date"],
               items["new_cases"], items["total_cases"], items["tested"], items["cured"], items["died"]] for
              (items, date)
              in parsed_items if items],
        columns=["MsgDate", "ReportDate", "NewCases", "TotalCases", "Tested", "Cured", "Died"]
    ).apply(pd.to_numeric, errors='ignore')
    df["NewCasesRatio"] = df["NewCases"] / df["Tested"]
    df["ActiveCases"] = df["TotalCases"] - df["Cured"] - df["Died"]
    df["MsgDateLabel"] = [a if ind % 2 != len(df.index) % 2 else "" for ind, a in enumerate(df["MsgDate"])]

    plot_covid_charts_new_cases(df)
    plot_covid_charts_active_cases(df)

    plt.show()


def plot_covid_charts_active_cases(df):
    mpl.style.use('seaborn')
    rc('mathtext', default='regular')

    total_cases_fig = plt.figure()
    total_cases_fig.add_subplot(111)

    total_cases_ax = df["TotalCases"].plot(x="MsgDate", color='#2DA8D8FF', kind='bar', label="Total Cases")
    df["ActiveCases"].plot(x="MsgDate", ax=total_cases_ax, color='#D9514EFF', kind='bar', label="Active Cases")
    df["Tested"].plot(x=df.index, color='#2A2B2DFF', label="Tested per Day", grid=True, linestyle='dotted', marker='o')
    df["Died"].plot(x=df.index, color='brown', label="Died Total", grid=True, linestyle='--', marker='+')
    df["Cured"].plot(x=df.index, color='green', label="Cured Total", grid=True, linestyle='--', marker='+')
    total_cases_ax.set_xticklabels(df["MsgDateLabel"], rotation='vertical')

    total_cases_ax.legend()
    plt.title("Covid-19 Spb Cases")


def plot_covid_charts_new_cases(df):
    mpl.style.use('seaborn')
    rc('mathtext', default='regular')
    new_cases_fig = plt.figure()
    new_cases_plot = new_cases_fig.add_subplot(111)
    lns_new_cases = new_cases_plot.bar(df["MsgDate"], df["NewCases"], label='New Cases', color='#1f77b4')
    new_cases_ratio_plot = new_cases_plot.twinx()
    lns_new_cases_ratio = new_cases_ratio_plot.bar(df["MsgDate"], df["NewCasesRatio"], label='New Cases Ratio', color='#ff7f0e')
    new_cases_plot.legend((lns_new_cases, lns_new_cases_ratio),
                         (lns_new_cases.get_label(), lns_new_cases_ratio.get_label()))
    new_cases_plot.grid()
    new_cases_plot.set_xlabel("Date")
    new_cases_plot.set_ylabel(r"Number of new cases")
    new_cases_plot.set_xticklabels(df["MsgDateLabel"], rotation='vertical')
    plt.title("Covid-19 Spb New Cases")



if __name__ == '__main__':
    main()
