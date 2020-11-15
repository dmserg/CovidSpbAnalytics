import re


class MskCovidMsgParser:
    def __init__(self):
        self.p_cases = re.compile(
            r'.*ИВЛ.* (?P<lv_cases>\d+) .*подтверждено\s+(?P<new_cases>\d+) новых случаев.*госпитализировано (?P<hospital_cases>\d+) пациент.*',
                re.DOTALL | re.IGNORECASE)

    def parse(self, msg):
        m_cases = self.parse_cases(msg)

        if m_cases:
            return m_cases
        else:
            return None

    def parse_cases(self, msg):
        return self.__parse__(msg, self.p_cases, ["new_cases", "lv_cases", "hospital_cases"])

    @staticmethod
    def __parse__(msg, rx, group_names):
        m = rx.search(msg)
        if m:
            return {col: m.group(col) for col in group_names}
        else:
            return None