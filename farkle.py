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
        kept_dice = input("Enter dice to keep (or nothing to roll again), separated by spaces: ").split()
        if not kept_dice:
            return []
        kept_dice = [int(d) for d in kept_dice]
        
        if all(d in rolled_dice for d in kept_dice):
            return kept_dice
        else:
            print("Invalid dice chosen. Please choose again from the dice rolled.")

def computer_strategy(rolled_dice, score_diff):
    # Basic strategy:
    # - Always keep scoring dice.
    # - If score of current turn is less than 300 and more dice can be rolled, continue rolling.
    # - If ahead by a significant margin (say, 1000 points), play conservatively.
    # - If trailing by a significant margin, play more aggressively.
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

def turn(is_player, player_score, computer_score):
    rolled_dice = roll_dice(6)
    turn_score = 0
    score_diff = player_score - computer_score
    while True:
        print("\nDice rolled: " + " ".join(map(str, rolled_dice)))
        if calculate_score(rolled_dice) == 0:
            print("Farkle!")
            return 0
        if is_player:
            kept_dice = ask_to_keep(rolled_dice)
        else:
            time.sleep(2)
            kept_dice = computer_strategy(rolled_dice, score_diff)
            print("Computer keeps: " + " ".join(map(str, kept_dice)))
        
        if not kept_dice:
            rolled_dice = roll_dice(len(rolled_dice))
            continue
        
        turn_score += calculate_score(kept_dice)
        remaining_dice = len(rolled_dice) - len(kept_dice)
        
        if remaining_dice == 0:
            rolled_dice = roll_dice(6)
        else:
            for d in kept_dice:
                rolled_dice.remove(d)
            rolled_dice.extend(roll_dice(remaining_dice))
        
        if is_player:
            print(f"\nCurrent Turn Score: {turn_score}")
            choice = input("Press Enter to roll again or type 'stay' to keep your points: ").strip().lower()
            if choice == 'stay':
                return turn_score

def main():
    print("\nWelcome to Farkle!")
    print(RULES)
    player_score = 0
    computer_score = 0
    while player_score < 10000 and computer_score < 10000:
        print("\n============================")
        print(f"Current Scores:\nPlayer: {player_score}\nComputer: {computer_score}")
        print("============================\n")
        
        print("Your turn! Press Enter to roll the dice...")
        input()
        player_score += turn(True, player_score, computer_score)
        
        if player_score < 10000:
            print("\nComputer's turn... Press Enter for the computer to roll the dice.")
            input()
            computer_score += turn(False, player_score, computer_score)
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
