import gensim.models.keyedvectors as word2vec
from Relation import *
import re
import numpy as np
import operator


def load_model(path):
    model = word2vec.KeyedVectors.load_word2vec_format(path, binary=True)

    return model


def calculate_cosine(a, b):
    dot = np.dot(a, b)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    cos = dot / (norma * normb)
    return cos


def read_relations(path):
    regex = re.compile(r'[\n\r\t]')
    lines = open(path, "r")
    relations = []
    words = []
    for line in lines:
        if ":" in line:
            line = regex.sub(" ", line)
            relations.append(line.split(":")[1])
        elif "//" not in line:
            line = regex.sub("", line)
            items = line.split(" ")
            new_r = Relation(items[0], items[1], items[2], items[3], relations[-1])
            words.append(new_r)

    return words


def prediction(model, words):
    correctness = 0
    for i in range(len(words)):
        predictions = {}
        check = []
        v_a = model[words[i].word1]
        check.append(words[i].word1)
        v_b = model[words[i].word2]
        check.append(words[i].word2)
        v_c = model[words[i].word3]
        check.append(words[i].word3)
        # arithmetic operation
        v_d = v_b - v_a + v_c

        for key in model.vocab:
            if key not in check:
                predictions[key] = calculate_cosine(v_d, model[key])
        predict = max(predictions.items(), key=operator.itemgetter(1))[0]
        print("Prediction: "+predict+" Target: "+words[i].word4)
        if predict == words[i].word4:
            correctness += 1

    print("Accuracy of the analogy is " + str(((correctness / len(words)) * 100)) + "%")
