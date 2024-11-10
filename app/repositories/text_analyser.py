import spacy
from app.repositories.file import FileRepository
import asyncio


class TextAnalyser:
    __nlp = spacy.load('ru_core_news_sm')

    __WORD_BEGINNINGS = "abcdefghijkmnlopqrstuvwxyz0123456789абвгдеёжзийклмнопрстуфхцчщшъыьэюя"

    def __get_text_lemmas(self, text):
        text = text.lower().replace("\n", " ")
        text_set = set(text)
        for ch in set(text_set):
            if ch not in self.__WORD_BEGINNINGS:
                text = text.replace(ch, " ")
        while "  " in text:
            text = text.replace("  ", " ")

        text_lemmas = []
        text_tokens = self.__nlp(text)
        for token in text_tokens:
            text_lemmas += [token.lemma_]
        return text_lemmas

    def __get_lemma_lists_intersection(self, lemmas1, lemmas2):
        lemmas1_set = set(lemmas1)
        lemmas2_set = set(lemmas2)
        intersection = lemmas1_set.intersection(lemmas2_set)
        return intersection

    def get_auction_name(self, text: str, is_tz: bool, auction_real_name):
        auction_real_name_lemmas = self.__get_text_lemmas(auction_real_name)

        text = text[: min(len(text), 500)].lower()
        KEYWORDS = ['техническое задание', 'тз', 'техническое_задание']
        start_searching_index = 0
        for key in KEYWORDS:
            start_searching_index = max(start_searching_index, text.find(key) + len(key))
        text = text[start_searching_index:]

        while text[0] not in self.__WORD_BEGINNINGS:
            text = text[1:]

        text_array = text.split(" ")
        intersection_best = set()
        for i in range(len(text_array)):
            for j in range(i+2, min(len(text_array), i+15)):
                text_curr = ' '.join(text_array[i:j+1])
                text_lemmas = self.__get_text_lemmas(text_curr)
                intersection = self.__get_lemma_lists_intersection(text_lemmas, auction_real_name_lemmas)
                intersection_best = max(intersection, intersection_best, key=len)
        print(intersection_best)
        return '', 0

    def __prepare_string(self, text: str):
        text = text.lower()
        str_set = set(text)
        for ch in str_set:
            if ch not in self.__WORD_BEGINNINGS:
                text = text.replace(ch, " ")
        while "  " in text:
            text = text.replace("  ", " ")
        while text[0] not in self.__WORD_BEGINNINGS:
            text = text[1:]
        while text[-1] not in self.__WORD_BEGINNINGS:
            text = text[:-1]
        return text

    def get_auction_name_simple(self, text: str, is_tz: bool, auction_real_name):
        text = text[: min(len(text), 500)].lower()
        if is_tz:
            KEYWORDS = ['техническое задание', 'тз', 'техническое_задание']
            start_searching_index = 0
            for key in KEYWORDS:
                start_searching_index = max(start_searching_index, text.find(key) + len(key))
            text = text[start_searching_index:]
        else:
            KEYWORDS = ['гражданско правовой договор', 'гражданско_правовой_договор', 'проект_договора', 'договор бюджетного учреждения']
            start_searching_index = 0
            for key in KEYWORDS:
                start_searching_index = max(start_searching_index, text.find(key) + len(key))
            text = text[start_searching_index:]

        while text[0] not in self.__WORD_BEGINNINGS:
            text = text[1:]

        end_index = min(text.find('.'), text.find('\n'), len(text))
        text = text[:end_index]
        auction_real_name_formatted = self.__prepare_string(auction_real_name)
        return text, self.__get_sentences_similarity(text, auction_real_name_formatted)

    def __get_sentences_similarity(self, str1, str2):
        doc1 = self.__nlp(str1)
        doc2 = self.__nlp(str2)
        return doc1.similarity(doc2)

    def test_contract_files(self):
        CONTRACT_LIST = [
            "232480290",
            "232492123",
            "232498799",
            "232507116",
            "232508272",
            "232509211",
            "232520280",
            "232178142",
            "232170711",
            "232168697"
        ]
        AUCTION_NAME_LIST = [
            "ЗАПАСНЫЕ ЧАСТИ ДЛЯ ТРАНСПОРТНЫХ СРЕДСТВ",
            "ОДЕЖДА СПЕЦИАЛЬНАЯ ДЛЯ ЗАЩИТЫ ОТ ИСКР И БРЫЗГ РАСПЛАВЛЕННОГО МЕТАЛЛА",
            "ОДЕЖДА (ВКЛЮЧАЯ ФОРМЕННУЮ), ОБУВЬ, ГАЛАНТЕРЕЯ, ГОЛОВНЫЕ УБОРЫ",
            "МЕБЕЛЬ УЧЕНИЧЕСКАЯ",
            "ЗАПАСНЫЕ ЧАСТИ ДЛЯ ТРАНСПОРТНЫХ СРЕДСТВ",
            "ОБУВЬ",
            "Вода питьевая Аква Лига ЛЮКС Фарватер 18,9л",
            "ОДЕЖДА (ВКЛЮЧАЯ ФОРМЕННУЮ), ОБУВЬ, ГАЛАНТЕРЕЯ, ГОЛОВНЫЕ УБОРЫ",
            "Сканер штрих-кода 2D АТОЛ SB2108 Plus USB",
            "Шпагат джутовый 1,5 ктекс, 1 кг/боб."
        ]
        handler = FileRepository()
        for i, id in enumerate(CONTRACT_LIST):
            result = asyncio.run(handler.handle_file(id))
            if result is None:
                print("for id", id, "result is none!")
                continue
            name, similarity = self.get_auction_name_simple(result.text, result.is_TZ, AUCTION_NAME_LIST[i])
            print(name)
            print(similarity)


    def test_tz_files(self):
        TZ_LIST = [
            '232480287',
            '232492125',
            '232498803',
            '232507119',
            '232508260',
            '232509229',
            '232520279',
            '232178164',
            '232170708',
            '232168690'
        ]
        AUCTION_NAME_LIST = [
            "ЗАПАСНЫЕ ЧАСТИ ДЛЯ ТРАНСПОРТНЫХ СРЕДСТВ",
            "ОДЕЖДА СПЕЦИАЛЬНАЯ ДЛЯ ЗАЩИТЫ ОТ ИСКР И БРЫЗГ РАСПЛАВЛЕННОГО МЕТАЛЛА",
            "ОДЕЖДА (ВКЛЮЧАЯ ФОРМЕННУЮ), ОБУВЬ, ГАЛАНТЕРЕЯ, ГОЛОВНЫЕ УБОРЫ",
            "МЕБЕЛЬ УЧЕНИЧЕСКАЯ",
            "ЗАПАСНЫЕ ЧАСТИ ДЛЯ ТРАНСПОРТНЫХ СРЕДСТВ",
            "ОБУВЬ",
            "Вода питьевая Аква Лига ЛЮКС Фарватер 18,9л",
            "ОДЕЖДА (ВКЛЮЧАЯ ФОРМЕННУЮ), ОБУВЬ, ГАЛАНТЕРЕЯ, ГОЛОВНЫЕ УБОРЫ",
            "Сканер штрих-кода 2D АТОЛ SB2108 Plus USB",
            "Шпагат джутовый 1,5 ктекс, 1 кг/боб."
        ]
        handler = FileRepository()
        for i, id in enumerate(TZ_LIST):
            result = asyncio.run(handler.handle_file(id))
            if result is None:
                print("for id", id, "result is none!")
                continue
            name, similarity = self.get_auction_name_simple(result.text, result.is_TZ, AUCTION_NAME_LIST[i])
            print(name)
            print(similarity)
