from random import shuffle
import sys
import unittest
from datetime import datetime

class CardFactory:
    suits = ["spades", "hearts", "diamonds", "clubs"]
    values = [None, None, "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    @classmethod
    def create_card(cls, value, suit):
        return Card(value, suit)

class Card:
    suits = CardFactory.suits
    values = CardFactory.values

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"{self.values[self.value]} of {self.suits[self.suit]}"

class Deck:
    def __init__(self):
        self.cards = [CardFactory.create_card(value, suit) for value in range(2, 15) for suit in range(4)]
        shuffle(self.cards)

    def remove_card(self):
        return self.cards.pop() if self.cards else None

class Player:
    def __init__(self, name):
        self.wins = 0
        self.card = None
        self.name = name

    def __str__(self):
        return self.name

class ComputerPlayer(Player):
    def __init__(self):
        super().__init__("Computer")

class Game:
    def __init__(self, name1=None, name2=None, use_computer=None, logger=print):
        self.results_file = "game_results.txt"
        self.logger = logger
        self.read_previous_results()

        if name1 is None:
            name1 = input("Player 1 name: ")
        if use_computer is None:
            use_computer = input("Play against computer? (y/n): ").lower() == 'y'

        self.deck = Deck()
        self.p1 = Player(name1)
        if use_computer:
            self.p2 = ComputerPlayer()
        else:
            name2 = name2 or input("Player 2 name: ")
            self.p2 = Player(name2)

    def read_previous_results(self):
        try:
            with open(self.results_file, 'r') as file:
                results = file.readlines()
                if results:
                    print("\nPrevious Game Results:")
                    for line in results[-3:]: 
                        print(line.strip())
                else:
                    print("\nNo previous results found.")
        except FileNotFoundError:
            print("\nNo previous results found.")

    def wins(self, winner_name):
        self.logger(f"{winner_name} wins this round!")

    def draw(self, p1_name, p1_card, p2_name, p2_card):
        self.logger(f"{p1_name} drew {p1_card}, {p2_name} drew {p2_card}")

    def show_score(self):
        self.logger(f"Score → {self.p1.name}: {self.p1.wins} | {self.p2.name}: {self.p2.wins}\n")

    def play_game(self):
        print("\nBeginning War!\n")
        while len(self.deck.cards) >= 2:
            response = input("Press 'q' to quit. Any other key to play: ")
            if response.lower() == 'q':
                break

            table_cards = []
            p1_card = self.deck.remove_card()
            p2_card = self.deck.remove_card()
            self.p1.card = p1_card
            self.p2.card = p2_card
            table_cards.extend([p1_card, p2_card])
            self.draw(self.p1.name, p1_card, self.p2.name, p2_card)

            if p1_card > p2_card:
                self.p1.wins += 1
                self.wins(self.p1.name)
            elif p2_card > p1_card:
                self.p2.wins += 1
                self.wins(self.p2.name)
            else:
                self.logger("WAR!")
                self.war(table_cards)

            self.show_score()

        winner = self.determine_winner()
        self.save_result(winner)
        print(f"War is over. {winner if winner != 'It was a tie!' else winner}")

    def war(self, table_cards):
        if len(self.deck.cards) < 8:
            self.logger("Not enough cards to continue war. Ending war.")
            return

        self.logger("Each player places three cards face down and one face up.")

        for _ in range(3):
            table_cards.append(self.deck.remove_card()) 
            table_cards.append(self.deck.remove_card()) 

        p1_war_card = self.deck.remove_card()
        p2_war_card = self.deck.remove_card()
        table_cards.extend([p1_war_card, p2_war_card])
        self.draw(self.p1.name, p1_war_card, self.p2.name, p2_war_card)

        if p1_war_card > p2_war_card:
            self.p1.wins += 1
            self.logger(f"{self.p1.name} wins the war and takes {len(table_cards)} cards.")
        elif p2_war_card > p1_war_card:
            self.p2.wins += 1
            self.logger(f"{self.p2.name} wins the war and takes {len(table_cards)} cards.")
        else:
            self.logger("WAR again!")
            self.war(table_cards)

    def determine_winner(self):
        if self.p1.wins > self.p2.wins:
            return self.p1.name
        elif self.p2.wins > self.p1.wins:
            return self.p2.name
        else:
            return "It was a tie!"

    def save_result(self, winner):
        with open(self.results_file, 'a') as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Winner: {winner}\n")

class TestCard(unittest.TestCase):
    def test_card_comparison(self):
        c1 = Card(10, 2) 
        c2 = Card(11, 1) 
        self.assertTrue(c2 > c1)
        self.assertFalse(c1 > c2)
        self.assertTrue(c1 == Card(10, 0)) 

    def test_deck_size(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_winner_determination(self):
        game = Game(name1="Mykolas", name2="Simonas", use_computer=False, logger=lambda *args: None)
        game.p1.wins = 3
        game.p2.wins = 1
        self.assertEqual(game.determine_winner(), "Mykolas")
        game.p1.wins = 2
        game.p2.wins = 2
        self.assertEqual(game.determine_winner(), "It was a tie!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=sys.argv[:1])
    else:
        game = Game()
        game.play_game()
