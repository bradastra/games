import random
import time

# Define scoring rules
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
    (1, 1, 1, 1): 2000,
    (1, 1, 1, 1, 1): 3000,
    (1, 1, 1, 1, 1, 1): 4000,
    (2, 2, 2, 2): 400,
    (2, 2, 2, 2, 2): 600,
    (2, 2, 2, 2, 2, 2): 800,
    (3, 3, 3, 3): 600,
    (3, 3, 3, 3, 3): 900,
    (3, 3, 3, 3, 3, 3): 1200,
    (4, 4, 4, 4): 800,
    (4, 4, 4, 4, 4): 1200,
    (4, 4, 4, 4, 4, 4): 1600,
    (5, 5, 5, 5): 1000,
    (5, 5, 5, 5, 5): 1500,
    (5, 5, 5, 5, 5, 5): 2000,
    (6, 6, 6, 6): 1200,
    (6, 6, 6, 6, 6): 1800,
    (6, 6, 6, 6, 6, 6): 2400,
    # Full house (three of a kind + pair). Score: 750
}

# Adding full house combinations to SCORING_RULES
for three_of_a_kind in range(1, 7):
    for pair in range(1, 7):
        if three_of_a_kind != pair:  # Can't be the same number
            SCORING_RULES[(three_of_a_kind,) * 3 + (pair,) * 2] = 750

def roll_dice(num=6):
    return tuple(random.choice(range(1, 7)) for _ in range(num))

def calculate_score(dice):
    score = 0
    for combo, combo_score in SCORING_RULES.items():
        if all(dice.count(d) >= combo.count(d) for d in combo):
            score += combo_score
    return score

def computer_turn(total_score):
    remaining_dice = 6
    turn_score = 0
    while remaining_dice > 0:
        roll = roll_dice(remaining_dice)
        print(f"Computer rolled: {roll}")
        time.sleep(2)  # Add suspense with a pause

        # Find all scoring dice
        scoring_dice = [d for d in roll if calculate_score((d,)) > 0]
        if not scoring_dice:
            print("\nFARKLE! Oh, what a devastating turn of events for the computer!\n")
            return 0

        # Decide to keep rolling or stop based on some simple strategy
        if total_score + turn_score < 500:
            # Always roll if not in the game yet
            turn_score += calculate_score(roll)
        elif len(scoring_dice) > 3 or random.random() < 0.5:
            # Take a risk if there's a good number of scoring dice or 50% chance
            turn_score += calculate_score(roll)
        else:
            # Otherwise end the turn
            return turn_score

        # Remove scoring dice and continue
        for d in scoring_dice:
            roll = list(roll)
            roll.remove(d)
            remaining_dice -= 1

        # Reset dice count if all are used
        if remaining_dice == 0:
            remaining_dice = 6

        print(f"Computer kept: {scoring_dice} - Current turn score: {turn_score}")
        time.sleep(1)

    return turn_score

def player_turn():
    remaining_dice = 6
    turn_score = 0
    while remaining_dice > 0:
        roll = roll_dice(remaining_dice)
        print(f"Current roll: {roll}")
        
        choices = input("Which dice do you want to keep? (enter space-separated numbers or 'done'): ").split()
        if "done" in choices:
            break

        # Calculate score based on player's choices
        chosen_dice = tuple(map(int, choices))
        score_for_this_roll = calculate_score(chosen_dice)
        if score_for_this_roll == 0:
            print("\nInvalid choice! Those dice don't score.\n")
            continue

        turn_score += score_for_this_roll

        # Remove chosen dice and continue
        for d in chosen_dice:
            roll = list(roll)
            roll.remove(d)
            remaining_dice -= 1

        # Reset dice count if all are used
        if remaining_dice == 0:
            remaining_dice = 6

        print(f"You kept: {chosen_dice} - Current turn score: {turn_score}")

        # Check for Farkle
        if calculate_score(roll) == 0:
            print("\nFARKLE! Oh, the sheer devastation of it all!\n")
            return 0
        
        # Ask player to roll again or stay
        action = input("Do you want to 'roll' again or 'stay'? ").lower()
        if action == "stay":
            break

    return turn_score

def display_rules():
    print("The scoring rules are:")
    for combo, score in SCORING_RULES.items():
        print(f"{combo}: {score} points")
    print()

def main():
    display_rules()

    player_score = 0
    computer_score = 0

    while player_score < 10000 and computer_score < 10000:
        print(f"\nCurrent Scores - You: {player_score}, Computer: {computer_score}\n")
        
        player_score += player_turn()
        print(f"\nEnd of Your Turn - Your score: {player_score}\n")
        
        computer_score += computer_turn(computer_score)
        print(f"\nEnd of Computer's Turn - Computer score: {computer_score}\n")

    # Announce winner
    if player_score >= 10000:
        print("\nCongratulations! You won!")
    else:
        print("\nComputer wins. Better luck next time!")

if __name__ == "__main__":
    main()

