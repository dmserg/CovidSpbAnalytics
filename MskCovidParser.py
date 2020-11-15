import argparse
import json
import re
from MskCovidMsgParser import MskCovidMsgParser
import pandas as pd
import datetime as dt
import dateutil.parser as du_parser
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib as mpl
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description='Process JSON with covid messages.')
    parser.add_argument('--filename', help='Messages JSON dump file')
    args = parser.parse_args()

    parse_and_display(args.filename)

def parse_and_display(filename):
    with open(filename, 'r', encoding="utf8") as f:
        msg_dict = json.load(f)

    msgFilter = re.compile(".*ИВЛ", re.IGNORECASE)
    list = [(msg["message"], msg["date"]) for msg in msg_dict if
            msg["_"] and msg["_"] == "Message" and msgFilter.match(msg["message"])]

    msgParser = MskCovidMsgParser()
    for (msg, msgDate) in list:
        parsed_items = msgParser.parse(msg)
        if parsed_items:
            print("Date:{}, New cases:{}, lung ventilation cases:{}, hospital:{}".format(msgDate,
                                                                                               parsed_items[
                                                                                                   "new_cases"],
                                                                                               parsed_items[
                                                                                                   "lv_cases"],
                                                                                               parsed_items[
                                                                                                   "hospital_cases"]
                                                                                               ))
        else:
            print("Can't parse: " + msg)

    parsed_items = [(msgParser.parse(msg), msgDate) for (msg, msgDate) in reversed(list)]
    df = pd.DataFrame(
        data=[[msgDate, items["new_cases"], items["lv_cases"], items["hospital_cases"]] for
              (items, date)
              in parsed_items if items],
        columns=["MsgDate", "NewCases", "LVCases", "InHospital"]
    ).apply(pd.to_numeric, errors='ignore')

    df.to_csv("msk_covid_parsed.csv")

    #plot_covid_charts_new_cases(df)
    #plot_covid_charts_active_cases(df)
    #plot_covid_charts_cured_vs_died(df)

    #plt.show()

if __name__ == '__main__':
    main()
