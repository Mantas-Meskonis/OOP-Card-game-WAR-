from random import shuffle
import sys
import unittest

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
        self.name = name
        self.wins = 0
        self.card = None

    def __str__(self):
        return self.name

class ComputerPlayer(Player):
    def __init__(self):
        super().__init__("Computer")

class Game:
    def __init__(self, player1_name, player2_name=None, use_computer=False, results_file="game_results.txt", logger=print):
        self.logger = logger
        self.deck = Deck()
        self.p1 = Player(player1_name)
        self.p2 = ComputerPlayer() if use_computer else Player(player2_name or "Player 2")
        self.results_file = results_file

    def wins(self, winner_name):
        self.logger(f"{winner_name} wins this round!")

    def draw(self, p1_name, p1_card, p2_name, p2_card):
        self.logger(f"{p1_name} drew {p1_card}, {p2_name} drew {p2_card}")

    def show_score(self):
        self.logger(f"Score → {self.p1.name}: {self.p1.wins} | {self.p2.name}: {self.p2.wins}\n")

    def play_round(self):
        p1_card = self.deck.remove_card()
        p2_card = self.deck.remove_card()
        if not p1_card or not p2_card:
            return False

        self.p1.card = p1_card
        self.p2.card = p2_card
        self.draw(self.p1.name, p1_card, self.p2.name, p2_card)

        if p1_card > p2_card:
            self.p1.wins += 1
            self.wins(self.p1.name)
        elif p2_card > p1_card:
            self.p2.wins += 1
            self.wins(self.p2.name)
        else:
            self.logger("WAR!")
            self.war([p1_card, p2_card])

        self.show_score()
        return True

    def war(self, table_cards):
        if len(self.deck.cards) < 8:
            self.logger("Not enough cards to continue war. Awarding based on current score.")
            return

        self.logger("Each player places three cards face down and one face up...")

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
        return "It was a tie!"

    def save_result(self, winner):
        with open(self.results_file, 'a') as file:
            file.write(f"Winner: {winner}\n")

    def play_game(self):
        self.logger("Beginning War!")
        while len(self.deck.cards) >= 2:
            response = input("Press 'q' to quit. Any other key to play: ")
            if response.lower() == 'q':
                break
            if not self.play_round():
                break

        winner = self.determine_winner()
        self.save_result(winner)
        self.logger(f"War is over. {winner} won!")

class TestCardGame(unittest.TestCase):
    def test_card_comparison(self):
        c1 = Card(10, 2)  
        c2 = Card(11, 1) 
        self.assertTrue(c2 > c1)
        self.assertFalse(c1 > c2)
        self.assertFalse(c1 > c1)

    def test_deck_size(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_winner_determination(self):
        game = Game("Mykolas", "Simonas", logger=lambda *args: None)
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
        name1 = input("Player 1 name: ")
        use_computer = input("Play against computer? (y/n): ").lower() == 'y'
        name2 = None if use_computer else input("Player 2 name: ")
        game = Game(name1, name2, use_computer)
        game.play_game()