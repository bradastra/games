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
    (1, 2, 3, 4, 5, 6): 1500
}

def roll_dice(num=6):
    return tuple(random.randint(1, 6) for _ in range(num))

def calculate_score(dice):
    score = 0
    dice_counts = {i: dice.count(i) for i in set(dice)}

    for combo, points in SCORING_RULES.items():
        if all(dice_counts.get(d, 0) >= combo.count(d) for d in combo):
            score += points

    return score

def player_turn():
    total_score = 0
    dice_left = 6

    while dice_left > 0:
        current_roll = roll_dice(dice_left)
        print(f"Current roll: {current_roll}")

        while True:
            selected_values = input("Which dice do you want to keep? (enter space-separated numbers or 'done'): ").split()
            if selected_values == ['done']:
                return total_score

            if not all(value.isdigit() for value in selected_values):
                print("Please enter valid dice numbers or 'done'.")
                continue

            try:
                selected_values = tuple(current_roll[int(val) - 1] for val in selected_values)
                if len(set(selected_values)) != len(selected_values):
                    raise IndexError
            except (ValueError, IndexError):
                print("Invalid choice. Ensure you select dice numbers only from the current roll and don't duplicate. Try again.")
                continue

            score = calculate_score(selected_values)
            if score == 0:
                print("The selected dice don't give any score. Try again.")
                continue

            total_score += score
            dice_left -= len(selected_values)

    return total_score

def computer_turn():
    total_score = 0
    dice_left = 6

    while total_score < 300 and dice_left > 0:
        current_roll = roll_dice(dice_left)
        score = calculate_score(current_roll)
        total_score += score
        print(f"Computer rolled: {current_roll} - Score: {score}")
        dice_left -= len(current_roll)  # assumes computer keeps all dice it rolls

    return total_score

def display_rules():
    print("--- FARKLE RULES & INSTRUCTIONS ---")
    print("Objective: Be the first to score 10,000 points.")
    print("Gameplay:")
    print("1. Roll all six dice.")
    print("2. After each roll, choose the dice you want to keep (the ones that give you scores).")
    print("3. You can continue rolling the remaining dice to accumulate more points, but if a roll results in zero points, you lose all points accumulated in that turn.")
    print("4. You decide when to stop rolling and keep the points you've accumulated.")
    print("\nScoring:")
    for combo, score in SCORING_RULES.items():
        print(f"{combo}: {score} points")
    print("------------------------------------\n")

def play_again_prompt():
    """Prompts the player to either play again or exit the game."""
    time.sleep(2)  # Wait for 2 seconds before asking
    while True:
        choice = input("Play Again? Y / N (or X to exit): ").lower()
        if choice == 'y':
            return True
        elif choice == 'n' or choice == 'x':
            return False
        else:
            print("Invalid choice. Please choose Y, N, or X.")

def main():
    display_rules()

    while True:
        player_score, computer_score = 0, 0

        while player_score < 10000 and computer_score < 10000:
            player_score += player_turn()
            print(f"Your turn ended with {player_score} points.")

            computer_score += computer_turn()
            print(f"Computer's turn ended with {computer_score} points.")

        winner = "Player" if player_score >= 10000 else "Computer"
        print(f"{winner} wins!")

        if not play_again_prompt():
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
