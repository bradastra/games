import random

def roll_dice(num=6):
    return tuple(random.randint(1, 6) for _ in range(num))

def calculate_score(dice):
    # Scoring rules
    score = 0
    counts = {i: dice.count(i) for i in set(dice)}

    for num, count in counts.items():
        if count >= 3:
            if num == 1:
                score += 1000
            else:
                score += num * 100
            count -= 3

        if num == 1:
            score += count * 100
        elif num == 5:
            score += count * 50

    return score

def player_turn():
    current_roll = roll_dice()
    total_score = 0

    while True:
        print(f"Current roll: {current_roll}")

        selected_values = input("Which dice do you want to keep? (enter space-separated numbers or 'done'): ").split()

        if 'done' in selected_values:
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
        current_roll = roll_dice(len(current_roll) - len(selected_values))
        if not current_roll:
            return total_score

def computer_turn():
    current_roll = roll_dice()
    total_score = 0

    while current_roll:
        score = calculate_score(current_roll)
        if score == 0:
            return 0
        total_score += score
        current_roll = roll_dice(len(current_roll) - len(current_roll))

    return total_score

def main():
    player_score = 0
    computer_score = 0
    while True:
        player_score += player_turn()
        print(f"Your turn ended with {player_score} points.")
        computer_score += computer_turn()
        print(f"Computer's turn ended with {computer_score} points.")
        print(f"Scores - Player: {player_score}, Computer: {computer_score}")

if __name__ == "__main__":
    main()

