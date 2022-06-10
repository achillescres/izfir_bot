import string
import pandas as pd
import pymorphy2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

from bot.data.config import PROJECT_ROOT

morph = pymorphy2.MorphAnalyzer()


def hook_answer(question: str):
    ans = None

    ans = classify(question)

    return ans if ans else 'err'


def classify(question: str):
    def lemmatize(text):
        text = str(text)
        words = text.split()  # разбиваем текст на слова
        res = []
        for word in words:
            p = morph.parse(word)[0]
            res.append(p.normal_form)
        return " ".join(res)

    # Удаление символов пунктуации
    def remove_punctuation(text):
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    def normalize_text(text):
        return lemmatize(text)

    text = question
    df: pd.DataFrame = pd.read_excel(f'{PROJECT_ROOT}/nlp/izfir.xlsx')
    df['lemmatized_text'] = df['Context'].apply(normalize_text)
    tfidf = TfidfVectorizer()
    x_tfidf = tfidf.fit_transform(
        df['lemmatized_text'].values.dropna().astype('U')
    ).toarray()

    df_tfidf = pd.DataFrame(x_tfidf, columns=tfidf.get_feature_names_out())

    def chat_tfidf(text):
        lemma = lemmatize(remove_punctuation(text))
        tf = tfidf.transform([lemma]).toarray()
        cos = 1 - pairwise_distances(df_tfidf, tf, metric='cosine')
        index_value = cos.argmax()
        return df['Answer'].loc[index_value]

    return chat_tfidf(text)


ans = hook_answer('Каковы вступительные испытания на программу бакалавриата «Зарубежное регионоведение. Американские исследования»')
print(ans)
