import random
import time

# Define scoring rules
SCORING_RULES = {
    (1,): 100,
    (5,): 50,
    (1, 1, 1): 1000,
    (2, 2, 2): 200,
    (3, 3, 3): 300,
    (4, 4, 4): 400,
    (5, 5, 5): 500,
    (6, 6, 6): 600,
    (1, 2, 3, 4, 5, 6): 1500,
    # Four of a kind, five of a kind, six of a kind
    (1, 1, 1, 1): 2000,
    (1, 1, 1, 1, 1): 3000,
    (1, 1, 1, 1, 1, 1): 4000
}

def roll_dice(num=6):
    return tuple(random.choice(range(1, 7)) for _ in range(num))

def calculate_score(dice):
    score = 0
    dice = list(dice)
    for combo, combo_score in sorted(SCORING_RULES.items(), key=lambda x: (-len(x[0]), -x[1])):
        while all(dice.count(d) >= combo.count(d) for d in combo):
            score += combo_score
            for d in combo:
                dice.remove(d)
    return score

def computer_turn(total_score, opponent_score):
    remaining_dice = 6
    turn_score = 0
    while remaining_dice > 0:
        roll = roll_dice(remaining_dice)
        print(f"Computer rolled: {roll}")
        time.sleep(2)

        # Find all scoring dice
        scoring_dice = [d for d in roll if calculate_score((d,)) > 0]
        if not scoring_dice:
            return 0

        # Strategy decision
        score_diff = opponent_score - total_score
        risk_factor = 0.5 if score_diff < 500 else 0.7
        should_continue = len(scoring_dice) > 3 or random.random() < risk_factor

        if not should_continue:
            return turn_score

        turn_score += calculate_score(scoring_dice)
        print(f"Computer kept: {scoring_dice} - Current turn score: {turn_score}")
        time.sleep(1)

        # Update remaining dice
        for d in scoring_dice:
            roll = list(roll)
            roll.remove(d)
            remaining_dice -= 1

        # Reset dice if all are used
        if remaining_dice == 0:
            remaining_dice = 6

    return turn_score

def player_turn():
    remaining_dice = 6
    turn_score = 0
    while remaining_dice > 0:
        roll = roll_dice(remaining_dice)
        print(f"Current roll: {roll}")

        choices = input("Which dice do you want to keep? (enter space-separated numbers or 'done'): ").split()
        if "done" in choices:
            return turn_score

        # Input validation
        chosen_dice = tuple(map(int, choices))
        if not all(chosen_dice.count(d) <= roll.count(d) for d in chosen_dice):
            print("Invalid dice selection. Try again.")
            continue

        score_for_this_roll = calculate_score(chosen_dice)
        if score_for_this_roll == 0:
            print("Non-scoring dice selected. Try again.")
            continue

        turn_score += score_for_this_roll
        print(f"You kept: {chosen_dice} - Current turn score: {turn_score}")

        # Update remaining dice
        for d in chosen_dice:
            roll = list(roll)
            roll.remove(d)
            remaining_dice -= 1

        # Reset dice if all are used
        if remaining_dice == 0:
            remaining_dice = 6

        choice = input("Would you like to roll again or stay? (roll/stay): ").strip().lower()
        if choice == "stay":
            break

    return turn_score

def display_rules():
    print("The scoring rules are:")
    for combo, score in SCORING_RULES.items():
        print(f"{combo}: {score} points")
    print("\nThe first player to reach 10,000 points wins!\n")

def main():
    player_score, computer_score = 0, 0
    print("Welcome to Farkle!")
    play_choice = input("Would you like to play? (yes/no): ")
    if play_choice.lower() != "yes":
        return

    display_rules()

    player_had_final_turn = False
    computer_had_final_turn = False

    while True:
        print("\nYour turn!")
        player_score += player_turn()
        print(f"Your total score: {player_score}")
        if player_score >= 10000 and not player_had_final_turn:
            player_had_final_turn = True
            if computer_had_final_turn:
                break

        print("\nComputer's turn!")
        computer_score += computer_turn(computer_score, player_score)
        print(f"Computer's total score: {computer_score}")
        if computer_score >= 10000 and not computer_had_final_turn:
            computer_had_final_turn = True
            if player_had_final_turn:
                break

    print("Game over!")
    if player_score > computer_score:
        print("Congratulations! You win!")
    else:
        print("Computer wins!")

if __name__ == "__main__":
    main()

