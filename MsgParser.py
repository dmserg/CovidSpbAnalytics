import re


class MsgParser:
    def __init__(self):
        self.p_cases = re.compile(
            r'.*Картина дня (?P<date>\d+ \w+).* (?P<new_cases>\d+) новы.*Петербурге\s+(?P<total_cases>\d+).*', re.DOTALL | re.IGNORECASE)

        self.p_tested = re.compile(
            r'.*коронавирус[^0-9]+(?P<tested>\d+) +человек.*', re.DOTALL | re.IGNORECASE)

        self.p_cured_died = re.compile(
            r'.*[кончались|мерло|мерших][^0-9]+(?P<died>\d+)че.*здоровел[^0-9]+(?P<cured>\d+)че.*',
            re.DOTALL | re.IGNORECASE)

    def parse_tested(self, msg):
        return self.__parse__(msg, self.p_tested, ["tested"])

    def parse_cases(self, msg):
        return self.__parse__(msg, self.p_cases, ["date", "new_cases", "total_cases"])

    def parse_cured_died(self, msg):
        return self.__parse__(re.sub(r"\s", "", msg), self.p_cured_died, ["cured", "died"])

    def parse(self, msg):
        m_cases = self.parse_cases(msg)
        m_tested = self.parse_tested(msg)
        m_cured_died = self.parse_cured_died(msg)

        if m_cases and m_tested and m_cured_died:
            return {**m_cases, **m_tested, **m_cured_died}
        else:
            return None

    @staticmethod
    def __parse__(msg, rx, group_names):
        m = rx.search(msg)
        if m:
            return {col: m.group(col) for col in group_names}
        else:
            return None
