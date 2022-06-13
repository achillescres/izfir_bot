import string
import pandas as pd
import pymorphy2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

from data.config import BOT_ROOT

morph = pymorphy2.MorphAnalyzer()

print(BOT_ROOT + '/nlp/izfir.xlsx')
df = pd.read_excel(BOT_ROOT + '/nlp/izfir.xlsx')


def get_answer(question):
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

    df['lemmatized_text'] = df['Context'].apply(normalize_text)
    tfidf = TfidfVectorizer()
    x_tfidf = tfidf.fit_transform(
        df['lemmatized_text'].values.astype('U')
    ).toarray()
    df_tfidf = pd.DataFrame(x_tfidf, columns=tfidf.get_feature_names_out())

    def chat_tfidf(text):
        lemma = lemmatize(remove_punctuation(text))
        tf = tfidf.transform([lemma]).toarray()
        cos = 1 - pairwise_distances(df_tfidf, tf, metric='cosine')
        index_value = cos.argmax()
        return df['Answer'].loc[index_value]

    return chat_tfidf(text)


def hook_answer(question):
    ans = None
    try:
        ans = get_answer(question)
    finally:
        pass

    return ans if ans else 'err'


if __name__ == '__main__':
    print(get_answer('Какая стоимость обучения бакалавриата'))
