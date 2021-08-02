import string
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.corpus import stopwords
import multiprocessing
from sklearn.linear_model import LogisticRegression
from sklearn import utils
from sklearn.metrics import accuracy_score
from nltk.stem import LancasterStemmer


def read_parse(path):
    data = pd.read_csv(path)
    # Elimination of empty elements
    train_df = data[:2000].dropna()
    test_df = data[2000:].dropna()
    return train_df, test_df


# Stop Words, Suffix, Punctuation
def tokenize_text(text):
    lancaster = LancasterStemmer()
    stopWords = set(stopwords.words('english'))
    tokens = []
    words = text.split(" ")
    for i in range(len(words)):
        if not words[i].lower() in stopWords:
            tokens.append(lancaster.stem(words[i].lower()).translate(str.maketrans('', '', string.punctuation)))
    return tokens


def generate_model(df):
    data_set = []
    tags_dict = {"sci-fi": 1, "action": 2, "comedy": 3, "fantasy": 4, "animation": 5, "romance": 6}
    for index, row in df.iterrows():
        data_set.append(TaggedDocument(words=tokenize_text(row["plot"]), tags=[tags_dict[row["tag"]]]))

    cores = multiprocessing.cpu_count()
    model = Doc2Vec(dm=1, vector_size=300, negative=5, hs=0, min_count=2, sample=0, workers=cores, alpha=0.025,
                    min_alpha=0.01)
    model.build_vocab(data_set)
    return model, data_set


def create_vector(model, documents):

    targets, feature_vectors = zip(*[(document.tags[0], model.infer_vector(document.words, steps=20))
                                     for document in documents])
    return targets, feature_vectors


def evaluation(model, train_set, test_set):

    # shuffle
    train_documents = utils.shuffle(train_set)
    model.train(train_documents, total_examples=len(train_documents), epochs=10)
    train_result, train = create_vector(model, train_set)
    test_result, test = create_vector(model, test_set)

    # Logistic Regression
    log_reg = LogisticRegression(random_state=0, solver='sag', multi_class='multinomial')
    log_reg.fit(train, train_result)
    test_prediction = log_reg.predict(test)
    accuracy = accuracy_score(test_result, test_prediction)
    print('Accuracy of the model is ' + str(round(100 * accuracy)) + " %")
    return round(100 * accuracy)
