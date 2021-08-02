import dynet as dy
import nltk
import numpy as np
import random


def train_model(poems, hot_vectors, hidden_size, epoches):
    model = dy.Model()

    # Initializing of variables
    W = model.add_parameters((hidden_size, len(hot_vectors.keys())))
    U = model.add_parameters((len(hot_vectors.keys()), hidden_size))
    b = model.add_parameters(hidden_size)
    d = model.add_parameters(len(hot_vectors.keys()))
    # SGD
    trainer = dy.SimpleSGDTrainer(model)
    for epoch in range(epoches):
        random.shuffle(poems)
        for key in range(5000):
            print(key)
            epoch_loss = 0
            sequence = list(nltk.bigrams(poems[key]))
            for i in range(len(sequence)):

                prediction = feed_forward(sequence[i], hot_vectors, W, U, b, d)
                # target value: next word vector
                target = dy.softmax(dy.inputVector((hot_vectors[sequence[i][1]])[0]))
                # Optimization
                prediction_opt = dy.softmax(prediction)
                # Cross-Entropy
                loss = do_loss(prediction_opt, target)
                epoch_loss += loss.value()
                loss.backward()
                trainer.update()
        print("Epoch %d. loss = %f" % (epoch, epoch_loss))
    # save model
    model.save("tmp.model")


def feed_forward(sequence, hot_vectors, W, U, b, d):
    dy.renew_cg()
    x = dy.inputVector((hot_vectors[sequence[0]])[0])
    hidden_value = dy.tanh(W * x + b)
    y = U * hidden_value + d
    return y


def do_loss(prediction, target):

    index = np.argmin(target.value())
    loss = -dy.log(dy.pick(prediction, index))
    return loss


