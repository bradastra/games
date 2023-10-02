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
    # Adding the more complex rules
    # Four of a kind, five of a kind, six of a kind
    (1, 1, 1, 1): 2000,
    (1, 1, 1, 1, 1): 3000,
    (1, 1, 1, 1, 1, 1): 4000
}

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

    return turn_score

def display_rules():
    print("The scoring rules are:")
    for combo, score in SCORING_RULES.items():
        print(f"{combo}: {score} points")
    print("\nThe first player to reach 10,000 points wins!\n")

def main():
    player_score, computer_score = 0, 0
    print("Welcome to Farkle!")
    play_choice = input("Would you like to play? (yes/no): ")
    if play_choice.lower() != "yes":
        return

    display_rules()

    while player_score < 10000 and computer_score < 10000:
        print("\nYour turn!")
        player_score += player_turn()
        print(f"Your total score: {player_score}")
        if player_score >= 10000:
            break

        print("\nComputer's turn!")
        computer_score += computer_turn(computer_score)
        print(f"Computer's total score: {computer_score}")

    print("Game over!")
    if player_score > computer_score:
        print("Congratulations! You win!")
    else:
        print("Computer wins!")

if __name__ == "__main__":
    main()

