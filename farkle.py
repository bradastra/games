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
    for combo, points in SCORING_RULES.items():
        if all(dice.count(d) >= combo.count(d) for d in combo):
            score += points
            for d in combo:
                dice.remove(d)

    return score

def player_turn():
    remaining_dice = 6
    turn_total = 0

    while remaining_dice > 0:
        current_roll = roll_dice(remaining_dice)
        print(f"Current roll: {current_roll}")

        chosen_dice = input("Which dice do you want to keep? (enter space-separated numbers or 'done'): ").split()

        if "done" in chosen_dice:
            break

        valid_choice = all(current_roll.count(int(d)) >= chosen_dice.count(d) for d in chosen_dice)
        if valid_choice:
            score = calculate_score(list(map(int, chosen_dice)))
            if score == 0:
                return 0
            turn_total += score
            remaining_dice -= len(chosen_dice)
        else:
            print("Invalid choice. Ensure you select dice numbers only from the current roll and don't duplicate. Try again.")

    return turn_total

def computer_turn():
    # A very basic strategy for the computer: roll, take all points, and stop.
    dice = roll_dice()
    return calculate_score(list(dice))

def display_rules():
    print("--- FARKLE RULES & INSTRUCTIONS ---")
    print("Objective: Be the first to score 10,000 points.")
    print("Gameplay:")
    print("1. Roll all six dice.")
    print("2. After each roll, choose the dice you want to keep (the ones that give you scores).")
    print("3. You can continue rolling the remaining dice to accumulate more points, but if a roll results in zero points, you lose all points accumulated in that turn.")
    print("4. You decide when to stop rolling and keep the points you've accumulated.")
    print("\nScoring:")
    for combo, points in SCORING_RULES.items():
        print(f"{combo}: {points} points")

def play_game():
    player_score = 0
    computer_score = 0

    while player_score < 10000 and computer_score < 10000:
        print("\nYour turn!")
        player_score += player_turn()
        print(f"Your turn ended with {player_score} points.\n")

        print("Computer's turn...")
        computer_score += computer_turn()
        print(f"Computer's turn ended with {computer_score} points.\n")

    if player_score >= 10000:
        print("You Win!")
    else:
        print("Computer Wins!")
    time.sleep(2)

def main():
    print("Welcome to Farkle!")
    time.sleep(2)
    display_rules()
    play_choice = input("\nWould you like to play? (Y to start / X to exit): ").lower()

    while play_choice == 'y':
        play_game()
        play_choice = input("\nPlay Again? Y / N (or X to exit): ").lower()

    print("\nThank you for playing Farkle! It was a pleasure to have you.")
    print("- bradastra")
    print("\nP.S. Check out my Instagram profile: @bradastra.ai. Hope to see you there!")

if __name__ == "__main__":
    main()

