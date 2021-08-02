import string
from collections import Counter
from random import *
import math
import re


def detect_sentence(text):
    sentence = re.compile('([a-zA-Z][^\.!?]*[\.!?])')
    x = sentence.split(text)
    x.remove(" ")
    x.remove("")
    for i in range(len(x)):
        x[i] = "<s> " + x[i] + " </s>"
    str2 = " ".join(x)
    return str2


def preprocessing(text):
    # detection of punctuations and adding to the list as a new item
    eos = re.compile('["]?[a-zA-Z]{2,}[.?!,;:\'"]$')
    for i in range(len(text)):
        if eos.match(text[i]):
            punc = text[i][-1]
            text[i] = text[i][:-1]
            text.insert(i + 1, punc)
    return text


def read_files():
    # initialize the essay numbers which will be used for tasks #
    hamilton = [1, 6, 7, 8, 13, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    madison = [10, 14, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]
    hamilton_test = [9, 11, 12]
    madison_test = [47, 48, 58]
    test_set = [49, 50, 51, 52, 53, 54, 55, 56, 57, 62, 63]
    ds_hamilton = []
    ds_madison = []
    ds_ht = []
    ds_mt = []
    ds_test = []

    for i in range(len(hamilton)):
        with open("data/" + str(hamilton[i]) + ".txt") as f:
            content1 = f.read().splitlines()
            text1 = preprocessing(detect_sentence(content1[1]).split())
            content = " ".join(text1)
            ds_hamilton.append(content.lower())

    for i in range(len(madison)):
        with open("data/" + str(madison[i]) + ".txt") as f:
            content2 = f.read().splitlines()
            text2 = preprocessing(detect_sentence(content2[1]).split())
            content_m = " ".join(text2)
            ds_madison.append(content_m.lower())

    for i in range(len(test_set)):
        with open("data/" + str(test_set[i]) + ".txt") as f:
            content3 = f.read().splitlines()
            text3 = preprocessing(detect_sentence(content3[1]).split())
            content_t = " ".join(text3)
            ds_test.append(content_t.lower())

    for i in range(len(hamilton_test)):
        with open("data/" + str(hamilton_test[i]) + ".txt") as f:
            content4 = f.read().splitlines()
            text4 = preprocessing(detect_sentence(content4[1]).split())
            content_ht = " ".join(text4)
            ds_ht.append(content_ht.lower())

    for i in range(len(madison_test)):
        with open("data/" + str(madison_test[i]) + ".txt") as f:
            content5 = f.read().splitlines()
            text5 = preprocessing(detect_sentence(content5[1]).split())
            content_mt = " ".join(text5)
            ds_mt.append(content_mt.lower())

    return ds_hamilton, ds_madison, ds_test, ds_ht, ds_mt


def ngrams(words, n):
    ngram_list = []

    for i in range(len(words)):
        ngram = ' '.join(words[i:i + n])
        ngram_list.append(ngram)

    return ngram_list


def generate_ngrams(ds_hamilton, ds_madison):
    # unigram
    unigramH = []
    unigramM = []
    # bigram
    bigramH = []
    bigramM = []
    # trigram
    trigramH = []
    trigramM = []

    for i in range(len(ds_hamilton)):
        unigramH.extend(ngrams(ds_hamilton[i].split(), 1))
        bigramH.extend(ngrams(ds_hamilton[i].split(), 2))
        trigramH.extend(ngrams(ds_hamilton[i].split(), 3))
    hamilton_unigram = dict(Counter(unigramH))
    hamilton_bigram = dict(Counter(bigramH))
    hamilton_trigram = dict(Counter(trigramH))
    for i in range(len(ds_madison)):
        unigramM.extend(ngrams(ds_madison[i].split(), 1))
        bigramM.extend(ngrams(ds_madison[i].split(), 2))
        trigramM.extend(ngrams(ds_madison[i].split(), 3))
    madison_unigram = dict(Counter(unigramM))
    madison_bigram = dict(Counter(bigramM))
    madison_trigram = dict(Counter(trigramM))
    hamiltonlist = [hamilton_unigram, hamilton_bigram, hamilton_trigram]
    madisonlist = [madison_unigram, madison_bigram, madison_trigram]
    return hamiltonlist, madisonlist


def calculate_probability_unigram(essay, author):
    total_prob = 0
    for i in range(len(essay)):
        total_prob += math.log(author[essay[i]] / sum(author.values()))
    str1 = ' '.join(essay)
    print_essay(str1.strip())
    print(total_prob)


def calculate_probability_bigram(essay, author):
    total_prob = 0
    for i in range(len(essay)):
        x = author[0][essay[i].split()[0]]
        y = author[1][essay[i]]
        total_prob += math.log(y / x)
    str2 = ' '.join(essay)
    print_essay(str2.strip())
    print(total_prob)


def calculate_probability_trigram(essay, author):
    total_prob = 0
    for i in range(len(essay)):
        keys = essay[i].split()
        str1 = ' '.join(keys[:2])
        x = author[1][str1]
        y = author[2][essay[i]]
        total_prob += math.log(y / x)
    str2 = ' '.join(essay)
    print_essay(str2.strip())
    print(total_prob)


def print_essay(text):
    punc = ['.', ';', ':', '!', '?', ',']
    # remove end and start tokens from text
    txt = re.sub("<s>|</s>", "", text)
    if txt[0] in punc:
        print(txt[1:].strip().capitalize())
    else:
        print(txt.capitalize())


def generate_essay(author, n):
    i = 0
    cl = []
    words = []
    essay = []
    for key, value in author[n - 1].items():
        i += value
        words.append(key)
        cl.append(i)
    length = round(30 / n)
    for i in range(length):
        point = randint(1, sum(author[n - 1].values()))
        ind = min(cl, key=lambda x: abs(x - point))
        essay.append(words[cl.index(ind)])
    if n == 1:
        calculate_probability_unigram(essay, author[n - 1])
    elif n == 2:
        calculate_probability_bigram(essay, author)
    elif n == 3:
        calculate_probability_trigram(essay, author)


def testing(author, test_set, n):
    results = []
    for i in range(len(test_set)):
        sample = ngrams(test_set[i].split(), n)
        results.append(calculate_perplexity(author, sample, n))
    return results


def calculate_perplexity(author, test, n):
    total_prob = 0
    y = -1
    x = -1
    for i in range(len(test)):
        if test[i] not in author[n - 1].keys():
            y = 0
        else:
            y = author[n - 1][test[i]]
        if n == 2:
            if test[i].split()[0] not in author[n - 2].keys():
                x = 0
            else:
                x = author[n - 2][test[i].split()[0]]
        elif n == 3:
            str2 = ' '.join(test[i].split()[:2])
            if str2 not in author[n - 2].keys():
                x = 0
            else:
                x = author[n - 2][str2]
        # add-one smoothing
        total_prob += math.log((y + 1) / (x + len(author[n - 2].keys())))
    pp = -total_prob / len(author[n - 1].keys())
    perplexity = 2 ** pp
    return perplexity


def detection(author1, author2, test_set):
    hamilton_results_bi = testing(author1, test_set, 2)
    hamilton_results_tri = testing(author1, test_set, 3)
    madison_results_bi = testing(author2, test_set, 2)
    madison_results_tri = testing(author2, test_set, 3)
    for i in range(11):
        prediction = min(hamilton_results_bi[i], hamilton_results_tri[i], madison_results_bi[i], madison_results_tri[i])
        if prediction == hamilton_results_tri[i]:
            print(str(i + 1) + ".text belongs to Hamilton")
        elif prediction == madison_results_tri[i]:
            print(str(i + 1) + ".text belongs to Madison")


ds_hamilton, ds_madison, ds_test, ds_ht, ds_mt = read_files()
# Task1
hamilton, madison = generate_ngrams(ds_hamilton, ds_madison)
# Task2
for k in range(2):
    print("\n UNIGRAM GENERATION \n")
    print(" Hamilton: ")
    generate_essay(hamilton, 1)
    print(" Madison: ")
    generate_essay(madison, 1)
    print("\n BIGRAM GENERATION\n")
    print(" Hamilton :")
    generate_essay(hamilton, 2)
    print(" Madison: ")
    generate_essay(madison, 2)
    print("\n TRIGRAM GENERATION\n")
    print(" Hamilton :")
    generate_essay(hamilton, 3)
    print(" Madison: ")
    generate_essay(madison, 3)
# Task3-1
print("\n Perplexities of Hamilton in its testset \n")
print("Bigram:")
print(testing(hamilton, ds_ht, 2))
print("\nTrigram:")
print(testing(hamilton, ds_ht, 3))
print("\n Perplexities of Madison in its testset \n")
print("Bigram:")
print(testing(madison, ds_mt, 2))
print("\nTrigram:")
print(testing(madison, ds_mt, 3))
# Task3-2
print("\n Prediction of Unknown Essays")
detection(hamilton, madison, ds_test)
