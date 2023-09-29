import random

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
    """Roll a specified number of dice and return their values."""
    return tuple(random.randint(1, 6) for _ in range(num))

def get_score(dice):
    """Calculate the score for a given dice roll."""
    score = 0
    dice_counts = {i: dice.count(i) for i in set(dice)}

    for combo, points in SCORING_RULES.items():
        if all(dice_counts.get(d, 0) >= combo.count(d) for d in combo):
            score += points

    return score

def player_turn():
    """Execute the player's turn."""
    total_score = 0
    dice_left = 6

    while dice_left > 0:
        roll = roll_dice(dice_left)
        print(f"Current roll: {roll}")

        while True:
            selected_values = input("Which dice do you want to keep? (enter space-separated numbers or 'done'): ").split()
            if selected_values == ['done']:
                return total_score

            selected_values = tuple(map(int, selected_values))
            if set(selected_values).issubset(roll) and get_score(selected_values) > 0:
                dice_left -= len(selected_values)
                total_score += get_score(selected_values)
                break
            else:
                print("The selected dice don't give any score. Try again.")

    return total_score

def computer_turn():
    """Execute the computer's turn."""
    total_score = 0
    dice_left = 6

    while total_score < 300 and dice_left > 0:
        roll = roll_dice(dice_left)
        score = get_score(roll)
        total_score += score
        print(f"Computer rolled: {roll} - Score: {score}")
        dice_left -= len(roll)  # assumes computer keeps all dice it rolls

    return total_score

def display_rules():
    """Display the game rules and instructions."""
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

def main():
    """Main game loop."""
    display_rules()

    player_score, computer_score = 0, 0

    while player_score < 10000 and computer_score < 10000:
        player_score += player_turn()
        print(f"Your turn ended with {player_score} points.")
        
        computer_score += computer_turn()
        print(f"Computer's turn ended with {computer_score} points.")

    winner = "Player" if player_score >= 10000 else "Computer"
    print(f"{winner} wins!")

if __name__ == "__main__":
    main()

