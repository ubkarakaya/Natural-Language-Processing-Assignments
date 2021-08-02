import json
import numpy as np
from collections import Counter
import fnn
import generation
import dynet as dy


def read_parse(path):
    corpus = []
    poems ={}
    with open(path) as f:
        data = json.load(f)
    for j in range(len(data)):
        start=[]
        #start = ["<s>"]
        #corpus.append("<s>")
        rows = data[j]["poem"].split("\n")
        for i in range(len(rows)):
            corpus.extend(rows[i].split(" "))
            start.extend(rows[i].split(" "))
            if i < len(rows) - 1:
                corpus.append("\n")
                start.append("\n")

        #corpus.append("</s>")
        #start.append("</s>")
        poems[j] = start

    return poems, data, corpus, Counter(corpus)


def create_one_hot(unique):
    hot_vectors = {}
    index_words = {}
    index = 0
    for key in unique.keys():
        one_hot_vector = np.zeros([1, len(unique.keys())])
        one_hot_vector[0][index] = 1
        hot_vectors[key] = one_hot_vector
        index_words[index] = key
        index += 1
    return index_words,hot_vectors


# read dataset
poems, data, corpus, uniques = read_parse('unim_poem.json')
# hot-one vectors
index_words_dict, hot_vectors_dict = create_one_hot(uniques)
# TASK-I
fnn.train_model(poems, hot_vectors_dict, 100, 1)
# TASK-II
#generation.generation_poem(index_words_dict, hot_vectors_dict, 100)
