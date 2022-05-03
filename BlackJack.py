import pyttsx3
from random import shuffle

# Sound Engine
engine = pyttsx3.init()

suits = ("Hearts", "Clubs", "Spades", "Diamonds")
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8,
          "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10,
          "Ace": 1}
ranks = values.keys()

def pauseExecution():
    while (input() != '\n'):
        pass
    return None

class Card:
    def __init__(self, suit, rank):
        '''
        :param suit: suit of card[hearts,diamonds,spades,clubs]
        :param rank: rank of card from (2,10,jack,queen,king,ace)
        :returns: A card belonging to the entered suit and rank
        '''
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self, _suits, _ranks):
        '''
        Complete deck of cards based on suits and ranks provided.
        :param _suits: List of strings specifying desired suits.
        :param _ranks: List of strings specifying desired ranks.
        :returns: A deck of cards with cards of all possible suits and ranks.
        '''
        self.cards = [Card(suit, rank) for suit in _suits for rank in _ranks]

    def shuffle(self):
        shuffle(self.cards)

    def __str__(self):
        return str(len(self.cards)) + " cards"

    def __len__(self):
        return len(self.cards)


class Player:

    def __init__(self, name, deck, game_rounds, _player_money):
        self.name = name
        self.hand = [deck.cards.pop(0) for _ in range(2)]
        if game_rounds == 0:
            self.money = 1000
        else:
            self.money = _player_money

    def hit(self, deck):
        self.hand.append(deck.cards.pop(0))
        if self.hand[-1].rank == "Ace":
            while True:
                try:
                    self.hand[-1].value = int(input("What do you want to consider your ace value as '1' or '11'?"))
                    if self.hand[-1].value not in [1, 11]:
                        print("That's not a valid value!")
                        engine.say("That's not a valid value!")
                        engine.runAndWait()
                        continue
                    else:
                        break
                except ValueError:
                    print("Value of card must be an integer.")
                    engine.say("Value of card must be an integer.")
                    engine.runAndWait()
                    continue

    def player_score(self):
        return sum(map(lambda a: a.value, self.hand))

    def __str__(self):
        return f"PLAYER HAND: {list(map(str,self.hand))}"


class ComputerDealer:

    def __init__(self, deck):
        self.name = "Computer"
        self.hand = [deck.cards.pop(0) for _ in range(2)]

    def hit(self, deck):
        self.hand.append(deck.cards.pop(0))
        if self.hand[-1].rank == "Ace":
            if self.computer_score() + 10 <= 21:
                # Default value of ace is 1, so replacing it with 11 would an increment of 10
                print(f"Dealer decides to treat his {self.hand[-1]} as 11")
                engine.say(f"Dealer decides to treat his {self.hand[-1]} as 11")
                engine.runAndWait()
                self.hand[-1].value = 11
            else:
                print(f"Dealer decides to treat his {self.hand[-1]} as 1")
                engine.say(f"Dealer decides to treat his {self.hand[-1]} as 1")
                engine.runAndWait()
                pass

    def computer_score(self):
        return sum(map(lambda a: a.value, self.hand))

    def __str__(self):
        return f"COMPUTER HAND: [{self.hand[0]},{self.hand[1:]}]"

def move_choice():
    pin = ""
    while pin not in ["hit", "stay"]:
        engine.say("Do you want to 'hit' or 'stay'?")
        engine.runAndWait()
        pin = input("Do you want to 'hit' or 'stay'?").lower()
        if pin not in ["hit", "stay"]:
            print("Learn to play First!")
            engine.say("Learn to play First!")
            engine.runAndWait()
    return pin


def score_check(_player):
    player_score = sum(map(lambda a: a.value, _player.hand))
    if player_score <= 21:
        print(f"{_player.name} hit!\n{_player}")
        engine.say(f"{_player.name} hit!\n")
        return True
    else:
        print(f"{_player.name} Busted!")
        engine.say(f"{_player.name} Busted!")
        engine.runAndWait()
        return False


def bet_choice(_player):
    _bet = 0
    while True:
        try:
            print(f"How much do you want to put on stake {player.name}?\nYou currently have {_player.money} coins.")
            engine.say(f"How much do you want to put on stake {player.name}?\nYou currently have {_player.money} coins.")
            engine.runAndWait()
            _bet = int(input())
            if _bet < 50:
                print("You broke or what?!\nEnter a bet of at least 50")
                engine.say("You broke or what?!\nEnter a bet of at least 50")
                engine.runAndWait()
                continue
            else:
                if _bet > _player.money:
                    print("Not enough money!")
                    engine.say("Not enough money!")
                    engine.runAndWait()
                    continue
                else:
                    return _bet
        except ValueError:
            print("Did you learn counting in school?")
            engine.say("Did you learn counting in school?")
            engine.runAndWait()
            continue


def replay_choice():
    pin = ""
    while pin not in ["yes", "no"]:
        engine.say("Wanna play another round?")
        engine.runAndWait()
        pin = input("Wanna play another round?").lower()
        if pin not in ["yes", "no"]:
            print("I don't understand.")
            engine.say("I don't understand.")
            engine.runAndWait()
    return pin

# Game Logic Starts
rounds = 0
game_on = 1
player_money = 1000

engine.say("Welcome to BlackJack, Please enter your name")
engine.runAndWait()
player_name = input("Welcome to BlackJack!\nPlease enter your name: ")

while game_on:
    game_deck = Deck(suits, ranks)
    shuffle(game_deck.cards)
    player = Player(player_name, game_deck, rounds, player_money)
    computer = ComputerDealer(game_deck)
    bet = bet_choice(player)
    player.money -= bet
    player_money = player.money
    round_on = 1
    while round_on:

        print(f"Round {rounds}")
        print(player, ",", computer)
        player_turn = 1
        while player_turn:
            player_choice = move_choice()
            if player_choice == "hit":
                player.hit(game_deck)
                if score_check(player):
                    continue
                else:
                    win = 0
                    round_on = 0
                    break
            else:
                print(f"{player.name} decided to 'stay'!")
                engine.say(f"{player.name} decided to 'stay'!")
                engine.runAndWait()
                player_turn = 0
                break

        if round_on:
            computer_turn = 1
        else:
            computer_turn = 0

        while computer_turn:
            while computer.computer_score() <= 21:
                computer.hit(game_deck)
                if score_check(computer):
                    if computer.computer_score() > player.player_score():
                        print(f"Dealer Score: {computer.computer_score()}!")
                        win = 0
                        computer_turn = 0
                        round_on = 0
                        break
                    elif computer.computer_score() == player.player_score() == 21:
                        win = 2
                        computer_turn = 0
                        round_on = 0
                        break
                    continue
                else:
                    win = 1
                    computer_turn = 0
                    round_on = 0
                    break

        if win == 1:
            print(f"{player.name} Wins!")
            print(f"{player.name} Deck: {list(map(str,player.hand))},Dealer Deck: {list(map(str,computer.hand))}")
            player_money += 2*bet
        elif win == 2:
            print("TIE GAME!\n Both dealer and player on 21.")
            print(f"{player.name} Deck: {list(map(str, player.hand))},Dealer Deck: {list(map(str, computer.hand))}")
            player_money += bet
        else:
            print(f"{player.name} Deck: {list(map(str, player.hand))},Dealer Deck: {list(map(str, computer.hand))}")
            print("You Lose!")
            if player_money < 50:
                print("You have gone bankrupt!\n*GAME OVER*")
                pauseExecution()
                game_on = 0
                break
    if game_on:
        if replay_choice() == "no":
            game_on = 0
        else:
            pass
    rounds += 1
