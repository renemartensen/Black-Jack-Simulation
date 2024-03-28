# Black Jack Simulation Program

This program simulates the game of Blackjack and provides analytical features to assess optimal strategies and win rates. It includes functionalities to find win rates based on an optimal decision table provided by a casino, compare suggested decisions from the optimal table against complementary decisions, and determine win rates based on the decision table. Additionally, it supports the determination of win rates following the high-low counting strategy.

## Features

- **Optimal Decision Table Analysis:** Find win rates of different card match-ups when following the suggestions from an optimal decision table provided by a casino.
  
- **Decision Comparison:** Compare the suggested decisions from the optimal decision table against complementary decisions to verify the table. (Table turns out not to be optimal)
  
- **Win Rate Calculation:** Determine the win rate when playing according to the decision table
  
- **High-Low Counting Strategy:** Calculate the win rate following the high-low counting strategy suggestions from the decision table.

## Installation

1. Clone the repository: git clone ""
2. Install dependencies: pip install -r requirements.txt
3. Run the program: python blackjack_simulation.py -m MODE [-p PLAYER_HAND] [-d DEALER_HAND] -nd NUM_DECKS -r REPS
**Options:**
- `-m, --mode`: Specify mode (`single`, `whole`, `full_compare`, `game`, `card_counting`)
- `-p, --player`: Specify player hand
- `-d, --dealer`: Specify dealer hand
- `-nd, --num_decks`: Specify number of decks (default=6)
- `-r, --reps`: Specify number of repetitions (default=100000)

**Example ('card_counting'):**
python3 bj_simulation.py -m card_counting -nd 6 -r 10000000


## Requirements

- Python 3.x
- Required Python packages listed in `requirements.txt`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.# Black-Jack-Simulation
