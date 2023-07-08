import random
import pandas as pd
import matplotlib.pyplot as plt

class Deck:
    def __init__(self):
        self.cards = [x for x in range(1, 14)]*4
        self.left_over_cards = []
        self.rounds_won = 0
    
    def draw_card(self):
        if len(self.cards) == 0:
            return False
        cardIndex = random.randint(0, len(self.cards)-1)
        selected_card = self.cards.pop(cardIndex)

        if len(self.left_over_cards) < 1:
            self.left_over_cards.append(selected_card)
            return True
        elif selected_card >= self.left_over_cards[-1]:
            self.left_over_cards.append(selected_card)
            self.rounds_won += 1
            return True
        else:
            return False
    
    def play_game(self):
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
        wins.append(curr_win/len(win_list)*100)
        round_names.append(f"round_{rounds}")
    return wins, round_names


if __name__ == "__main__":
    win_list = []
    for _ in range(100000):
        deck = Deck()
        win_list.append(deck.play_game())
                        
    perc, round_names = get_win_percentage(win_list)

    ## Dataframe visualization
    df = pd.DataFrame(data=perc, index=round_names, columns=["%"])
    print(df.head())

    ## Plotting
    fig = plt.figure(figsize = (10, 6))
    bar_colors = ['tab:green', 'tab:blue', 'tab:red', 'tab:orange']
    plt.bar(round_names, perc, color = bar_colors)
    plt.xlabel("Rounds Won")
    plt.ylabel("%")
    plt.title(f"How likely it is to win consecutive rounds in over or under. Simlations of {len(win_list)} games.")
    plt.savefig("over_or_under.png")