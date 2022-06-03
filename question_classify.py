import string
import pandas as pd
#from pymystem3 import Mystem
import pymorphy2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

#m = Mystem()
morph = pymorphy2.MorphAnalyzer()


# def diction_form(text):
#     text = ''.join(m.lemmatize(text)).rstrip('\n')
#     return text
def getAnswer(question):
    def lemmatize(text):
        text = str(text)
        words = text.split()  # разбиваем текст на слова
        res = []
        for word in words:
            p = morph.parse(word)[0]
            res.append(p.normal_form)
        return " ".join(res)
    # print(diction_form("На какие программы проходит набор в бакалавриат в 2022г.?"))

    # Удаление символов пунктуации

    def remove_punctuation(text):
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    def normalize_text(text):
        return lemmatize(text)

    # text = 'На какие программы осуществляется/будет/проходит набор в бакалавриат в 2022г.?'
    text = question
    # print(lemmatize(text))
    df = pd.read_excel('izfir.xlsx')
    df['lemmatized_text'] = df['Context'].apply(normalize_text)
    # df.to_excel("izfir1.xlsx")
    tfidf = TfidfVectorizer()
    x_tfidf = tfidf.fit_transform(
        df['lemmatized_text'].values.astype('U')).toarray()
    df_tfidf = pd.DataFrame(x_tfidf, columns=tfidf.get_feature_names_out())

    def chat_tfidf(text):
        lemma = lemmatize(remove_punctuation(text))
        tf = tfidf.transform([lemma]).toarray()
        cos = 1 - pairwise_distances(df_tfidf, tf, metric='cosine')
        index_value = cos.argmax()
        return df['Answer'].loc[index_value]

    return chat_tfidf(text)
