import random

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
        return f"{self.rank} of {self.suit_symbols[self.suit]}"
    

class Deck:
    def __init__(self):
        self.suits = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
        self.ranks = [str(x+1) for x in range(1,10)] + ['Jack', 'Queen', 'King', 'Ace']
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
            num_cards_per_player = int(input('How many cards are to be dealt per player? '))

        for i in range(num_players):
            player = players[i]
            start_index = 0
            end_index = num_cards_per_player
            player.hand = self.card_list[start_index:end_index]
            del self.card_list[start_index:end_index]
            player.hand = sorted(player.hand, key=lambda card: (card.suit, card.rank))
        
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

    def __str__(self):
        return f"{self.name} is a {self.status}"

    def show_hand(self):
        str_hand = [f"{card.rank if len(card.rank) <= 2 else card.rank[0]} {card.suit_symbols[card.suit]}" for card in self.hand]
        print(str_hand)
        return str_hand
    
    def play_card(self, card):
        self.hand.pop() 
        return card


def create_players(num_players, num_bots):
    players = []
    for i in range(num_players):
        if i < (num_players - num_bots):
            players.append(Player(f"Player {i+1}", 'human'))
        else:
            players.append(Player(f"Player {i+1}", 'bot'))
    return players

def play_round(players, card_dict):
    for i in range(len(players)):
        player = players[i]
        if player.status == 'human':
            print('Your hand: \n') 
            str_hand = player.showhand()
            requested_card = input('What card would you like to play? ')

        elif player.status == 'bot':
            pass
    pass

def user_turn(player):

    pass

def create_game():
    # num_players = int(input('How many players are there? '))
    # num_bots = int(input('How many of these players will be bots? '))
    players = create_players(4, 3)
    deck = Deck()
    deck.shuffle()
    deck.deal(players)
    for i in range(len(players)):
        players[i].show_hand()
    print('\n')
    print(deck.show_deck())



create_game()

