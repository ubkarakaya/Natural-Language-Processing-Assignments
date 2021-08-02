
import math
import operator


def viterbi(word_list, emission_dict, transition, corpus_tag):
    start = {"<s>": 0}
    e_prob = [start]
    tags = sorted(corpus_tag.keys())[2:]
    # Emission Block
    for i in range(len(word_list)):
        # if data is unseen the dictionary is added normally
        seen = {}
        for j in range(len(tags)):
            seen[tags[j]] = math.log(1 / sum(corpus_tag.values()))
        if word_list[i] in emission_dict.keys():
            for key, value in emission_dict[word_list[i]].items():
                seen[key] = math.log((value + 1) / (corpus_tag[key] + sum(corpus_tag.values())))

        e_prob.append(seen)
    stop = {"<s>": 0}
    e_prob.append(stop)
    # Calculation
    prediction = []
    for i in range(len(e_prob) - 1):
        main_dct = {}
        for key1, value1 in e_prob[i].items():
            tag_level = {}
            for key2, value2 in e_prob[i + 1].items():
                # seen transition tags
                if create_key(key1, key2) in transition.keys():

                    total = math.log((transition[create_key(key1, key2)] + 1) / (corpus_tag[key1]) +
                                     sum(corpus_tag.values())) + value2 + value1
                    tag_level[key2] = total
                # unseen transition tags
                else:
                    total = math.log(1 / (corpus_tag[key1]) + sum(corpus_tag.values())) + value2 + value1
                    tag_level[key2] = total

            main_dct[key1] = tag_level
        if i > 0:
            max_item = back_trace(main_dct)
            e_prob[i + 1] = main_dct[max_item]
            prediction.append(max_item)
    return prediction


def back_trace(tags):
    max_key = {}
    for key, value in tags.items():
        max_key[key] = sum(tags[key].values())
    predict = max(max_key.items(), key=operator.itemgetter(1))[0]
    return predict


def create_key(a, b):
    key = a + " " + b
    return key

