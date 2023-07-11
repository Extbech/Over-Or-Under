import random
import pandas as pd
import tqdm
import matplotlib.pyplot as plt

class Player:
    def __init__(self):
        self.unseen_cards = {i: 4 for i in range(1, 14)}

    def make_first_guess(self):
        return 1

    def make_second_guess(self, is_over):
        return 1

    def found_card(self, i):
        self.unseen_cards
        return

class Deck:
    def __init__(self):
        self.cards = [x for x in range(1, 14)] * 4
        self.rounds_won = 0

    def draw_card(self, player):
        if len(self.cards) == 0:
            return False
        guessing_number = player.make_first_guess()
        cardIndex = random.randint(0, len(self.cards) - 1)
        selected_card = self.cards.pop(cardIndex)

        if guessing_number == selected_card:
            player.found_card(guessing_number)
            self.rounds_won += 1
            return True

        elif selected_card > guessing_number:
            guessing_number = player.make_second_guess(True)
            if selected_card == guessing_number:
                player.found_card(guessing_number)
                self.rounds_won += 1
                return True

        elif selected_card < guessing_number:
            guessing_number = player.make_second_guess(False)
            if selected_card == new_guess:
                player.found_card(guessing_number)
                self.rounds_won += 1
                return True
        else:
            return False

    def play_game(self):
        self.cards.sort()
        player = Player()
        while True:
            play = self.draw_card(player)
            if not play:
                return self.rounds_won

def get_win_percentage(win_list: list) -> list:
    wins = []
    round_names = []
    for rounds in range(1, max(win_list)):
        curr_win = 0
        for win in win_list:
            if win >= rounds:
                curr_win += 1
        wins.append(curr_win / len(win_list) * 100)
        round_names.append(f"{rounds}")
    return wins, round_names

if __name__ == "__main__":
    win_list = []
    for _ in tqdm.tqdm(range(100000)):
        deck = Deck()
        win_list.append(deck.play_game())

    perc, round_names = get_win_percentage(win_list)

    ## Dataframe visualization
    df = pd.DataFrame(data=perc, index=round_names, columns=["%"])
    print(df.head())

    ## Plotting
    fig = plt.figure(figsize=(10, 6))
    bar_colors = ["tab:green", "tab:blue", "tab:red", "tab:orange"]
    plt.bar(round_names, perc, color=bar_colors)
    plt.xlabel("Rounds Won")
    plt.ylabel("%")
    plt.title(
        f"How likely it is to win consecutive rounds in over or under. Simlations of {len(win_list)} games."
    )
    plt.savefig("over_or_under.png")
