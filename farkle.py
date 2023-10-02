# farkle.py

import random
import time

# Game rules & scoring
RULES = """Rules & Scoring:
1: 100 points
5: 50 points
Three 1's: 1000 points
Three 2's: 200 points
Three 3's: 300 points
Three 4's: 400 points
Three 5's: 500 points
Three 6's: 600 points
Four or more of any number: Double the three of a kind score for each extra number.
Press 'r' anytime during the game to see these rules again.
"""

SCORING_RULES = {
    (1,): 100,
    (5,): 50,
    (1, 1, 1): 1000,
    (2, 2, 2): 200,
    (3, 3, 3): 300,
    (4, 4, 4): 400,
    (5, 5, 5): 500,
    (6, 6, 6): 600,
    (1, 1, 1, 1): 2000,
    (2, 2, 2, 2): 400,
    (3, 3, 3, 3): 600,
    (4, 4, 4, 4): 800,
    (5, 5, 5, 5): 1000,
    (6, 6, 6, 6): 1200,
    (1, 1, 1, 1, 1): 3000,
    (2, 2, 2, 2, 2): 500,
    (3, 3, 3, 3, 3): 750,
    (4, 4, 4, 4, 4): 1000,
    (5, 5, 5, 5, 5): 1250,
    (6, 6, 6, 6, 6): 1500,
    (1, 1, 1, 1, 1, 1): 4000,
    (2, 2, 2, 2, 2, 2): 1600,
    (3, 3, 3, 3, 3, 3): 1800,
    (4, 4, 4, 4, 4, 4): 2000,
    (5, 5, 5, 5, 5, 5): 2200,
    (6, 6, 6, 6, 6, 6): 2400,
    (1, 2, 3, 4, 5, 6): 1500, # Run: 1, 2, 3, 4, 5, 6
    (1, 1, 2, 2, 3, 3): 1500,
    (4, 4, 5, 5, 6, 6): 1500
}

def roll_dice(num=6):
    return [random.choice(range(1, 7)) for _ in range(num)]

def calculate_score(dice):
    dice = sorted(dice)
    score = 0
    for combination, combination_score in sorted(SCORING_RULES.items(), key=lambda x: len(x[0]), reverse=True):
        while all(dice.count(die) >= combination.count(die) for die in combination):
            score += combination_score
            for die in combination:
                dice.remove(die)
    return score

def choose_dice_to_keep(rolled_dice):
    while True:
        try:
            kept_dice = input("Enter dice to keep (e.g. 456): ")
            kept_dice_list = [int(die) for die in kept_dice]
            if all(die in rolled_dice for die in kept_dice_list):
                return kept_dice_list
            else:
                print("You can only choose dice that you rolled.")
        except ValueError:
            print("Please enter valid dice numbers.")

def player_turn():
    total_turn_score = 0
    remaining_dice = 6
    input("\nYour turn! Press Enter to roll the dice...")
    while remaining_dice > 0:
        rolled_dice = roll_dice(remaining_dice)
        print(f"\nYou rolled: {rolled_dice}")

        kept_dice = choose_dice_to_keep(rolled_dice)
        score_this_roll = calculate_score(kept_dice)

        if score_this_roll == 0:
            print("Farkle!")
            return 0

        total_turn_score += score_this_roll
        print(f"Score this roll: {score_this_roll}")

        for die in kept_dice:
            rolled_dice.remove(die)
        remaining_dice -= len(kept_dice)

        if not remaining_dice:
            remaining_dice = 6

        action = input("\nDo you want to (P)ass or (R)oll again? ").upper()
        if action == 'P':
            return total_turn_score

def enhanced_computer_turn():
    dice = 6
    total_round_score = 0

    while dice:
        roll = roll_dice(dice)
        print(f"\nComputer rolled: {roll}")
        possible_scores = calculate_possible_scores(roll)
        
        if not possible_scores:
            print("Computer got a Farkle!")
            return 0

        # Select highest scoring combination
        selected_score = max(possible_scores, key=possible_scores.get)
        total_round_score += possible_scores[selected_score]
        print(f"Computer decides to keep {', '.join(map(str, selected_score))} for {possible_scores[selected_score]} points.")

        dice -= len(selected_score)

        # Decision making
        if total_round_score > 1000:
            print(f"Computer decides to pass with a total round score of {total_round_score}.")
            return total_round_score

        if computer_score + total_round_score > 9500 and total_round_score > 300:
            print(f"Computer decides to pass and get closer to winning with a total round score of {total_round_score}.")
            return total_round_score

        if total_round_score > 500 and dice <= 3:
            print(f"Computer decides to pass with a decent score and not risk it with only {dice} dice left.")
            return total_round_score

        print(f"Computer decides to roll again despite getting {total_round_score} in this round.")
    
    return total_round_score

def display_rules():
    print("\nWelcome to Farkle!")
    print(RULES)

def main():
    display_rules()
    player_score = 0
    computer_score = 0
    while True:
        player_score += player_turn()
        print(f"\nYour total score: {player_score}")

        # Computer's turn
        computer_score += enhanced_computer_turn(player_score, computer_score)
        print(f"Computer's total score: {computer_score}")

        # Check if player has reached 10,000 and give computer a last turn
        if player_score >= 10000:
            print("\nYou've reached 10,000 points! Computer will now take its final turn.")
            computer_score += enhanced_computer_turn(player_score, computer_score)
            print(f"Computer's final score: {computer_score}")
            break

        # Check if computer has reached 10,000 and give player a last turn
        if computer_score >= 10000:
            print("\nComputer has reached 10,000 points! You will now take your final turn.")
            player_score += player_turn()
            print(f"Your final score: {player_score}")
            break

    if player_score > computer_score:
        print("\nCongratulations! You won!")
    else:
        print("\nSorry, the computer won this time.")

if __name__ == "__main__":
    main()
