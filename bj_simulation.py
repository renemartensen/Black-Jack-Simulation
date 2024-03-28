import numpy as np
import random
import pandas as pd
import argparse
    

class Utility: 

    @classmethod
    def create_output_html_file(self, relative_table, table, table_difference, output_file):

        # Convert the matrix to a DataFrame
        df = pd.DataFrame(relative_table, index = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "A"])

        df_decision_table = pd.DataFrame(table, index = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"])

        # Convert DataFrame to HTML
        html_table = df.to_html()  # Set index=False to exclude index from HTML

        html_decision_table = df_decision_table.to_html()


        if table_difference:
            df_difference_table = pd.DataFrame(table_difference, index = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"])
            html_difference = df_difference_table.to_html()
            # Combine HTML content into a single page
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Blackjack</title>
            </head>
            <body>
                <h2>Decision Table</h2>
                {html_decision_table}
                <h2>Winrates of decisions</h2>
                {html_table}
                <h2>Differences - Comparison against complementary actions</h2>
                <p>Negative values = Alternative action has been better</p>
                <p>Positive values = Action specified by table has been better</p>
                {html_difference}
            </body>
            </html>
            """
        else:
            # Combine HTML content into a single page
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Blackjack</title>
            </head>
            <body>
                <h2>Decision Table</h2>
                {html_decision_table}
                <h2>Winrates of decisions</h2>
                {html_table}
            </body>
            </html>
            """
        # Output HTML
        with open(output_file, 'w') as f:
            f.write(html_content)
    
    @classmethod
    def read_table(self):
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
        

    @classmethod
    def extract_strings(self, input_string):
        numbers = ''
        letters = ''
        for char in input_string:
            if char.isdigit():
                numbers += char
            elif char == 'A':
                letters += char
        return numbers, letters

    @classmethod
    def add_values(self, player, card_value): 
        value = ""
        number, ace = Utility.extract_strings(player)
        if player == "A":
            if card_value in {"King", "Queen", "Jack"}:
                value = player + "10"
            elif card_value == 'A':
                value = 'A' + card_value
            else:   
                value = player + card_value
        elif player == 'AA':
            if card_value in {"King", "Queen", "Jack"} or card_value == '10':
                value = "12"
            elif card_value == 'A':
                value = 'A' + '2'
            else:   
                value = 'A' + str(int(card_value)+1)
        elif card_value == 'A':
            if 'A' in player:
                value = ace + str(int(number)+1)
            elif int(player) > 10:
                value = str(int(player) + 1)
            else:
                value = card_value + player
        elif card_value in  {"King", "Queen", "Jack"}:
            if 'A' in player:
                if int(number)+10 > 10:
                    value = str(int(number)+10 +1)
                else:
                    value = ace + str(int(number)+10)
            else:
                value = str(int(player)+10)
        elif card_value in {'2', '3', '4', '5', '6', '7', '8', '9', '10'}:
            if len(ace) > 0:
                if int(number) + int(card_value) > 10:
                    value = str(int(number) + int(card_value) + 1)
                else: 
                    value = ace + str(int(number) + int(card_value))
            else:
                value = str(int(player) + int(card_value))
        else:
            print("Somehing gone wrong", player, card_value)
        return value

    @classmethod
    def get_value(self, value):
        number, ace = Utility.extract_strings(value)
        num_aces = len(ace)

        if number == '1010':
            hand_value = 20
        elif len(number)>0:
            hand_value = int(number) + num_aces * 11
        else:
            hand_value = num_aces*11
        # Adjust for aces if necessary
        while hand_value > 21 and num_aces > 0:
            hand_value -= 10  # Convert ace from 11 to 1
            num_aces -= 1
        if hand_value >= 17:
            return str(hand_value)
        else:
            return value
        
    @classmethod
    def get_and_change_to_complement_action(self, current, player, dealer, table):
        alternative_action = 'same'
        if current == 'S':
            table.get(player)[dealer] = 'H'
            alternative_action = 'H'
        elif current == 'D':
            table.get(player)[dealer] = 'H'
            alternative_action = 'H'
        elif current == 'H':
            table.get(player)[dealer] = 'S'
            alternative_action = 'S'
        return alternative_action



class Deck:
    def __init__(self, num_decks=6, counting = True):
        self.stack = []
        self.num_decks = num_decks
        self.populate_deck()
        self.draw_until = random.randint(int(len(self.stack)*(1/2)), int(len(self.stack)*(4/5)))
        self.has_to_shuffle = False

        self.counting = counting
        self.total_cards = num_decks * (4*13)
        self.cards_drawn = 0
        self.number_of_decks_remaining = num_decks
        self.strategy_counter = 0
        self.true_count = 0 
        self.units_to_bet = round(self.true_count -1, 1)

    def populate_deck(self):
        self.stack = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'A']
        for _ in range(self.num_decks):
            for suit in suits:
                for rank in ranks:
                    self.stack.append(Card(suit, rank))
        random.shuffle(self.stack)

    def shuffle(self):
        self.populate_deck()
        self.draw_until = random.randint(int(len(self.stack)*(1/2)), int(len(self.stack)*(4/5)))
        self.has_to_shuffle = False
        self.reset_counts()


    def draw(self):
        card = self.stack.pop()
        if self.counting:
            self.update_counts(card.rank)
        if len(self.stack) > self.draw_until:
            return card
        else:
            self.has_to_shuffle = True
            return card
        
    def reset_counts(self):
        self.cards_drawn = 0
        self.number_of_decks_remaining = self.num_decks
        self.strategy_counter = 0
        self.true_count = 0
        self.units_to_bet = round(self.true_count -1, 1)
        
    def update_counts(self, card):
        self.increment_strategy_counter(card)
        self.cards_drawn += 1
        self.number_of_decks_remaining = (self.total_cards - self.cards_drawn) / (4*13)
        self.true_count = round(self.strategy_counter / self.number_of_decks_remaining, 2)
        self.units_to_bet = round(self.true_count -1, 1)
        
    
    def increment_strategy_counter(self, card_value):
        if card_value in {'10','Jack', 'Queen', 'King', 'A'}:
            self.strategy_counter -= 1
        if card_value in {'2','3','4','5','6'}:
            self.strategy_counter += 1


    
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank


class Simulator:

    def __init__(self, num_decks, reps):
        self.table_relative = dict()
        self.table = Utility.read_table()
        self.table_difference = dict()
        self.deck = Deck(num_decks)
        self.reps = reps


    def run(self):
        for player in self.table.keys():
            row = self.table.get(player)
            row_list = []
            for dealer in row.keys():
                win_rate = self.simulate(dealer, player)
                row_list.append(round(win_rate, 3))
            self.table_relative[player] = row_list
            print("one row finished", player)
        Utility.create_output_html_file(self.table_relative, self.table, None, "output.html")


    def run_single(self, player, dealer):
        winrate_original_table = self.simulate(dealer, player)
        current = self.table.get(player)[dealer]

        alternative_action = Utility.get_and_change_to_complement_action(current, player, dealer, self.table)
        win_rate_new = self.simulate(dealer, player)

        print(f"Player: {player}\nDealer: {dealer}\nWinrate action of table ({current}): {winrate_original_table}\nWinrate alternative action ({alternative_action}): {win_rate_new}")

        print(f'Action from table is {winrate_original_table - win_rate_new} better')


    def run_full_comparison(self):
        for player in self.table.keys():
            if player == '17':
                break
            row = self.table.get(player)
            row_list = []
            row_full_comparison = []
            for dealer in row.keys():
                current = self.table.get(player)[dealer]
                win_rate_current = self.simulate(dealer, player)

                alternative_action = Utility.get_and_change_to_complement_action(current, player, dealer, self.table)
                win_rate_alternative = self.simulate(dealer, player)

                self.table.get(player)[dealer] = current
                if alternative_action == "same":
                    row_full_comparison.append(0.000)
                else:
                    row_full_comparison.append(round(win_rate_current - win_rate_alternative, 3))
                row_list.append(round(win_rate_current, 3))
            self.table_difference[player] = row_full_comparison
            self.table_relative[player] = row_list
            print("one row finished", player)
        Utility.create_output_html_file(self.table_relative, self.table, self.table_difference, "output_full_comparison.html")


    def run_game_simulation(self):
        wins = 0
        looses = 0
        for i in range(self.reps):
            next_card = self.deck.draw()
            first_card_player = next_card.rank
            next_card = self.deck.draw()
            card_dealer = next_card.rank
            next_card = self.deck.draw()
            second_card_player = next_card.rank
            if first_card_player in {'Jack', 'Queen', 'King'}:
                first_card_player = "10"
            if second_card_player in {'Jack', 'Queen', 'King'}:
                second_card_player = "10"
            if card_dealer in {'Jack', 'Queen', 'King'}:
                card_dealer = "10"
            if first_card_player == second_card_player:
                player = first_card_player + second_card_player
            else:
                player = Utility.add_values(first_card_player, second_card_player)
                player = Utility.get_value(player)
            
            w, l = self.do_one_turn(player, card_dealer)
            wins += w
            looses += l

            if self.deck.has_to_shuffle:
                self.deck.shuffle()

        print(f"{self.reps} number of games has been played\nPlayer wins: {wins}\nDealer wins: {looses}\nWinrate of player: {wins/(wins+looses)}")


    #TODO: Implement card counting
    def run_game_simulation_with_card_counting(self):
        wins = 0
        looses = 0
        betting_unit = 5
        x = 0
        times_played = 0
        for i in range(self.reps):
            if self.deck.units_to_bet < 0:
                x = 0
            else:
                x = self.deck.units_to_bet
                times_played +=1

            next_card = self.deck.draw()
            first_card_player = next_card.rank
            next_card = self.deck.draw()
            card_dealer = next_card.rank
            next_card = self.deck.draw()
            second_card_player = next_card.rank
            if first_card_player in {'Jack', 'Queen', 'King'}:
                first_card_player = "10"
            if second_card_player in {'Jack', 'Queen', 'King'}:
                second_card_player = "10"
            if card_dealer in {'Jack', 'Queen', 'King'}:
                card_dealer = "10"

            if first_card_player == second_card_player:
                player = first_card_player + second_card_player
            else:
                player = Utility.add_values(first_card_player, second_card_player)
                player = Utility.get_value(player)
            
            w, l = self.do_one_turn(player, card_dealer)
            wins += w * x*betting_unit
            looses += l * x*betting_unit

            if self.deck.has_to_shuffle:
                self.deck.shuffle()

        print(f"{self.reps} number of games has been played\n{times_played} number of times placed a bet\nPlayer wins: {wins}\nDealer wins: {looses}\nWinrate of player: {wins/(wins+looses)}")

    
    def simulate(self, dealer, player):
        wins = 0
        looses = 0
        for i in range(self.reps):
            w, l = self.do_one_turn(player, dealer)
            wins += w
            looses += l
            if self.deck.has_to_shuffle:
                self.deck.shuffle()

        return wins /(wins+looses)
    

    def do_one_turn(self, player, dealer):
        player_results = self.players_turn(player, dealer, False)
        dealer_result, is_black_dealer = self.dealer_turn(dealer)

        looses = 0
        wins = 0
        for (player_result, double, is_black_player) in player_results:
            if player_result > 21:
                looses += (1*double)
            elif is_black_dealer and is_black_player:
                pass
            elif is_black_dealer:
                looses += (1*double)
            elif is_black_player:
                wins += (1.5*double)
            elif dealer_result > 21:
                wins += (1*double)
            elif player_result > dealer_result:
                wins += (1*double)
            elif player_result < dealer_result:
                looses += (1*double)
            elif player_result == dealer_result:
                pass
            else:
                print(player_result, is_black_dealer, is_black_player, dealer_result) 
                print("Error ")
            return wins, looses


    def dealer_turn(self, dealer):
        hand_value = 0
        num_aces = 0
        card = dealer

        if card == 'A':
            num_aces += 1
            hand_value += 11
        elif card in {"King", "Queen", "Jack"}:
            hand_value += 10
        else: 
            hand_value += int(card)

        round = 1
        # Draw additional cards
        while hand_value < 17:
            card = self.deck.draw()
            card_value = card.rank
            if card_value == 'A':  # Ace
                num_aces += 1
                hand_value += 11
            elif card_value in {"King", "Queen", "Jack"}:
                hand_value += 10
            else:
                hand_value += int(card_value) 

            # Adjust for aces if necessary
            while hand_value > 21 and num_aces > 0:
                hand_value -= 10  # Convert ace from 11 to 1
                num_aces -= 1
            
            if round == 1 and hand_value == 21:
                return hand_value, True
            round +=1

        return hand_value, False
    

    
    def players_turn(self, player, dealer, is_split): 
        is_split = is_split
        player = player 
        round = 0
        no_bj = is_split

        if player.isdigit() and player == '21':
            return [(int(player), 1, True)]
        elif player == '1010':
            return [(20, 1, False)] 
        elif player.isdigit() and not all(elem == player[0] for elem in player) and int(player) >= 17:
            return [(int(player), 1, False)]
        elif len(player) > 1 and all(elem == player[0] for elem in player):
            no_bj = True

        if player == 'A6' or player == 'A7' and not is_split:
            print("works")

        while True:
            num, ace = Utility.extract_strings(player)
            if is_split:
                next_card = self.deck.draw()
                card_value = next_card.rank
                if card_value == player:
                    player = player + card_value
                    p = self.table.get(player)
                    action = p.get(dealer)
                else:
                    value = Utility.add_values(player, card_value)
                    real_value = Utility.get_value(value)
                    player = real_value
                    action = ''
                is_split = False
                round += 1
            elif len(ace) == 0 and int(num) < 7:
                action = 'H'
            else:
                p = self.table.get(player)
                action = p.get(dealer)
                if round > 0 and action == 'D':
                    action = 'H'

            if action == "H":
                if all(elem == player[0] for elem in player) and len(player) > 1 and player != 'AA' and player != '11':
                    player = str(sum(int(x) for x in player))
                next_card = self.deck.draw()
                card_value = next_card.rank
                value = Utility.add_values(player, card_value)
                real_value = Utility.get_value(value)
                player = real_value
            elif action == "S":
                if all(elem == player[0] for elem in player) and len(player) > 1 and player != 'AA' and player != '11':
                    player = str(sum(int(x) for x in player))
                return [(int(Utility.get_value(player)), 1, False)]
            elif action == "P":
                res1 = self.players_turn(player[0], dealer, True)
                res2 = self.players_turn(player[1], dealer, True)
                return res1 + res2
            elif action == "D":
                if all(elem == player[0] for elem in player) and player != '11':
                    player = str(sum(int(x) for x in player))
                next_card = self.deck.draw()
                card_value = next_card.rank
                value = Utility.add_values(player, card_value)
                real_value = Utility.get_value(value)
                player = real_value
                num, ace = Utility.extract_strings(player)
                res = int(num) + len(ace)
                return [(res, 2, False)]

            num, ace = Utility.extract_strings(player)
            if round == 1 and int(num) == 21 and not no_bj:
                return [(int(player), 1, True)]
            
            if len(num)>1 and int(num) >= 17:
                return [(int(num), 1, False)]
            
            round += 1

        
class Test:

    def main(self):
        simulator = Simulator(num_decks=6, reps=100000)
        simulator.run()

    def test1(self):
        simulator = Simulator(num_decks=6, reps=100000)
        player_results = simulator.players_turn("11", "6", False)
        dealer_result = simulator.dealer_turn("6")
        print(player_results)
        print(dealer_result)

    def single_comparison(self):
        simulator = Simulator(num_decks=6, reps=1000000)
        simulator.run_single("16", "7")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Blackjack simulation')
    # Add command-line options
    parser.add_argument('-m', '--mode', default="single", help='Specify mode <single> comparison or <whole> table')
    parser.add_argument('-p', '--player', default="10", help='player hand')
    parser.add_argument('-d', '--dealer', default="10", help='dealer hand')
    parser.add_argument('-nd', '--num_decks', type=int, default=6, help='Specify number of decks')
    parser.add_argument('-r', '--reps', type=int, default=100000, help='Specify number of repitions')

    # Parse the command-line arguments
    args = parser.parse_args()

    simulator = Simulator(num_decks=args.num_decks, reps=args.reps)

    if args.mode == 'single':
        simulator.run_single(args.player, args.dealer)
    elif args.mode == 'whole':
        simulator.run()
    elif args.mode == 'full_compare':
        simulator.run_full_comparison()
    elif args.mode == 'game':
        simulator.run_game_simulation()
    elif args.mode == 'card_counting':
        simulator.run_game_simulation_with_card_counting()

    # Ex: python3 bj_simulation.py -m single -nd 6 -r 100000 -p 16 -d 10
    # Ex: python3 bj_simulation.py -m whole -nd 6 -r 100000
    # Ex: python3 bj_simulation.py -m full_compare -nd 6 -r 100000
    # Ex: python3 bj_simulation.py -m game -nd 6 -r 100000
    # Ex: python3 bj_simulation.py -m card_counting -nd 6 -r 10000000
    


