import re


class MsgParser:
    def __init__(self):
        self.p_cases = re.compile(
            r'Картина дня (?P<date>\d+ \w+).* (?P<new_cases>\d+)\s+новы.* (?P<total_cases>\d+)[\n| ]случа.*на коронавирус[\n| ](?P<Tested>\d+).*',
            re.DOTALL | re.IGNORECASE)

        self.p_cured_died = re.compile(
            r'.*[кончались|мерло|мерших][^0-9]+(?P<died>\d+)че.*здоровел[^0-9]+(?P<cured>\d+)че.*',
            re.DOTALL | re.IGNORECASE)

    def parse_cases(self, msg):
        m = self.p_cases.search(msg)
        if m:
            return {
                "date": m.group("date"),
                "new_cases": m.group("new_cases"),
                "total_cases": m.group("total_cases"),
                "tested": m.group("Tested")
            }
        else:
            return None

    def parse_cured_died(self, msg):
        m = self.p_cured_died.search(re.sub(r"\s", "", msg))
        if m:
            return {
                "cured": m.group("cured"),
                "died": m.group("died")
            }
        else:
            return None
