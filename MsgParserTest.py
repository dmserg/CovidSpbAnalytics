import unittest
from MsgParser import MsgParser

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.msg_aug10 = """КАРТИНА ДНЯ 10 АВГУСТА
➕ Зафиксировано 157 новых случаев заражения коронавирусной инфекцией.

📉 Всего с начала пандемии в Санкт-Петербурге 33204  случаев заражения COVID-19. 
Скончались 2176 человек. Выздоровело 24165 человек.

🔬 За последние сутки в Петербурге обследовали на коронавирус 12050 человек.

🏠 Под медицинским наблюдением находится 713 человек. Из них 150 - в обсерваторе, 299 - на самоизоляции, 264 - контактные."""

        self.msg_apr12 = """КАРТИНА ДНЯ 12 АПРЕЛЯ
➕ Зафиксирован 121 новый случай заражения коронавирусной инфекцией.

➖ Выздоровело 4 человека.

📈 Всего с начала пандемии в Санкт-Петербурге 678 случаев заражения COVID-19. 
Умерло 4 человека. Выздоровело 78 человек.
 
🔬 За последние сутки в Петербурге обследовали на коронавирус 1821 человека. 

🏠 На карантине находится  5605 человек. Из них 41 - в обсерваторе, 3128 - на самоизоляции, 2436 - контактные.
___

📞 В службе экстренных вызовов 112 зарегистрировано 406 обращений. О прибытии из другой страны на территорию России сообщили 76 человек. В Городскую службу скорой помощи направлено 111 обращений, в полицию - 108. Остальные звонки были справочного характера.
"""

        self.msg_apr22 = """КАРТИНА ДНЯ 22 АПРЕЛЯ 
 
➕ Зафиксирован 191 новый случай заражения коронавирусной инфекцией.

📈 Всего с начала пандемии в Санкт-Петербурге  2458 случаев заражения COVID-19. 
Умерло 17 человек. Выздоровело 368 человек.

🔬 За последние сутки в Петербурге обследовано на коронавирус  8196 человек. 

🏠 На карантине находится  2974 человека. Из них 63 - в обсерваторе, 545 - на самоизоляции, 2366 - контактные.
___

🚑 Обработано 1567 вызовов, поступивших на номер 122 в Единую региональную информационно-справочную службу по вопросам,связанным с коронавирусом.

📞 В службе экстренных вызовов 112 зарегистрировано 702 обращения. О прибытии из другой страны на территорию России сообщили 13 человек. В Городскую службу скорой помощи направлено 55 обращений, в полицию - 149. Остальные звонки были справочного характера."""

    def test_aug10_cases(self):
        p = MsgParser()
        result = p.parse_cases(self.msg_aug10)

        self.assertEqual("157", result["new_cases"])


    def test_apr12_cases(self):
        p = MsgParser()
        result = p.parse_cases(self.msg_apr12)
        self.assertEqual("12 АПРЕЛЯ", result["date"])
        self.assertEqual("121", result["new_cases"])
        self.assertEqual("678", result["total_cases"])

    def test_apr12_cured_died(self):
        p = MsgParser()
        result = p.parse_cured_died(self.msg_apr12)
        self.assertEqual("78", result["cured"])
        self.assertEqual("4", result["died"])

    def test_apr22_cases(self):
        p = MsgParser()
        result = p.parse_cases(self.msg_apr22)
        self.assertEqual("22 АПРЕЛЯ", result["date"])
        self.assertEqual("191", result["new_cases"])
        self.assertEqual("2458", result["total_cases"])

    def test_apr22_cured_died(self):
        p = MsgParser()
        result = p.parse_cured_died(self.msg_apr22)
        self.assertEqual("368", result["cured"])
        self.assertEqual("17", result["died"])

    def test_apr22_tested(self):
        p = MsgParser()
        result = p.parse_tested(self.msg_apr22)
        self.assertEqual("8196", result["tested"])

    def test_apr12_parse(self):
        p = MsgParser()
        result = p.parse(self.msg_apr12)
        self.assertEqual("12 АПРЕЛЯ", result["date"])
        self.assertEqual("121", result["new_cases"])
        self.assertEqual("678", result["total_cases"])
        self.assertEqual("78", result["cured"])
        self.assertEqual("4", result["died"])


if __name__ == '__main__':
    unittest.main()
