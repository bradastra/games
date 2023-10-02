import random
import time

# Constants for scoring thresholds and win condition
ENTRY_THRESHOLD = 500
WINNING_SCORE = 10000

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
    (1, 2, 3, 4, 5, 6): 1500,
    (2, 3, 4, 5, 6, 6): 2500  # two triplets
}

def roll_dice(n):
    """Roll n dice and return the result as a tuple."""
    return tuple(random.randint(1, 6) for _ in range(n))

def calculate_score(dice):
    """Calculate the score for a given dice combination."""
    dice = list(dice)
    score = 0
    for combo, combo_score in SCORING_RULES.items():
        while all(combo.count(die) <= dice.count(die) for die in combo):
            score += combo_score
            for die in combo:
                dice.remove(die)
    return score

def computer_turn_strategy(roll, computer_score, player_score):
    """Determine which dice the computer should keep."""
    score = calculate_score(roll)
    dice_left = len(roll)
    
    # Always keep dice if it's a high scoring roll
    if score >= 500:
        return roll
    
    # If computer is trailing, take more risk
    if computer_score < player_score:
        if dice_left >= 4:
            return [die for die in roll if die == 1 or die == 5]
        if dice_left == 3 and (1 in roll or 5 in roll):
            return roll
    else:
        if dice_left >= 5:
            return [die for die in roll if die == 1 or die == 5]
        if dice_left == 4 and (1 in roll or 5 in roll):
            return roll

    # If none of the conditions are met, keep everything
    return roll

def main():
    player_score = 0
    computer_score = 0
    in_game = False

    print("Welcome to Farkle!")
    play_choice = input("Would you like to play? (yes/no): ").lower()

    if play_choice != "yes":
        print("Thanks for stopping by!")
        return

    while player_score < WINNING_SCORE and computer_score < WINNING_SCORE:
        # Player's turn
        print("\nYour turn!")
        dice = roll_dice(6)
        print(f"Current roll: {dice}")
        kept_dice = list(map(int, input("Which dice do you want to keep? (enter space-separated numbers or 'done'): ").split()))
        
        if not kept_dice:
            print("You rolled a Farkle!")
            continue

        player_score += calculate_score(kept_dice)
        if player_score >= ENTRY_THRESHOLD:
            in_game = True

        # Computer's turn
        print("\nComputer's turn!")
        dice = roll_dice(6)
        print(f"Computer rolled: {dice}")
        time.sleep(2)  # Pause for 2 seconds to let the player see the roll
        
        kept_dice = computer_turn_strategy(dice, computer_score, player_score)
        
        computer_score += calculate_score(kept_dice)
        print(f"Computer kept: {kept_dice}")
        time.sleep(2)  # Pause for 2 seconds to let the player see the kept dice
        
        print(f"Computer's total score: {computer_score}")

    if player_score >= WINNING_SCORE:
        print("\nCongratulations! You won!")
    else:
        print("\nSorry, the computer won!")

if __name__ == "__main__":
    main()

