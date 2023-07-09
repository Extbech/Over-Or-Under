import random
import pandas as pd
import matplotlib.pyplot as plt


class Deck:
    def __init__(self):
        self.cards = [x for x in range(1, 14)] * 4
        self.rounds_won = 0

    def draw_card(self):
        if len(self.cards) == 0:
            return False
        count_list = {}
        i = 1
        while i < max(self.cards) + 1:
            count_list[i] = self.cards.count(i)
            i += 1
        guessing_number = self.cards[len(self.cards) // 2]
        cardIndex = random.randint(0, len(self.cards) - 1)
        selected_card = self.cards.pop(cardIndex)

        if guessing_number == selected_card:
            self.rounds_won += 1
            return True

        elif selected_card > guessing_number:
            updated_count = {k: v for k, v in count_list.items() if k > guessing_number}
            guessing_number = max(updated_count)
            if selected_card == guessing_number:
                self.rounds_won += 1
                return True

        elif selected_card <= guessing_number:
            updated_count = {
                k: v for k, v in count_list.items() if k <= guessing_number
            }
            new_guess = max(updated_count)
            if guessing_number == new_guess:
                del updated_count[new_guess]
            new_guess = max(updated_count)
            if selected_card == new_guess:
                self.rounds_won += 1
                return True
        else:
            return False

    def play_game(self):
        self.cards.sort()
        while True:
            play = self.draw_card()
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
    for _ in range(10000000):
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
