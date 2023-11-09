import random
import time

time_delay = 1

class Card:
    def __init__(self, rank, suit) -> None:
        self.card_values = {
            'Ace': 11,  # value of the ace is high until it needs to be low
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'Jack': 10,
            'Queen': 10,
            'King': 10
        }
        self.suit_symbols = {
            'Spades': '♠',
            'Diamonds': '♦',
            'Hearts': '♥',
            'Clubs': '♣'
        }
        self.suit = suit
        self.rank = rank
        self.points = self.card_values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.suits = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
        self.ranks = [str(x+1) for x in range(1, 10)] + \
            ['Jack', 'Queen', 'King', 'Ace']
        self.card_list = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def show_deck(self):
        return [f"{card.rank} {card.suit_symbols[card.suit]}" for card in self.card_list]

    def shuffle(self):
        self.card_list = random.sample(self.card_list, len(self.card_list))
        return self.card_list

    def deal(self, players, deal_all=True):
        if len(players) == 0:
            print("No players to deal cards to.")
            return

        num_players = len(players)

        if deal_all:
            num_cards_per_player = len(self.card_list) // num_players
        else:
            num_cards_per_player = int(
                input('How many cards are to be dealt per player? '))

        for i in range(num_players):
            player = players[i]
            start_index = 0
            end_index = num_cards_per_player
            player.hand = self.card_list[start_index:end_index]
            del self.card_list[start_index:end_index]
            player.hand = sorted(
                player.hand, key=lambda card: (card.suit, card.rank))

        if deal_all:
            for player in players:
                if len(self.card_list) != 0:
                    player.hand.append(self.card_list.pop(0))
                else:
                    break


class Player:
    def __init__(self, name, status) -> None:
        self.name = name
        self.status = status
        self.hand = []
        self.cards_that_follow_suit = []
        self.tricks = []
        self.first = False
        self.can_follow_suit = False
        self.played_card = None
        self.won_last_round = False

    def __str__(self):
        return f"{self.name} is a {self.status}"

    def show_hand(self):
        str_hand_symbols = convert_to_readable(self.hand, True)
        print(str_hand_symbols)
        return str_hand_symbols

    def play_card(self, card):
        self.hand.pop()
        return card


def convert_to_readable(card_list, symbols=False):
    if not symbols:
        return [str(card) for card in card_list]
    return [[f"{card.rank if len(card.rank) <= 2 else card.rank[0]} {card.suit_symbols[card.suit]}"] for card in card_list]


def create_players(num_players, num_bots):
    players = []
    for i in range(num_players):
        if i < (num_players - num_bots):
            player_name = input(f"Insert Player {i+1}'s name: ")
            players.append(Player(player_name, 'human'))
        else:
            players.append(Player(f"Player {i+1}", 'bot'))
    return players

def who_goes_first(players, first_round):
    if first_round:
        # Owner of the 2 of Clubs starts
        for i in range(len(players)):
            player = players[i]
            if '2 of Clubs' in convert_to_readable(player.hand):
                starting_player = i
        reordered_players = players[starting_player:] + players[:starting_player]
        reordered_players[0].first = True
        print(f"{reordered_players[0].name} owns the 2 of Clubs! They go first!")
        time.sleep(time_delay)
    else:
        for i in range(len(players)):
            player = players[i]
            if player.won_last_round:
                starting_player = i
                player.won_last_round = False
        reordered_players = players[starting_player:] + players[:starting_player]
        reordered_players[0].first = True
        print(f"{reordered_players[0].name} goes first!")
        time.sleep(time_delay)
    return reordered_players

def follow_suit(player, trick):
    player.cards_that_follow_suit = []
    for card in player.hand:
        if card.suit == trick[0].suit:
            player.cards_that_follow_suit.append(card)
            player.can_follow_suit = True
    return player

def play_round(players):
    trick = []
    for i in range(len(players)):
        player = players[i]
        if player.status == 'human':
            trick = human_turn(player, trick)
        elif player.status == 'bot':
            trick = bot_turn(player, trick)
    players = who_won(players, trick)
    return players

def human_turn(player, trick):
    valid_card = False
    print(f"It's {player.name}'s turn.")
    # Don't display played cards if human player goes first
    if len(trick) > 0:
        print('The following cards have been played. You must follow suit if possible.\n', convert_to_readable(trick, True))
        time.sleep(time_delay)
    print('Your hand:')
    player.show_hand()
    time.sleep(time_delay)
    print('What card would you like to play?\n(Type "A ♠" as "Ace of Spades" or "2 ♥" as "2 of Hearts)')
    time.sleep(time_delay)
    str_hand = convert_to_readable(player.hand)
    if not player.first:
        player = follow_suit(player, trick)
    while not valid_card:
        requested_card = input('Your chosen card: ')
        time.sleep(time_delay)
        if requested_card in str_hand:
            index = str_hand.index(requested_card)
            player.played_card = player.hand[index]
            if player.first:
                trick.append(player.played_card)
                player.hand.remove(player.played_card)
                valid_card = True
            elif (player.played_card.suit == trick[0].suit and player.can_follow_suit) or not player.can_follow_suit:
                trick.append(player.played_card)
                player.hand.remove(player.played_card)
                valid_card = True
            else:
                print('The card you pick must be of the same suit as the first, if possible.')
                time.sleep(time_delay)
                print(f'You must play one of these cards:\n {convert_to_readable(player.cards_that_follow_suit, True)}')
                time.sleep(time_delay)
        else:
            print('The card you tried to play is not in your hand. Try again.')
            time.sleep(time_delay)
    return trick

def bot_turn(player, trick):
    player.played_card = random.choice(player.hand)
    if not player.first:
        player = follow_suit(player, trick)
        if player.can_follow_suit:
            player.played_card = random.choice(player.cards_that_follow_suit)
    trick.append(player.played_card)
    player.hand.remove(player.played_card)
    return trick

def who_won(players, trick):
    cards_in_suit = []
    for card in trick:
        if card.suit == trick[0].suit:
            cards_in_suit.append(card)
    cards_in_suit_points = [card.points for card in cards_in_suit]
    winning_card = cards_in_suit[cards_in_suit_points.index(max(cards_in_suit_points))]
    for player in players:
        if player.played_card == winning_card:
            print(f"{player.name} won that trick!")
            time.sleep(time_delay)
            player.won_last_round = True
            player.tricks.append(trick)
    return players
        

def create_game():
    print("Welcome to HEARTS!")
    options = input("Type 'help' for the rules or 'play' to begin the game: ")
    if options == 'play':
        num_bots = int(input('How many of these players will be bots? '))
        players = create_players(4, num_bots)
        deck = Deck()
        deck.shuffle()
        deck.deal(players)
        first_round = True
        for i in range(13):
            if i > 0:
                first_round = False
            players = who_goes_first(players, first_round)
            players = play_round(players)
            print(f'End of round {i+1}:')
            time.sleep(time_delay)
            round_stats = ''
            for player in players:
                if len(player.tricks) > 0:
                    round_stats += f'{player.name} has {len(player.tricks)} trick(s), '
            print(round_stats[:-2] + '!')


create_game()
