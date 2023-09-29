import random

# Scoring rules
SCORING = {
    (1,): 100,
    (5,): 50,
    (1, 1, 1): 1000,
    (2, 2, 2): 200,
    (3, 3, 3): 300,
    (4, 4, 4): 400,
    (5, 5, 5): 500,
    (6, 6, 6): 600,
    tuple(range(1, 7)): 1500  # straight
}

def show_scoring():
    print("\n--- SCORING ---")
    for combo, value in SCORING.items():
        print(f"{combo}: {value} points")
    print("--------------\n")

def score(roll):
    """Calculate score based on roll."""
    total_score = 0
    counts = {i: roll.count(i) for i in set(roll)}

    # Check three of a kind and straight
    for combo, value in SCORING.items():
        if all(counts.get(i, 0) >= combo.count(i) for i in combo):
            total_score += value

            # remove scored dice
            for i in combo:
                counts[i] -= combo.count(i)

    # Singles
    for combo, value in SCORING.items():
        if len(combo) == 1 and counts.get(combo[0], 0):
            total_score += counts[combo[0]] * value

    return total_score

def roll_dice(n):
    """Roll n dice and return results."""
    return tuple(random.randint(1, 6) for _ in range(n))

def player_turn():
    remaining_dice = 6
    turn_score = 0
    show_scoring()

    while remaining_dice > 0:
        roll = roll_dice(remaining_dice)
        selected = select_dice(roll)
        current_roll_score = score(selected)

        print(f"Selected dice: {selected} - Score: {current_roll_score}")

        if current_roll_score == 0:
            print("Farkle!")
            return 0

        turn_score += current_roll_score
        remaining_dice -= len(selected)

        if remaining_dice == 0:  # All dice scored, so they get to roll all 6 again
            remaining_dice = 6

        action = input(f"Turn score: {turn_score}. Keep score (k) or roll again (r)? ").lower()
        if action == "k":
            return turn_score

def computer_turn():
    remaining_dice = 6
    turn_score = 0

    while remaining_dice > 0:
        roll = roll_dice(remaining_dice)
        selected = [die for die in roll if die == 1 or die == 5 or roll.count(die) >= 3]  # basic strategy
        current_roll_score = score(selected)

        print(f"Computer rolled: {roll}")
        print(f"Computer selected: {selected} - Score: {current_roll_score}")

        if current_roll_score == 0:
            print("Computer Farkle!")
            return 0

        turn_score += current_roll_score
        remaining_dice -= len(selected)

        if remaining_dice == 0:
            remaining_dice = 6

        if turn_score > 300:  # Computer's threshold to keep score
            return turn_score

def main():
    player_score = 0
    computer_score = 0

    while player_score < 10000 and computer_score < 10000:
        player_score += player_turn()
        computer_score += computer_turn()
        print(f"Current Scores - Player: {player_score}, Computer: {computer_score}")

    # If the player crosses 10,000, give the computer one last chance
    if player_score >= 10000:
        print("You reached 10,000!")
        final_turn = computer_turn()
        computer_score += final_turn

    # Similarly, if the computer crosses 10,000, give the player one last chance
    elif computer_score >= 10000:
        print("Computer reached 10,000!")
        final_turn = player_turn()
        player_score += final_turn

    # Check for the winner
    if player_score > computer_score:
        print(f"You win with {player_score} points!")
    else:
        print(f"Computer wins with {computer_score} points!")

if __name__ == "__main__":
    main()

