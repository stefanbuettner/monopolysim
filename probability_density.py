import random as rng
from matplotlib import pyplot as plt

def throw_dice():
    d1 = rng.randint(1,6)
    d2 = rng.randint(1,6)
    return d1 + d2


if __name__  == "__main__":

    num_fields = 40
    board = [0 for x in range(num_fields)]
    num_games = 1000
    num_moves = 300
    i = 0
    for game in range(num_games):
        pos = 0
        for move in range(num_moves):
            step = throw_dice()
            pos = (pos + step) % num_fields
            board[pos] += 1
            i += 1
    board = [x / i for x in board]
    print(board)
    plt.bar(range(num_fields), board)
    plt.show()
