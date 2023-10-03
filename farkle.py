import random
import time

RULES = """
Rules & Scoring:
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

def roll_dice(num_dice):
    return [random.randint(1, 6) for _ in range(num_dice)]

def calculate_score(rolled_dice):
    score = 0
    dice_counts = [rolled_dice.count(i) for i in range(1, 7)]

    scoring_funcs = [
        (lambda count: count * 1000, 1000),    # For three 1's
        (lambda count: count * 200, 200),      # For three 2's
        (lambda count: count * 300, 300),      # For three 3's
        (lambda count: count * 400, 400),      # For three 4's
        (lambda count: count * 500, 500),      # For three 5's
        (lambda count: count * 600, 600)       # For three 6's
    ]

    for i, (func, base_score) in enumerate(scoring_funcs):
        if dice_counts[i] >= 3:
            score += func(dice_counts[i] - 2)

    score += dice_counts[0] * 100  # For individual 1's
    score += dice_counts[4] * 50   # For individual 5's

    return score

def player_turn():
    remaining_dice = 6
    total_round_score = 0
    while True:
        rolled_dice = roll_dice(remaining_dice)
        print(f"\nYou rolled: {rolled_dice}")
        
        potential_score = calculate_score(rolled_dice)
        if potential_score == 0:
            return 0
        
        while True:
            kept_dice = input("Enter dice to keep (e.g. 456): ")
            kept_dice = [int(i) for i in kept_dice if i.isdigit() and int(i) in rolled_dice]

            if kept_dice:
                break_score = calculate_score(kept_dice)
                if break_score > 0:
                    break
        
        total_round_score += break_score
        remaining_dice -= len(kept_dice)
        print(f"Score this roll: {break_score}")
        
        if remaining_dice == 0:
            remaining_dice = 6
        
        action = input("\nDo you want to (P)ass or (R)oll again? ").upper()
        if action == 'P':
            return total_round_score

def enhanced_computer_turn(player_score, computer_score):
    total_turn_score = 0
    remaining_dice = 6
    while True:
        rolled_dice = roll_dice(remaining_dice)
        print(f"\nComputer rolled: {rolled_dice}")
        time.sleep(2)

        potential_score = calculate_score(rolled_dice)
        if potential_score == 0:
            print("Computer got a Farkle!")
            return 0

        # Improved strategy: The computer will play it safe after reaching a score of 500 or more in a turn
        if total_turn_score + potential_score >= 500:
            total_turn_score += potential_score
            print(f"Computer adds {potential_score} to its total score.")
            return total_turn_score
        elif potential_score < 300 or computer_score + total_turn_score + potential_score < player_score:
            print(f"Computer decides to roll again despite getting {potential_score} in this roll.")
            total_turn_score += potential_score
            if remaining_dice <= 3:
                remaining_dice = 6
        else:
            total_turn_score += potential_score
            print(f"Computer adds {potential_score} to its total score.")
            return total_turn_score

def display_rules():
    print("\nWelcome to Farkle!")
    print(RULES)

def main():
    display_rules()
    player_score = 0
    computer_score = 0
    while True:
        print(f"\nYour score: {player_score} | Computer's score: {computer_score}\n")
        print("Your turn! Press Enter to roll the dice...")
        input()
        player_score += player_turn()
        print(f"Your total score: {player_score}")
        
        print("\nComputer's turn...")
        computer_score += enhanced_computer_turn(player_score, computer_score)
        print(f"Computer's total score: {computer_score}")

if __name__ == "__main__":
    main()
