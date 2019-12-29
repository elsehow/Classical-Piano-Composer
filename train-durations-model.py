import pickle
from lstm import train_network

if __name__ == '__main__':
    """ Train a Neural Network to generate music """
    with open('data/durations', 'rb') as filepath:
        notes = pickle.load(filepath)
    train_network(notes, 'weights-durations.hdf5')
