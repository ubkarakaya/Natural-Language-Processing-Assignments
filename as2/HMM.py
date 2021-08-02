from Word import*
from collections import Counter


def ngrams(words, n):
    ngram_list = []

    for i in range(len(words)):
        ngram = ' '.join(words[i:i + n])
        ngram_list.append(ngram)
        
    return ngram_list


def transition_prob(data_set, n):
    t_prob = []
    for i in range(len(data_set)):
        tags = ["<s>"]
        for j in range(len(data_set[i].split())):
            tag = data_set[i].split()[j].split("/")[1]
            tags.append(tag)
        tags.append("</s>")
        t_prob.extend(ngrams(tags, n))
    return dict(Counter(t_prob))


def emision_prob(data_set):

    words = []
    for i in range(len(data_set)):
        for j in range(len(data_set[i].split())):
            temp = Word(data_set[i].split()[j].split("/")[0].lower(), data_set[i].split()[j].split("/")[1])
            words.append(temp)
    return words


def re_organize(emissions):
    # emission probabilities
    ee = {}

    for i in range(len(emissions)):
        if emissions[i].name not in ee.keys():
            ee.setdefault(emissions[i].name, [])
            ee[emissions[i].name].append(emissions[i].tags)
        else:
            ee[emissions[i].name].append(emissions[i].tags)

    for key, value in ee.items():
        ee[key] = dict(Counter(value))

    return ee

