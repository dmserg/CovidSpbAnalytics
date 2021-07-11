import unittest
from SpbCovidMsgParser import SpbCovidMsgParser

class SpbCovidMsgParserTest(unittest.TestCase):

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

        self.msg_nov8 = """Картина дня 8 ноября
 
➕ Зафиксировано 1403 новых случая заражения коронавирусной инфекцией.

📉 Всего с начала пандемии в Санкт-Петербурге 71426 случаев заражения COVID-19. 
Скончались 4181человек. Выздоровело 43501 человек.

🔬 За последние сутки в Петербурге обследовали на коронавирус 25651человека.

🏠 Под медицинским наблюдением находится 4039 человек. Из них 83 - в обсерваторе, 1405 - контактные, 2551 - на самоизоляции."""

        self.msg_apr6 = """КАРТИНА ДНЯ 6 АПРЕЛЯ
 
➕ Зафиксировано 69 новых случаев заражения коронавирусной инфекцией.

📈 Всего с начала пандемии в Санкт-Петербурге 295 случаев заражения COVID-19. Выздоровело 36 человек. Умерло 3* человека.

За последние сутки в Петербурге обследовано на коронавирус 6957 человек.

🏠 На карантине находится 8917 человек. Из них 35 - в обсерваторе, 7987 - на самоизоляции. 
___

📞 В службе экстренных вызовов 112 зарегистрировано 1356 обращений. О прибытии из другой страны на территорию России сообщил 71 человек. В Городскую службу скорой помощи направлено 125 обращений, в полицию - 123. Остальные звонки были справочного характера.

* - по одной из смертей проводится проверка."""


        self.msg_dec15 = """Картина дня 15 декабря
 
➕ Зафиксировано 3758 новых случаев заражения коронавирусной инфекцией.

📉 Всего с начала пандемии в Санкт-Петербурге  185780 случаев заражения COVID-19. 
Скончались 6529 человек. Выздоровело 105665 человек.

🔬 За последние сутки в Петербурге обследовали на коронавирус 35 593 человека.

🏠 Под медицинским наблюдением находится 1782 человека. Из них 15 - в обсерваторе, 1274 - контактные, 493 - на самоизоляции."""

    def test_apr6_cases(self):
        p = SpbCovidMsgParser()
        result = p.parse_cases(self.msg_apr6)
        self.assertEqual("6 АПРЕЛЯ", result["date"])
        self.assertEqual("69", result["new_cases"])
        self.assertEqual("295", result["total_cases"])

    def test_apr6_tested(self):
        p = SpbCovidMsgParser()
        result = p.parse_tested(self.msg_apr6)
        self.assertEqual("6957", result["tested"])

    def test_apr6_cured_died(self):
        p = SpbCovidMsgParser()
        result = p.parse_cured_died(self.msg_apr6)
        self.assertEqual("36", result["cured"])
        self.assertEqual("3", result["died"])

    def test_nov11_cases(self):
        p = SpbCovidMsgParser()
        result = p.parse_cases(self.msg_nov8)

        self.assertEqual("1403", result["new_cases"])

    def test_nov8_cases(self):
        p = SpbCovidMsgParser()
        result = p.parse_cases(self.msg_nov8)

        self.assertEqual("8 ноября", result["date"])
        self.assertEqual("1403", result["new_cases"])
        self.assertEqual("71426", result["total_cases"])

    def test_nov8_tested(self):
        p = SpbCovidMsgParser()
        result = p.parse_tested(self.msg_nov8)
        self.assertEqual("25651", result["tested"])


    def test_nov8_cured_died(self):
        p = SpbCovidMsgParser()
        result = p.parse_cured_died(self.msg_nov8)
        self.assertEqual("43501", result["cured"])
        self.assertEqual("4181", result["died"])

    def test_aug10_cases(self):
        p = SpbCovidMsgParser()
        result = p.parse_cases(self.msg_aug10)

        self.assertEqual("157", result["new_cases"])


    def test_apr12_cases(self):
        p = SpbCovidMsgParser()
        result = p.parse_cases(self.msg_apr12)
        self.assertEqual("12 АПРЕЛЯ", result["date"])
        self.assertEqual("121", result["new_cases"])
        self.assertEqual("678", result["total_cases"])

    def test_apr12_cured_died(self):
        p = SpbCovidMsgParser()
        result = p.parse_cured_died(self.msg_apr12)
        self.assertEqual("78", result["cured"])
        self.assertEqual("4", result["died"])

    def test_apr22_cases(self):
        p = SpbCovidMsgParser()
        result = p.parse_cases(self.msg_apr22)
        self.assertEqual("22 АПРЕЛЯ", result["date"])
        self.assertEqual("191", result["new_cases"])
        self.assertEqual("2458", result["total_cases"])

    def test_apr22_cured_died(self):
        p = SpbCovidMsgParser()
        result = p.parse_cured_died(self.msg_apr22)
        self.assertEqual("368", result["cured"])
        self.assertEqual("17", result["died"])

    def test_apr22_tested(self):
        p = SpbCovidMsgParser()
        result = p.parse_tested(self.msg_apr22)
        self.assertEqual("8196", result["tested"])

    def test_apr12_parse(self):
        p = SpbCovidMsgParser()
        result = p.parse(self.msg_apr12)
        self.assertEqual("12 АПРЕЛЯ", result["date"])
        self.assertEqual("121", result["new_cases"])
        self.assertEqual("678", result["total_cases"])
        self.assertEqual("78", result["cured"])
        self.assertEqual("4", result["died"])


    def test_dec15_parse(self):
        p = SpbCovidMsgParser()
        result = p.parse(self.msg_dec15)
        self.assertEqual("15 декабря", result["date"])
        self.assertEqual("3758", result["new_cases"])
        self.assertEqual("185780", result["total_cases"])
        self.assertEqual("6529", result["died"])
        self.assertEqual("105665", result["cured"])
        self.assertEqual("35593", result["tested"])

    def test_regex_replace(self):
        def space_repl(match):
            return match.group().replace(" ", "")

        import re
        str = re.sub(r"\d+( )\d+", space_repl, "aaa 444 33 sss")
        self.assertEqual("aaa 44433 sss", str)

if __name__ == '__main__':
    unittest.main()
