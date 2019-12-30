""" This module prepares midi file data and feeds it to the neural
    network for training """
import numpy
from music21 import converter, instrument, note, chord
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import BatchNormalization as BatchNorm
from keras.layers import Activation


def vocab_size (items):
    return len(set(items))


def get_item_names (items):
    return  sorted(set(item for item in items))


def create_network(network_input, n_vocab):
    """ create the structure of the neural network """
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        recurrent_dropout=0.3,
        return_sequences=True
    ))
    model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3,))
    model.add(LSTM(512))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    return model


def prepare_sequences(items, n_vocab, sequence_length=100):
    """ Prepare the sequences used by the Neural Network """

     # create a dictionary to map items to integers
     # (we're treating this as categorical data, remember)
    item_names = get_item_names(items)
    item_to_int = dict((item, number) for number, item in enumerate(item_names))

    network_input = []
    network_output = []

    # create input sequences and the corresponding outputs
    for i in range(0, len(items) - sequence_length, 1):
        sequence_in = items[i:i + sequence_length]
        sequence_out = items[i + sequence_length]
        network_input.append([item_to_int[char] for char in sequence_in])
        network_output.append(item_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    normalized_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
    # normalize input
    normalized_input = normalized_input / float(n_vocab)

    return (normalized_input, network_output, network_input)


def train_network(items, filepath):
    # get number of unique items
    n_vocab = vocab_size(items)

    normalized_input, network_output, network_input = prepare_sequences(items, n_vocab)
    network_output = np_utils.to_categorical(network_output)

    model = create_network(normalized_input, n_vocab)

    train(model, normalized_input, network_output, filepath)


def train(model, network_input, network_output, filepath):
    """ train the neural network """
    checkpoint = ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]

    model.fit(network_input, network_output, epochs=200, batch_size=128, callbacks=callbacks_list)
