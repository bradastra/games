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

def score(roll):
    """Calculate score based on roll."""
    total_score = 0
    counts = {i: roll.count(i) for i in set(roll)}

    for combo, value in SCORING.items():
        if all(counts.get(i, 0) >= combo.count(i) for i in combo):
            total_score += value
            for i in combo:
                counts[i] -= combo.count(i)
    
    for combo, value in SCORING.items():
        if len(combo) == 1 and counts.get(combo[0], 0):
            total_score += counts[combo[0]] * value

    return total_score

def roll_dice(n):
    """Roll n dice and return results."""
    return tuple(random.randint(1, 6) for _ in range(n))

def choose_dice_to_keep(roll):
    """Let player choose dice to keep."""
    print(f"You rolled: {roll}")
    kept_dice = []
    while True:
        choice = input("Which dice do you want to keep? (enter the number or 'done'): ")
        if choice == "done":
            break
        if choice.isdigit() and int(choice) in roll:
            kept_dice.append(int(choice))
            roll = tuple(x for x in roll if x != int(choice))
        else:
            print("Invalid choice. Try again.")
    return tuple(kept_dice)

def player_turn():
    """Player's turn."""
    remaining_dice = 6
    turn_score = 0
    kept_dice = []

    while remaining_dice > 0:
        roll = roll_dice(remaining_dice)
        roll_score = score(roll)
        if roll_score == 0:
            print(f"You rolled: {roll} - Farkle!")
            return 0
        
        kept = choose_dice_to_keep(roll)
        if not kept:
            print("No dice kept. Farkle!")
            return 0
        
        kept_score = score(kept)
        turn_score += kept_score
        print(f"You kept: {kept} for a score of {kept_score}")

        action = input("Keep total score (k) or roll again (r)? ").lower()
        if action == "k":
            return turn_score
        
        kept_dice.extend(kept)
        remaining_dice -= len(kept)
        
        if remaining_dice == 0:
            remaining_dice = 6

def computer_turn():
    """Computer's turn."""
    remaining_dice = 6
    turn_score = 0

    while remaining_dice > 0:
        roll = roll_dice(remaining_dice)
        roll_score = score(roll)

        print(f"Computer rolled: {roll} - Score: {roll_score}")

        if roll_score == 0:
            print("Computer Farkle!")
            return 0
        
        if turn_score + roll_score > 300:
            return turn_score + roll_score
        else:
            turn_score += roll_score
            remaining_dice = 6

def main():
    """Main game loop."""
    player_score = 0
    computer_score = 0

    # Display the scoring rules
    print("--- SCORING ---")
    for combo, value in SCORING.items():
        print(f"{combo}: {value} points")
    print("--------------\n")

    while player_score < 10000 and computer_score < 10000:
        player_score += player_turn()
        computer_score += computer_turn()

        print(f"Current Scores - Player: {player_score}, Computer: {computer_score}")

    if player_score >= 10000:
        print("You win!")
    else:
        print("Computer wins!")

if __name__ == "__main__":
    main()

