import random
import time

# ... [unchanged code]

def player_turn():
    # ... [unchanged code]

# New Strategy and Turn Functions
def computer_strategy(player_score, computer_score):
    score_difference = computer_score - player_score
    if score_difference > 1000:
        return "conservative"
    elif score_difference < -1000:
        return "aggressive"
    else:
        return "balanced"

def computer_turn(player_score, computer_score):
    total_turn_score = 0
    strategy = computer_strategy(player_score, computer_score)

    while True:
        dice = roll_dice()
        score = calculate_score(list(dice))

        if score == 0: # Farkle!
            return 0

        total_turn_score += score

        if strategy == "conservative" and total_turn_score >= 300:
            return total_turn_score
        elif strategy == "aggressive" and (total_turn_score >= 1000 or len(dice) < 3):
            return total_turn_score
        elif strategy == "balanced" and (total_turn_score >= 500 or len(dice) < 2):
            return total_turn_score
        
        # Introduce a small randomness factor so the computer doesn't always act predictably
        if random.randint(0, 10) < 2: # 20% chance the computer decides to stop early
            return total_turn_score

# Updated play_game function
def play_game():
    player_score = 0
    computer_score = 0

    while player_score < 10000 and computer_score < 10000:
        print("\nYour turn!")
        player_score += player_turn()
        print(f"Your turn ended with {player_score} points.\n")

        print("Computer's turn...")
        # Updated the following line to pass scores to the computer's turn
        computer_score += computer_turn(player_score, computer_score)
        print(f"Computer's turn ended with {computer_score} points.\n")

    # ... [rest of the code remains unchanged]

# ... [rest of the code, like display_rules, main, etc.]

if __name__ == "__main__":
    main()

