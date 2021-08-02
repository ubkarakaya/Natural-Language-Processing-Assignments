import random
import dynet as dy
import numpy as np


def generation_poem(words, hot_vectors, hidden_size):
    # load the model
    model = dy.Model()
    W = model.add_parameters((hidden_size, len(hot_vectors.keys())))
    U = model.add_parameters((len(hot_vectors.keys()), hidden_size))
    b = model.add_parameters(hidden_size)
    d = model.add_parameters(len(hot_vectors.keys()))
    model.populate("tmp.model")
    # start token
    point = random.randint(0, len(hot_vectors.keys()))
    print(words[point])
    predict(hot_vectors[words[point]], words, hot_vectors, W, U, b, d)


def predict(input_x, words, hot_vectors, W, U, b, d):
    dy.renew_cg()
    x = dy.inputVector((input_x)[0])
    hidden_value = dy.tanh(W * x + b)
    y = dy.softmax(U * hidden_value + d)
    a = np.array(y.value())
    idx = np.argmax(a)
    print(words[idx])
    predict(hot_vectors[words[idx]], words, hot_vectors, W, U, b, d)

