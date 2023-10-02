import random
import time

# Version: 2.0

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
    (1, 1, 1, 1, 1, 1): 4000,
}

def roll_dice(num=6):
    return tuple(random.choice(range(1, 7)) for _ in range(num))

def calculate_score(dice):
    score = 0
    for combo, combo_score in SCORING_RULES.items():
        if all(dice.count(d) >= combo.count(d) for d in combo):
            score += combo_score
    return score

def player_turn():
    remaining_dice = 6
    turn_score = 0
    while remaining_dice > 0:
        roll = roll_dice(remaining_dice)
        print(f"\nCurrent roll: {roll}")
        
        choices = input("Which dice do you want to keep? (enter space-separated numbers, 'done' to end turn, or 'exit' to quit game): ").lower().split()

        if "exit" in choices:
            print("Thank you for playing! Goodbye!")
            exit()

        if "done" in choices:
            return turn_score

        # Calculate score based on player's choices
        chosen_dice = tuple(map(int, choices))
        score_for_this_roll = calculate_score(chosen_dice)
        if score_for_this_roll == 0:
            print("\nFarkle!\n")
            return 0

        turn_score += score_for_this_roll

        for d in chosen_dice:
            roll = list(roll)
            roll.remove(d)
            remaining_dice -= 1

        if remaining_dice == 0:
            remaining_dice = 6

        print(f"You kept: {chosen_dice} - Current turn score: {turn_score}")

def computer_turn():
    remaining_dice = 6
    turn_score = 0
    while remaining_dice > 0:
        roll = roll_dice(remaining_dice)
        print(f"\nComputer rolled: {roll}")
        time.sleep(2)

        scoring_dice = [d for d in roll if calculate_score((d,)) > 0]
        if not scoring_dice:
            print("\nFarkle!\n")
            return 0

        turn_score += calculate_score(roll)
        
        for d in scoring_dice:
            roll = list(roll)
            roll.remove(d)
            remaining_dice -= 1

        if remaining_dice == 0:
            remaining_dice = 6

        print(f"Computer kept: {scoring_dice} - Current turn score: {turn_score}")
        time.sleep(1)

    return turn_score

def display_rules():
    print("""
Welcome to Farkle!

Scoring Rules:
1 - 100 points
5 - 50 points
Three of a Kind (e.g., 1,1,1) - Based on the number (Three 1's: 1000, Three 2's: 200, etc.)
Four of a Kind (e.g., 1,1,1,1) - Double the Three of a Kind score
Five of a Kind - Triple the Three of a Kind score
Six of a Kind - Quadruple the Three of a Kind score

You can choose to keep rolling the dice for more points, but if you roll and don't score, you Farkle and lose your turn's points!

At any point, enter 'done' to end your turn or 'exit' to quit the game.

The first player to reach 10,000 points wins!

Let's get started!
""")

def main():
    display_rules()
    
    action = input("Do you want to 'play' or 'exit'? ").lower()
    if action == 'exit':
        print("Thank you for checking out Farkle! Goodbye!")
        return

    player_score = 0
    computer_score = 0

    while player_score < 10000 and computer_score < 10000:
        print(f"\nCurrent Scores - You: {player_score}, Computer: {computer_score}\n")
        
        player_score += player_turn()
        print(f"\nEnd of Your Turn - Your score: {player_score}\n")
        
        computer_score += computer_turn()
        print(f"\nEnd of Computer's Turn - Computer score: {computer_score}\n")

    if player_score >= 10000:
        print("\nCongratulations! You won!")
    else:
        print("\nComputer wins. Better luck next time!")

if __name__ == "__main__":
    main()
