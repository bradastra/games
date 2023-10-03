import random
import time

RULES = """
Farkle Rules:

Each turn starts with six rolled dice. The player must then select which dice to keep for points from that roll. Once that is done, the player may either Pass play to the next player or Roll the remaining dice to gain more points for that turn.

Each player must score at least 500 points during a single turn to get into the game. Once this has been achieved, any points accumulated during subsequent turns are added to the player's total score.

Winning:
Play continues until one player scores over 10,000 points. The other player gets one more turn to try and beat that score. The player with the highest score at the end of that turn wins the game.
"""

def roll_dice(num_dice):
    return [random.randint(1, 6) for _ in range(num_dice)]

def calculate_score(dice):
    counts = {i: dice.count(i) for i in range(1,7)}
    
    score = 0
    if len(dice) == 6:
        if all(val == 1 for val in counts.values()):
            return 1500
        if len({k for k, v in counts.items() if v == 3}) == 2:
            return 2500
        if len({k for k, v in counts.items() if v == 2}) == 3:
            return 1500

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

def ask_to_keep(rolled_dice):
    while True:
        print("Dice: " + " ".join(map(str, rolled_dice)))
        kept_input = input("Enter dice to keep (or nothing to roll again), separated by spaces: ").split()
        
        try:
            kept_dice = [int(d) for d in kept_input]
            
            if not all(1 <= d <= 6 for d in kept_dice):
                raise ValueError("Dice values should be between 1 and 6.")
            
            if not all(rolled_dice.count(d) >= kept_dice.count(d) for d in kept_dice):
                raise ValueError("You can't keep dice values more times than they were rolled.")
            
            return kept_dice
        except ValueError as e:
            print(f"Invalid input: {e}. Please choose again from the dice rolled.")

def computer_strategy(rolled_dice, score_diff):
    kept = []
    potential_score = calculate_score(rolled_dice)
    
    if potential_score == 0:
        return kept
    
    if score_diff > 1000 and potential_score < 500:
        return kept
    
    if score_diff < -1000 and potential_score > 250:
        return rolled_dice
    
    if potential_score > 300:
        return rolled_dice
    return kept

def score_roll(rolled_dice, is_human, opponent_score):
    if is_human:
        kept_dice = ask_to_keep(rolled_dice)
    else:
        score_diff = opponent_score - (player_score if is_human else computer_score)  # Estimate the score difference
        kept_dice = computer_strategy(rolled_dice, score_diff)

    # If the dice kept equals the dice rolled, player gets to use all six dice on their next roll.
    if len(kept_dice) == len(rolled_dice):
        print("\nYou've scored with all dice! You get a Free Roll with all six dice!")
        available_dice = 6
    else:
        available_dice = 6 - len(kept_dice)

    score = calculate_score(kept_dice)
    return score, kept_dice, available_dice

def turn(is_human, player_score, opponent_score):
    total_score = 0
    available_dice = 6
    
while True:
    rolled_dice = roll_dice(available_dice)
    print("\n" + ('Your' if is_human else "Computer's") + " Dice rolled: " + ' '.join(map(str, rolled_dice)))
    
    score, kept_dice, available_dice = score_roll(rolled_dice, is_human, opponent_score)  # Opponent's score is passed here
    
    if score == 0:
        return 0
        
        total_score += score

        if is_human:
            # For human player
            print(f"\nCurrent Turn Score: {total_score}")
            while True:
                decision = input("Press Enter to roll again or type 'stay' to keep your points: ").strip().lower()
                if decision in ["", "stay"]:
                    break
                print("Invalid input. Please press Enter or type 'stay'.")
            
            if decision == "stay":
                return total_score
        else:
            # For computer player
            print(f"Computer keeps: {' '.join(map(str, kept_dice))}")
            # Decision-making for the computer
            if total_score >= 500 and (total_score > score_diff or available_dice == 0 or random.random() > 0.5):
                print(f"Computer ends turn with {total_score} points.")
                return total_score
            time.sleep(2)

def main():
    print("\nWelcome to Farkle!")
    print(RULES)
    player_score = 0
    computer_score = 0
    player_on_board = False
    computer_on_board = False

    while player_score < 10000 and computer_score < 10000:
        print("\n============================")
        print(f"Current Scores:\nPlayer: {player_score}\nComputer: {computer_score}")
        print("============================\n")
        
        print("Your turn! Press Enter to roll the dice...")
        input()
        turn_score = turn(True, player_score, computer_score)
        
        if player_on_board or turn_score >= 500:
            player_on_board = True
            player_score += turn_score
        
        if player_score < 10000:
            print("\nComputer's turn... Press Enter for the computer to roll the dice.")
            input()
            turn_score = turn(False, player_score, computer_score)
            
            if computer_on_board or turn_score >= 500:
                computer_on_board = True
                computer_score += turn_score
        else:
            break
    
    # Final scoring announcement
    if player_score > computer_score:
        print(f"\nCongratulations! You win with a score of {player_score} to {computer_score}!")
    elif computer_score > player_score:
        print(f"\nComputer wins with a score of {computer_score} to {player_score}. Better luck next time!")
    else:
        print(f"\nIt's a tie! Both you and the computer have a score of {player_score}.")

if __name__ == "__main__":
    main()
