import spacy

class TextAnalyser:
    __nlp = spacy.load('ru_core_news_sm')

    def __get_auction_file_text_name(self, text):
        text = text.split('.')[:10]


    def get_sentences_similarity(self, str1, str2):
        doc1 = self.__nlp(str1)
        doc2 = self.__nlp(str2)
        return doc1.similarity(doc2)