import pickle


def download_svrt():
    return pickle.load(open('./trained/SVRp', 'rb'))


def download_svrh():
    return pickle.load(open('./trained/SVRh', 'rb'))


def download_weights(model):
    model.load_weights('./trained/neural_network.h5')
    pass
