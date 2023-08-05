import pickle


def download_svrt():
    return pickle.load(open('signal_separation/trained/SVRp', 'rb'))


def download_svrh():
    return pickle.load(open('signal_separation/trained/SVRh', 'rb'))


def download_weights(model):
    model.load_weights('signal_separation/trained/neural_network.h5')
    pass
