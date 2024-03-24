import pickle

def save_game_state(game_state, filename):
    with open(filename, "wb") as file:
        pickle.dump(game_state, file)

def load_game_state(filename):
    try:
        with open(filename, "rb") as file:
            game_state = pickle.load(file)
        return game_state
    except FileNotFoundError:
        return None
