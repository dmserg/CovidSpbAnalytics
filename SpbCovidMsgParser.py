import re


class SpbCovidMsgParser:
    def __init__(self):
        self.p_total_cases = re.compile(
            r'.*новы.*Петербурге\s+(?P<total_cases>\d+).*', re.DOTALL | re.IGNORECASE)

        self.p_new_cases = re.compile(
            r'.*Картина дня (?P<date>\d+ \w+).* (?P<new_cases>\d+) новы.*', re.DOTALL | re.IGNORECASE)

        self.p_tested = re.compile(
            r'.*коронавирус[^0-9]+(?P<tested>\d+)\s*человек.*', re.DOTALL | re.IGNORECASE)

        self.p_cured_died = re.compile(
            r'.*(кончались|мерло|мерших)(?P<died>\d+)че.*здоровел[^0-9]+(?P<cured>\d+)че.*',
            re.DOTALL | re.IGNORECASE)

        self.p_died = re.compile(
            r'.*(кончались|мерло|мерших)(?P<died>\d+)(че|\*).*',
            re.DOTALL | re.IGNORECASE)

        self.p_cured = re.compile(
            r'.*здоровел[^0-9]+(?P<cured>\d+)че.*',
            re.DOTALL | re.IGNORECASE)

        self.p_stat2021 = re.compile(
            r'.*За последние сутки в Петербурге.*выздоровели\s*(?P<cured_per_day>\d+).*скончались\s*(?P<died_per_day>\d+).*',
            re.DOTALL | re.IGNORECASE)

        self.p_find_digit_with_spaces = re.compile(r"\d+( )\d+")

    def parse_tested(self, msg):
        return self.__parse__(msg, self.p_tested, ["tested"])

    def parse_new_cases(self, msg):
        return self.__parse__(msg, self.p_new_cases, ["date", "new_cases"])

    def parse_cured_died(self, msg):
        return self.__parse__(re.sub(r"\s", "", msg), self.p_cured_died, ["cured", "died"])

    def parse_total_cases(self, msg):
        return self.__parse__(msg, self.p_total_cases, ["total_cases"])

    def parse_cured(self, msg):
        return self.__parse__(re.sub(r"\s", "", msg), self.p_cured, ["cured"])

    def parse_died(self, msg):
        return self.__parse__(re.sub(r"\s", "", msg), self.p_died, ["died"])

    def parse_stat_2021(self, msg):
        return self.__parse__(msg, self.p_stat2021, ["cured_per_day", "died_per_day"])

    def parse(self, msg):
        clean_msg = self.remove_spaces_in_numbers(msg)
        m_new_cases = self.parse_new_cases(clean_msg)
        m_total_cases = self.parse_total_cases(clean_msg)
        m_tested = self.parse_tested(clean_msg)
        m_cured_died = self.parse_cured_died(clean_msg)
        m_stat_2021 = self.parse_stat_2021(clean_msg)

        if m_tested and m_new_cases and m_stat_2021:
            return {**m_new_cases, **m_tested, **m_stat_2021, **{"total_cases":None, "died":None, "cured":None}}
        if m_new_cases and m_total_cases and m_tested and m_cured_died:
            return {**m_new_cases, **m_total_cases, **m_tested, **m_cured_died, **{"cured_per_day":None, "died_per_day":None}}
        else:
            return None

    @staticmethod
    def __parse__(msg, rx, group_names):
        m = rx.search(msg)
        if m:
            return {col: m.group(col) for col in group_names}
        else:
            return None

    def remove_spaces_in_numbers(self, msg):
        def space_repl(match):
            return match.group().replace(" ", "")
        return self.p_find_digit_with_spaces.sub(space_repl, msg)
