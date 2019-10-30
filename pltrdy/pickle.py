import pickle


def pickle_load(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def pickle_save(o, path):
    with open(path, 'wb') as f:
        pickle.dump(o, f)
