import random
import time

print("Welcome to The Final Guess.")

best_score = 0
streak = 0

while True:
    print("\nSelect mode:")
    print("1. Classic(Hints, AI Suggestion, No timer)")
    print("2. Hard(No hints, No AI, No timer)")
    print("3. Timer Mode(10 sec per guess)")

    try:
        mode = int(input("Enter your choice of mode(1/2/3): "))
    except ValueError:
        print("Invalid input! Defaulting to classic.")
        mode = 1

    if mode not in [1, 2, 3]:
        print("Invalid input! Defaulting to Classic.")
        mode = 1

    print("\nSelect Difficulty:")
    print("1. Easy(1-10, 5 attempts)")
    print("2. Medium(1-20, 10 attempts")
    print("3. Hard(1-50, 15 attempts)")
    print("4. Boss Level(1-100, 10 attempts)")

    try:
        choice = int(input("Enter your choice(1/2/3/4): "))
    except ValueError:
        print("Invalid input! Defaulting to Easy.")
        choice = 1

    if choice == 1:
        low, high, max_attempts = 1, 10, 5
    elif choice == 2:
        low, high, max_attempts = 1, 20, 10
    elif choice == 3:
        low, high, max_attempts = 1, 50, 15
    elif choice == 4:
        low, high, max_attempts = 1, 100, 10
    else:
        print("Invalid choice! Defaulting to easy.")
        low, high, max_attempts = 1, 10, 5

    num = random.randint(low, high)
    attempts = 0

    ai_low, ai_high = low, high

    print(f"Choose a number between {low} and {high}.")
    print(f"You have total {max_attempts} attempts.")

    while attempts < max_attempts:
        start_time = time.time()

        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Invalid input! Enter a proper positive number. ")
            continue

        if mode == 3 and (time.time() - start_time > 10):
            print("Too slow! Attempt wasted.")
            attempts += 1
            continue

        attempts += 1

        if guess == num:
            print("\nCorrect!")

            if attempts == 1:
                print("INSANE! Congrats!")

            print(f"You guessed it in {attempts} attempts.")

            score = max_attempts - attempts + 1
            print(f"Your score: {score}")

            if score > best_score:
                best_score = score
                print("New Best Score!")

            streak += 1
            print(f"Current streak: {streak}")
            break
        elif guess < num:
            print("Too Low!")
            ai_high = max(ai_low, guess + 1)
        else:
            print("Too High!")
            ai_low = min(ai_high, guess - 1)

        if mode != 2:
            difference = abs(num - guess)

            if difference <= 2:
                print("Too close!")
            elif difference <= 5:
                print("Close!")
            elif difference <= 10:
                print("Wrong!")
            else:
                print("Too far!")

            mid = (ai_low + ai_high)//2
            print(f"AI Suggestion: Try {mid}.")

        print(f"Range: {ai_low} to {ai_high}")
        print(f"Attempts left: {max_attempts - attempts}")

    else:
        print(f"Game Over! The number was {num}.")
        streak = 0
        print("Streak reset.")

    print(f"\nBest Score: {best_score}")

    again = input("Play again?(yes/no): ").lower()

    if again != "yes":
        print("Game Over! Goodbye player!")
        break