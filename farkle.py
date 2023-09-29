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

    if player_score >= 10000:
        print("Congratulations! You win!")
    else:
        print("Computer wins! Better luck next time.")

def display_rules():
    print("Welcome to Farkle!")
    print("\nThe scoring rules are:")
    for combo, score in SCORING_RULES.items():
        print(f"{combo}: {score} points")
    print("\nThe first player to reach 10,000 points wins!")

def main():
    display_rules()
    play_game()

if __name__ == "__main__":
    main()
