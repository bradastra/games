import random

# Farkle Scoring Rules
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
    """Roll a specified number of dice (default is 6)."""
    return [random.randint(1, 6) for _ in range(num)]

def score(roll):
    """Calculate the score for a given roll."""
    roll = tuple(sorted(roll))
    return SCORING_RULES.get(roll, 0)

def is_farkle(roll):
    """Determine if the roll is a Farkle (no points)."""
    return all(score((die,)) == 0 for die in roll) and score(roll) == 0

def select_dice(roll):
    """Let the player select which dice to keep."""
    selected = []
    while True:
        print(f"Current roll: {tuple(roll)}")
        choice = input("Which dice do you want to keep? (enter space-separated numbers or 'done'): ").strip().lower()
        if choice == 'done':
            break
        try:
            # Convert the input into a tuple of integers
            dice_to_keep = tuple(map(int, choice.split()))
            
            # Validate the chosen dice
            if all(die in roll for die in dice_to_keep):
                potential_score = score(dice_to_keep)
                if potential_score > 0:
                    for die in dice_to_keep:
                        roll.remove(die)
                    selected.extend(dice_to_keep)
                else:
                    print("The selected dice don't give any score. Try again.")
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid choice. Try again.")
    return selected

def player_turn():
    """Handle the player's turn."""
    total_score = 0
    roll = roll_dice()
    
    while True:
        if is_farkle(roll):
            print(f"You rolled: {tuple(roll)} - Farkle!")
            return 0
        
        kept = select_dice(roll)
        roll_score = score(kept)
        total_score += roll_score
        print(f"You kept: {tuple(kept)} for a score of {roll_score}")
        
        if len(roll) == 0:
            roll = roll_dice()
            print("You've used all the dice! Rolling all dice again.")
        
        action = input(f"Keep total score (k) or roll again (r)? ").strip().lower()
        if action == 'k':
            return total_score
        elif action == 'r':
            roll = roll_dice(len(roll))

def computer_turn():
    """Handle the computer's turn."""
    total_score = 0
    roll = roll_dice()
    
    while total_score < 300:
        if is_farkle(roll):
            print(f"Computer rolled: {tuple(roll)} - Farkle!")
            return 0
        
        # Simple strategy for computer: keep all scoring dice
        kept = [die for die in roll if score((die,)) > 0] or roll
        roll_score = score(kept)
        total_score += roll_score
        print(f"Computer rolled: {tuple(roll)} - Score: {roll_score}")
        
        for die in kept:
            roll.remove(die)
        
        if len(roll) == 0:
            roll = roll_dice()
    
    return total_score

def main():
    """Main game loop."""
    player_score = 0
    computer_score = 0
    
    # Print scoring rules
    print("\n--- SCORING ---")
    for roll, roll_score in SCORING_RULES.items():
        print(f"{roll}: {roll_score} points")
    print("--------------\n")
    
    while True:
        player_score += player_turn()
        computer_score += computer_turn()
        
        print(f"Current Scores - Player: {player_score}, Computer: {computer_score}")
        
        if player_score >= 10000 or computer_score >= 10000:
            break
    
    # Determine winner
    if player_score >= 10000:
        print("Congratulations! You won!")
    else:
        print("Computer wins! Better luck next time.")

if __name__ == "__main__":
    main()

