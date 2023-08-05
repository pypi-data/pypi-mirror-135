import pickle
from pathlib import Path
def download_svrt():
    p = Path(__file__).parent
    p = Path(p, 'trained', 'SVRp')
    return pickle.load(open(p, 'rb'))


def download_svrh():
    p = Path(__file__).parent
    p = Path(p, 'trained', 'SVRh')
    return pickle.load(open(p, 'rb'))


def download_weights(model):
    p = Path(__file__).parent
    p = Path(p, 'trained', 'neural_network.h5')
    model.load_weights(p)
    pass