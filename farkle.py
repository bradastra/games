import random
import time

# Scoring rules
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
    (1, 2, 3, 4, 5, 6): 1500,
    (1, 1, 2, 2, 3, 3): 1500,
    (4, 4, 5, 5, 6, 6): 1500
}

def roll_dice(num=6):
    return [random.choice(range(1, 7)) for _ in range(num)]

def calculate_score(dice):
    dice = sorted(dice)
    score = 0
    used_dice = []
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
            print("Farkle! You lose all points from this turn.")
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

def computer_turn():
    remaining_dice = 6
    turn_score = 0
    while remaining_dice > 0:
        roll = roll_dice(remaining_dice)
        print(f"\nComputer rolled: {roll}")
        time.sleep(2)

        scoring_dice = [d for d in roll if d == 1 or d == 5]
        if not scoring_dice:
            print("\nFarkle!\n")
            return 0

        score_this_roll = calculate_score(scoring_dice)
        turn_score += score_this_roll

        for d in scoring_dice:
            roll.remove(d)
            remaining_dice -= 1

        if not remaining_dice:
            remaining_dice = 6

        print(f"Computer kept: {scoring_dice} - Current turn score: {turn_score}")
        time.sleep(1)

    return turn_score

def display_rules():
    # Display rules as previously defined
    print("\nWelcome to Farkle!")
    print("Here are the basic rules:")
    # You can fill in other rules or scoring details here.

def main():
    display_rules()
    player_score = 0
    computer_score = 0
    while True:
        player_score += player_turn()
        print(f"\nYour total score: {player_score}")
        computer_score += computer_turn()
        print(f"Computer's total score: {computer_score}")
        
        if player_score > 10000 or computer_score > 10000:
            break

    if player_score > computer_score:
        print("\nCongratulations! You won!")
    else:
        print("\nSorry, the computer won this time.")

if __name__ == "__main__":
    main()

