import random
import time

RULES = """
Welcome to Farkle!
Rules & Scoring:
1: 100 points
5: 50 points
Three 1's: 1000 points
Three 2's: 200 points
Three 3's: 300 points
Three 4's: 400 points
Three 5's: 500 points
Three 6's: 600 points
Four or more of any number: Double the three of a kind score for each extra number.
Press 'r' anytime during the game to see these rules again.
"""

def roll_dice(num_dice):
    return [random.randint(1, 6) for _ in range(num_dice)]

def calculate_score(roll):
    score = 0
    counts = {i: roll.count(i) for i in range(1,7)}

    # Check for 1's and 5's first
    score += counts[1] * 100
    score += counts[5] * 50

    # Check for three or more of a kind for all numbers
    for number, count in counts.items():
        if count >= 3:
            if number == 1:
                score += 1000
            else:
                score += number * 100
            # For more than 3 of a kind, double the score for each extra number
            score += (count - 3) * score

    # Subtract the appropriate amount for 1's and 5's since they were added previously
    if counts[1] >= 3:
        score -= 300
    if counts[5] >= 3:
        score -= 150

    return score

def player_turn():
    remaining_dice = 6
    total_turn_score = 0

    while remaining_dice > 0:
        roll = roll_dice(remaining_dice)
        print("\nYou rolled:", roll)
        while True:
            try:
                dice_to_keep = input("Enter dice to keep (e.g. 456): ")
                if dice_to_keep == 'r':
                    print(RULES)
                    continue
                kept_dice = [int(i) for i in dice_to_keep]
                if all(x in roll for x in kept_dice):
                    break
            except ValueError:
                print("Invalid input. Please enter numbers from the roll.")

        turn_score = calculate_score(kept_dice)
        total_turn_score += turn_score
        print(f"Score this roll: {turn_score}\n")
        action = input("\nDo you want to (P)ass or (R)oll again? ").upper()
        if action == 'P':
            return total_turn_score

        remaining_dice -= len(kept_dice)
        if remaining_dice == 0:
            remaining_dice = 6

def enhanced_computer_turn(player_score, computer_score):
    total_turn_score = 0
    remaining_dice = 6
    while True:
        rolled_dice = roll_dice(remaining_dice)
        print(f"\nComputer rolled: {rolled_dice}")
        time.sleep(2)

        potential_score = calculate_score(rolled_dice)
        if potential_score == 0:
            print("Computer got a Farkle!")
            return 0

        if potential_score < 300 or computer_score + total_turn_score < player_score:
            print(f"Computer decides to roll again despite getting {potential_score} in this roll.")
            continue
        else:
            total_turn_score += potential_score
            print(f"Computer adds {potential_score} to its total score.")
            return total_turn_score

def display_rules():
    print(RULES)

def main():
    display_rules()
    player_score = 0
    computer_score = 0

    while True:
        print(f"\nYour score: {player_score} | Computer's score: {computer_score}")
        input("\nYour turn! Press Enter to roll the dice...")
        player_score += player_turn()
        if player_score >= 10000:
            print("\nYou reached 10,000 points!")
            input("Press Enter for the computer's last turn...")
            computer_score += enhanced_computer_turn(player_score, computer_score)
            break
        computer_score += enhanced_computer_turn(player_score, computer_score)
        if computer_score >= 10000:
            print("\nThe computer reached 10,000 points!")
            input("Press Enter for your last turn...")
            player_score += player_turn()
            break

    print(f"\nFinal score: You: {player_score} | Computer: {computer_score}")
    if player_score > computer_score:
        print("Congratulations! You won!")
    elif player_score < computer_score:
        print("The computer won! Better luck next time.")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()
