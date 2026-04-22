import json
import datetime
import os

session = {"username": None}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

ACTIVITIES = [
    {"activity": "running",         "met": {"low": 7.0,  "medium": 8.3,  "high": 11.0}},
    {"activity": "cycling",         "met": {"low": 4.5,  "medium": 6.8,  "high": 10.0}},
    {"activity": "swimming",        "met": {"low": 6.0,  "medium": 7.0,  "high": 9.5}},
    {"activity": "walking",         "met": {"low": 2.8,  "medium": 3.5,  "high": 4.3}},
    {"activity": "weight training", "met": {"low": 3.5,  "medium": 5.0,  "high": 6.0}},
    {"activity": "yoga",            "met": {"low": 2.0,  "medium": 2.5,  "high": 3.0}},
    {"activity": "aerobics",        "met": {"low": 6.5,  "medium": 7.3,  "high": 8.5}},
    {"activity": "dancing",         "met": {"low": 3.5,  "medium": 5.0,  "high": 7.5}},
    {"activity": "rowing machine",  "met": {"low": 5.5,  "medium": 7.0,  "high": 8.5}},
    {"activity": "hiking",          "met": {"low": 5.0,  "medium": 6.0,  "high": 7.0}},
    {"activity": "intercourse",     "met": {"low": 3.0,  "medium": 5.0,  "high": 5.8}},
]

def choose_activity():
    clear()
    print("\n=== Choose Activity ===")
    for i, a in enumerate(ACTIVITIES, 1):
        print(f"{i}. {a['activity'].capitalize()}")
    while True:
        choice = input("Enter number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(ACTIVITIES):
            return ACTIVITIES[int(choice) - 1]["activity"]
        print(f"Please enter a number between 1 and {len(ACTIVITIES)}.")

def choose_intensity():
    clear()
    print("\n=== Choose Intensity ===")
    print("1. Low")
    print("2. Medium")
    print("3. High")
    while True:
        choice = input("Enter number: ").strip()
        if choice == "1":
            return "low"
        elif choice == "2":
            return "medium"
        elif choice == "3":
            return "high"
        print("Please enter 1, 2 or 3.")

def calorie_calculation(activity, time_in_min, intensity):

    def find_met(activity):
        activity = activity.lower()
        for a in ACTIVITIES:
            if activity == a["activity"].lower():
                return a["met"]
        return None

    def calculate_calories(activity, time_in_min, intensity):
        user = session["username"]
        filename = f"{user}.json"
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        gender = data["gender"]
        weight = data["weight"]
        age    = data["age"]
        height = data["height"]

        met = find_met(activity)
        if met is None:
            return 0

        if gender.lower() == "male":
            bmr = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
        elif gender.lower() == "female":
            bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
        else:
            raise ValueError("Gender must be 'male' or 'female'.")

        calories = (bmr / 1440) * met[intensity] * time_in_min
        return round(calories, 2)

    return calculate_calories(activity, time_in_min, intensity)

def add_workout():
    clear()
    user = session["username"]
    filename = f"{user}.json"

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        activity    = choose_activity()
        intensity   = choose_intensity()
        clear()
        time_in_min = float(input("Time in minutes: "))
        date        = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        calories    = calorie_calculation(activity, time_in_min, intensity)

        new_session = {
            "date":        date,
            "activity":    activity,
            "intensity":   intensity,
            "time_in_min": time_in_min,
            "calories":    calories
        }

        if "workouts" not in data:
            data["workouts"] = []
        data["workouts"].append(new_session)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        clear()
        print(f"\nWorkout saved! Estimated calories burned: {calories} kcal")

    except Exception as e:
        print("Something went wrong:", e)

def view_workouts():
    clear()
    user = session["username"]
    filename = f"{user}.json"

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        workouts = data.get("workouts", [])

        if not workouts:
            print("\nNo workouts logged yet.")
            return

        total_calories = sum(w["calories"] for w in workouts)
        total_minutes  = sum(w["time_in_min"] for w in workouts)

        print(f"\n=== Workout History for '{user}' ===")
        print(f"{'#':<4} {'Date':<18} {'Activity':<18} {'Intensity':<12} {'Minutes':<10} {'Calories':<10}")
        print("-" * 74)
        for i, w in enumerate(workouts, 1):
            print(f"{i:<4} {w['date']:<18} {w['activity'].capitalize():<18} {w.get('intensity', '-').capitalize():<12} {w['time_in_min']:<10} {w['calories']:<10} kcal")
        print("-" * 74)
        print(f"{'Total':<4} {'':<18} {'':<18} {'':<12} {total_minutes:<10} {total_calories:<10} kcal")

    except Exception as e:
        print("Something went wrong:", e)

def create_account():
    clear()
    print("Create new account")
    username = input("Choose a username: ").lower().strip()
    gender   = input("Enter biological gender (male or female): ").lower().strip()
    age      = int(input("Enter age: "))
    height   = float(input("Enter height in (cm): "))
    weight   = float(input("Enter weight in (kg): "))

    user = {
        "username": username,
        "gender":   gender,
        "age":      age,
        "height":   height,
        "weight":   weight
    }

    filename = f"{username}.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(user, file, ensure_ascii=False, indent=4)

    clear()
    print(f"Your account '{username}' has been saved!")


def delete_account():
    clear()
    user = session["username"]
    filename = f"{user}.json"

    confirm = input(f"Are you sure you want to delete '{user}'? (yes/no): ").lower().strip()

    if confirm == "yes":
        try:
            os.remove(filename)
            session["username"] = None
            clear()
            print("Account deleted successfully.")
        except FileNotFoundError:
            clear()
            print("Account not found.")
        except Exception as e:
            print("Something went wrong:", e)
    else:
        clear()
        print("Deletion canceled")



def log_in():
    clear()
    username = input("Username: ").lower().strip()
    filename = f"{username}.json"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            json.load(file)
        session["username"] = username
        clear()
        print(f"Logged in as '{username}'!")
    except FileNotFoundError:
        clear()
        print("Account not found.")


while True:
    if session["username"] is None:
        print("\n=== Welcome ===")
        print("1. Log in")
        print("2. Create account")
        print("3. Quit")
        choice = input("Choose: ").strip()
        clear()

        if choice == "1":
            log_in()
        elif choice == "2":
            create_account()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

    else:
        print(f"\n=== Logged in as '{session['username']}' ===")
        print("1. Add workout")
        print("2. View all workouts")
        print("3. Log out")
        print("4. Quit")
        print("5. Delete account")
        choice = input("Choose: ").strip()
        clear()

        if choice == "1":
            add_workout()
        elif choice == "2":
            view_workouts()
        elif choice == "3":
            session["username"] = None
            print("Logged out.")
        elif choice == "4":
            print("Goodbye!")
            break
        elif choice == "5":
            delete_account()
        else:
            print("Invalid choice, please try again.")