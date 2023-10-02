import random
import time

# Version: 2.1

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
    (1, 2, 3, 4, 5, 6): 1500,  # Straight
    (1, 1, 2, 2, 3, 3): 1500,  # Three pairs variations
    (1, 1, 4, 4, 5, 5): 1500,
    (1, 1, 3, 3, 6, 6): 1500,
    (2, 2, 4, 4, 6, 6): 1500,
    (2, 2, 3, 3, 5, 5): 1500,
    (1, 1, 1, 2, 2, 2): 2500,  # Two triplets variations
    (1, 1, 1, 3, 3, 3): 2500,
    (1, 1, 1, 4, 4, 4): 2500,
    (1, 1, 1, 5, 5, 5): 2500,
    (1, 1, 1, 6, 6, 6): 2500,
    (2, 2, 2, 3, 3, 3): 2500,
    (2, 2, 2, 4, 4, 4): 2500,
    (2, 2, 2, 5, 5, 5): 2500,
    (2, 2, 2, 6, 6, 6): 2500,
    (3, 3, 3, 4, 4, 4): 2500,
    (3, 3, 3, 5, 5, 5): 2500,
    (3, 3, 3, 6, 6, 6): 2500,
    (4, 4, 4, 5, 5, 5): 2500,
    (4, 4, 4, 6, 6, 6): 2500,
    (5, 5, 5, 6, 6, 6): 2500,
}

# Four, Five, and Six of a kind multiplier rules
MULTIPLIER_RULES = {
    4: 2,
    5: 3,
    6: 4,
}

def roll_dice(num=6):
    return tuple(random.choice(range(1, 7)) for _ in range(num))

def calculate_score(dice):
    score = 0
    dice_count = {i: dice.count(i) for i in range(1, 7)}

    for combo, combo_score in SCORING_RULES.items():
        if all(dice.count(d) >= combo.count(d) for d in combo):
            score += combo_score

    # Checking for 4, 5, and 6 of a kind
    for num, count in dice_count.items():
        if count > 3:
            base_score = SCORING_RULES.get((num, num, num), 0)
            score += base_score * MULTIPLIER_RULES[count]

    return score

def is_farkle(dice):
    return calculate_score(dice) == 0

def player_turn():
    total_turn_score = 0
    num_dice = 6
    input("\nYour turn! Press Enter to roll the dice...")
    while True:
        rolled_dice = roll_dice(num_dice)
        print(f"\nYou rolled: {rolled_dice}")
        score_this_roll = calculate_score(rolled_dice)
        if is_farkle(rolled_dice):
            print("Farkle! No points this turn.")
            return 0
        print(f"Score this roll: {score_this_roll}")
        action = input("\nDo you want to (P)ass or (R)oll again? ").upper()
        if action == 'P':
            return total_turn_score + score_this_roll
        elif action == 'R':
            total_turn_score += score_this_roll
            num_dice -= len(rolled_dice)
            if num_dice == 0:
                num_dice = 6

def computer_turn():
    total_turn_score = 0
    num_dice = 6
    print("\nComputer's turn!")
    while total_turn_score < 300:  # Computer strategy to stop at a threshold score
        time.sleep(2)  # Pause for suspense
        rolled_dice = roll_dice(num_dice)
        print(f"\nComputer rolled: {rolled_dice}")
        score_this_roll = calculate_score(rolled_dice)
        if is_farkle(rolled_dice):
            print("Farkle! No points this turn for the computer.")
            return 0
        total_turn_score += score_this_roll
        num_dice -= len(rolled_dice)
        if num_dice == 0:
            num_dice = 6
    print(f"\nComputer secures {total_turn_score} points this turn.")
    return total_turn_score

def main():
    player_score, computer_score = 0, 0
    print("\nWelcome to Farkle!")
    while True:
        action = input("\nDo you want to (P)lay or (E)xit? ").upper()
        if action == 'E':
            print("\nThanks for playing!")
            break
        elif action == 'P':
            while player_score < 10000 and computer_score < 10000:
                player_score += player_turn()
                print(f"\nYour total score: {player_score}")
                computer_score += computer_turn()
                print(f"Computer's total score: {computer_score}")
            if player_score > computer_score:
                print("\nCongratulations! You win!")
            else:
                print("\nComputer wins! Better luck next time!")
            player_score, computer_score = 0, 0  # Reset scores for a new game
        else:
            print("\nInvalid choice. Please choose (P)lay or (E)xit.")

if __name__ == "__main__":
    main()

