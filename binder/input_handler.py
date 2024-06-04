def get_input():
    print("Enter 1 to show the entire process or 2 to show only the middle part of the final image:")
    while True:
        try:
            user_input = int(input())
            if user_input in [1, 2]:
                return user_input
            else:
                print("Invalid input. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number (1 or 2).")
