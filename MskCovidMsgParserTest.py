import unittest
from MskCovidMsgParser import MskCovidMsgParser

class MskCovidMsgParserTest(unittest.TestCase):

    def setUp(self):
        self.msg_oct21 = """❗️На ИВЛ в Москве находятся 383 пациента с COVID-19

В столице подтверждено 4389 новых случаев коронавируса. За последние сутки госпитализировано 1215 пациентов с COVID-19. На ИВЛ в больницах Москвы находится 383 человека.

Среди новых выявленных случаев:

🔹44,1%— от 18 до 45 лет
🔹31,6%— от 46 до 65 лет
🔹11,0%— от 66 до 79 лет
n🔹4,5% — старше 80 лет
🔹8,8% — дети

Оперштаб напоминает о необходимости соблюдения домашнего режима горожанам старше 65 лет и москвичам с хроническими заболеваниями."""


    def test_oct21_cases(self):
        p = MskCovidMsgParser()
        result = p.parse_cases(self.msg_oct21)

        self.assertEqual("4389", result["new_cases"])
        self.assertEqual("383", result["lv_cases"])
        self.assertEqual("1215", result["hospital_cases"])