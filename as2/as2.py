from HMM import *
from Viterbi import *


def read_file(txt):
    txt_array = []
    with open(txt, "r") as fileHandler:
        for line in fileHandler:
            txt_array.append(line.strip())
    length = len(txt_array)
    train_bound = round(length * 0.7)
    trainList = txt_array[0:train_bound - 1]
    testList = txt_array[train_bound - 1:]
    return trainList, testList


def prep(data_set):
    originals = []
    sentences = []
    tags = []
    for i in range(len(data_set)):
        sentence = []
        original = []
        tag = []
        for j in range(len(data_set[i].split())):
            temp1 = data_set[i].split()[j].split("/")[0].lower()
            temp = data_set[i].split()[j].split("/")[0]
            temp2 = data_set[i].split()[j].split("/")[1]
            sentence.append(temp1)
            tag.append(temp2)
            original.append(temp)
        sentences.append(sentence)
        tags.append(tag)
        originals.append(original)
    return sentences, tags, originals


def predict(dataset, emission_dict, transition, corpus):
    prediction_list = []
    for i in range(len(dataset)):
        prediction_list.append(viterbi(dataset[i], emission_dict, transition, corpus))
    return prediction_list


def evaluation(tags, predictions):
    correctness = 0
    total_words = 0
    for i in range(len(tags)):
        for j in range(len(tags[i])):
            total_words += 1
            if tags[i][j] == predictions[i][j]:
                correctness += 1
        accuracy = round((correctness/total_words) * 100)
    print("Accuracy: "+str(accuracy)+"%")


def rewrite(prediction, test):
    f = open("output.txt", "w+")
    for i in range(len(test)):
        sentence = ""
        for j in range(len(test[i])):
            token = test[i][j]+"/"+prediction[i][j]
            sentence += " "
            sentence += token
        f.write(sentence+"\n")
    f.close()


# TASK 1: BUILD HMM
train, test = read_file("metu.txt")
# Initial Probability
corpus_tag = transition_prob(train, 1)
# Transition Probability
transition_probability_bi = transition_prob(train, 2)
# Emission Probabilities
raw_emissions = emision_prob(train)
emission_dict = re_organize(raw_emissions)
# TASK 2: VITERBI
test_list, tag_list, orginals = prep(test)
predictions = predict(test_list, emission_dict, transition_probability_bi, corpus_tag)
# Predictions
rewrite(predictions, orginals)
# TASK 3: EVALUATION
evaluation(tag_list, predictions)
