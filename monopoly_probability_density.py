from matplotlib import pyplot as plt
from matplotlib import colors
from argparse import ArgumentParser
import numpy as np
from common import FieldPos
import classic
import frozen

if __name__  == "__main__":

    parser = ArgumentParser(description="Simulates the player movement of the board game monopoly and shows the approximated propability density of the player's position.")
    parser.add_argument("-n", "--games", dest="num_games", default=1000, type=int, help="Number of games to simulate.")
    parser.add_argument("-k", "--moves", dest="num_moves", default=300, type=int, help ="Number of moves per game.")
    parser.add_argument("--buy-free", dest="buy_free", action='store_true', help="The player always buys himself/herself out of jail.")
    parser.add_argument("--variant", dest="variant", default="classic", choices=["classic", "frozen"], help="The monopoly variant to simulate.")
    args = parser.parse_args()

    num_games = args.num_games
    num_moves = args.num_moves

    print("Simulating %d %s games with %d moves each." % (num_games, args.variant, num_moves))
    
    num_fields = 40
    board = np.zeros(num_fields)
    profit_0 = np.zeros(num_fields)
    chance_fields = [FieldPos.CHANCE_1, FieldPos.CHANCE_2, FieldPos.CHANCE_3]
    community_fields = [FieldPos.COMMUNITY_1, FieldPos.COMMUNITY_2, FieldPos.COMMUNITY_3]

    color = colors.get_named_colors_mapping()
    # Rents from 
    # http://www.math.yorku.ca/~zabrocki/math2042/Monopoly/prices.html
    variant = None
    if args.variant == "classic":
        variant = classic
    elif args.variant == "frozen":
        variant = frozen
    else:
        raise RuntimeError("variant" + args.variant + " undefined")
    
    board_fields = variant.board_fields

    i = 0
    for game in range(num_games):

        chance_cards = variant.init_chance_cards()
        community_cards = variant.init_community_cards()

        player = variant.Player(num_fields, args.buy_free)

        for move in range(num_moves):

            player.move()

            if player.pos in chance_fields:
                card = chance_cards.pop()
                card.execute(player)
                if len(chance_cards) <= 0:
                    chance_cards = variant.init_chance_cards()

            if player.pos in community_fields:
                card = community_cards.pop()
                card.execute(player)
                if len(community_cards) <= 0:
                    community_cards = variant.init_community_cards()

            board[player.pos] += 1
            profit_0[player.pos] += board_fields[player.pos].get_rent_0(player.threw)
            i += 1

    board = board / i
    profit_0 = profit_0 / i

    board_colors = [f.color for f in board_fields]
    field_names = [f.name for f in board_fields]
    rents_0 = np.array([f.rent_0 for f in board_fields]) * board

    x = np.arange(num_fields)

    scale = 5
    plt.xkcd()
    fig, ax = plt.subplots(figsize=(2 * scale, 1 * scale))
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    prop = ax.bar(x, board, color=board_colors)
    ax.set_title("Monopoly probability density distribution")
    ax.set_ylabel("Probability")
    ax.set_xlabel("FieldPos index")

    # profit = ax.bar(x, profit_0, color=board_colors)
    # ax.set_title("Monopoly's expected return per throw")
    # ax.set_ylabel("Expected return")
    # ax.set_xlabel("FieldPos index")

    plt.tight_layout()
    plt.show()
