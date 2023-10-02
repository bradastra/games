import random
import time

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

# ... [Rest of the functions remain unchanged]

def welcome_screen():
    print("Welcome to Farkle!")
    choice = input("Would you like to play? (yes/no): ").strip().lower()
    
    if choice == "yes" or choice == "y":
        return True
    elif choice == "no" or choice == "n":
        print("Thanks for checking out Farkle! Goodbye.")
        return False
    else:
        print("Invalid choice. Please enter 'yes' or 'no'.")
        return welcome_screen()  # Recursive call to handle invalid input

def main():
    if welcome_screen():
        display_rules()
        play_game()

if __name__ == "__main__":
    main()

