import tkinter as tk
from tkinter import messagebox

def read_table():
    with open("table.txt", "r") as f:
        dealer = f.readline().split()
        table = dict()
        for i in range(29):
            row = f.readline().split()
            me = row[:1]
            values = row[1:]
            row_dict = dict()
            for card, value in zip(dealer, values):
                row_dict[card] = value
            table[me[0]] = row_dict
        return table

class CardCounterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack Card Counter")

        # Initialize number of decks
        self.num_decks = tk.StringVar()
        
        # Create label and entry for number of decks
        tk.Label(self.master, text="Number of Decks:").grid(row=0, column=0, padx=5, pady=5)
        self.num_decks_entry = tk.Entry(self.master, textvariable=self.num_decks)
        self.num_decks_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Create button to start
        self.start_button = tk.Button(self.master, text="Start", command=self.start_game)
        self.start_button.grid(row=0, column=2, padx=5, pady=5)

    def start_game(self):
        try:
            num_decks = int(self.num_decks.get())
            if num_decks <= 0:
                raise ValueError
            self.master.destroy()
            root = tk.Tk()
            app = CardCounterGame(root, num_decks)
            root.mainloop()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of decks.")


class CardCounterGame:
    def __init__(self, master, num_decks):
        self.master = master
        self.master.title("Blackjack Card Counter")

        # Initialize card counts
        self.card_counts = {card: 0 for card in range(2, 12)}
        self.cards_drawn = 0
        self.number_of_decks = num_decks
        self.total_cards_of_one_type = self.number_of_decks * 4
        self.total_cards_10 = self.number_of_decks * 4 * 4
        self.total_cards = num_decks * 4 * 13
        self.strategy_counter = 0
        self.table = read_table()
        self.number_of_decks_remaining = num_decks
        self.true_count = 0

        # Create card buttons
        self.card_buttons = []
        for card_value in range(2, 12):
            if card_value == 11:
                button = tk.Button(self.master, text="A", command=lambda val=card_value: self.increment_count(val), width=5, height=2)
            else:
                button = tk.Button(self.master, text=str(card_value), command=lambda val=card_value: self.increment_count(val), width=5, height=2)
            button.grid(row=0, column=card_value-1, padx=5, pady=5)
            self.card_buttons.append(button)

        # Create labels to display counts
        self.count_labels = []
        for card_value in range(2, 12):
            if card_value != 10:
                label = tk.Label(self.master, text=f"{self.card_counts[card_value]}/{self.total_cards_of_one_type}", width=5)
                
            else:
                label = tk.Label(self.master, text=f"{self.card_counts[card_value]}/{self.total_cards_10}", width=5)
            label.grid(row=1, column=card_value-1)
            self.count_labels.append(label)

        # Create reset button
        self.reset_button = tk.Button(self.master, text="Reset Counts", command=self.reset_counts, width=50, height=2)
        self.reset_button.grid(row=3, columnspan=10, pady=10)
        self.cards_drawn_label = tk.Label(self.master, text="Cards Drawn: {}/{}".format(self.cards_drawn, self.total_cards))
        self.cards_drawn_label.grid(row=4, column=0, columnspan=10, padx=10, pady=10, sticky="sw")

        self.count_strategy_label = tk.Label(self.master, text="Count Strategy: {}".format(self.strategy_counter))
        self.count_strategy_label.grid(row=3, column=9, columnspan=10, padx=10, pady=10, sticky="sw")

        self.true_count_label = tk.Label(self.master, text="True Count: {}".format(self.true_count))
        self.true_count_label.grid(row=4, column=9, columnspan=10, padx=10, pady=10, sticky="sw")

        self.betting_message_label = tk.Label(self.master, text=f"You have to bet {round(self.true_count -1, 1)} betting units!")
        self.betting_message_label.grid(row=5, column=0, columnspan=10, padx=10, pady=10, sticky="sw")

        # Create input field and label
        tk.Label(self.master, text="<Dealer>vs<Us>:").grid(row=4, column=4, padx=5, pady=5)
        self.input_field = tk.Entry(self.master)
        self.input_field.grid(row=4, column=5, columnspan=2, padx=5, pady=5)
        self.input_field.bind('<Return>', self.handle_input)

        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=4, column=7, columnspan=2) 

        # Configure column to expand
        for i in range(10):
            self.master.columnconfigure(i, weight=1)

    def increment_strategy_counter(self, card_value):
        if card_value in {10,11}:
            self.strategy_counter -= 1
        if card_value in {2,3,4,5,6}:
            self.strategy_counter += 1


    def increment_count(self, card_value):
        self.card_counts[card_value] += 1
        self.cards_drawn += 1
        self.number_of_decks_remaining = (self.total_cards - self.cards_drawn) / (4*13)
        self.increment_strategy_counter(card_value)
        self.true_count = round(self.strategy_counter / self.number_of_decks_remaining, 2)
        self.update_count_labels()

    def reset_counts(self):
        confirm_reset = messagebox.askokcancel("Reset Counts", "Are you sure you want to reset counts?")
        if confirm_reset:
            for card_value in range(2, 12):
                self.card_counts[card_value] = 0
            self.cards_drawn = 0
            self.number_of_decks_remaining = self.number_of_decks
            self.strategy_counter = 0
            self.true_count = 0
            self.update_count_labels()

    def update_count_labels(self):
        for card_value in range(2, 12):
            if card_value != 10:
                self.count_labels[card_value-2].config(text=f"{self.card_counts[card_value]}/{self.total_cards_of_one_type}")
            else:
                self.count_labels[card_value-2].config(text=f"{self.card_counts[card_value]}/{self.total_cards_10}")
        self.cards_drawn_label.config(text="Cards Drawn: " + str(self.cards_drawn)+"/"+ str(self.total_cards))
        self.count_strategy_label.config(text="Count Strategy: " + str(self.strategy_counter))
        self.true_count_label.config(text="True Count: " + str(self.true_count))
        self.betting_message_label.config(text=f"You have to bet {round(self.true_count - 1, 1)} betting units!")

    def handle_input(self, event):
        user_input = self.input_field.get().strip().upper().split("VS")
        if len(user_input) != 2:
            self.result_label.config(text="Invalid input")
            self.input_field.delete(0, tk.END)
            return
        dealer = user_input[0]
        me = user_input[1]
        row = self.table.get(me)
        if row is None:
            self.result_label.config(text="Invalid input")
        else:
            entry = row.get(dealer)
            if entry is None:
                self.result_label.config(text="Invalid input")
            else:
                self.result_label.config(text=entry)
        self.input_field.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = CardCounterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

                                 