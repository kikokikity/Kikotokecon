import random, os, json
from datetime import datetime, date
default_data = {
    "users": {},
    "tasks": {
        "Stretching": {"points": 1, "example": "1 (qty of times stretching done).", "OptIn": " ∞", 
                       "rules": {0: -1}},
        "Wake Time": {"points": -2, "example": "10 for 10am (pm not recognized)", "OptIn": "6 or 7",
                      "rules": {1: -2, 2: -2, 3: -2, 4: -2, 5: -1, 6: 3, 7: 2, 8: 1, 9: 1, 10: -1, 11: -2, 12: -2, 13: 20000}},
        "Sleep Duration": {"points": 2, "example": "10 for 10 hrs", "OptIn": " 8 or 9",
                          "rules": {0: -6, 1: -6, 2: -5, 3: -4, 4: -3, 5: -2, 6: -1, 7: 1, 8: 2, 9: 2, 10: 1, 11: -2}},
        "Meditating": {"points": 3, "example": "1 for qty of times meditating, 0 for none.", "OptIn": " ∞ ",
                       "rules": {0: -1}},
        "Water": {"points": 1, "example": "1 for qty of bottles drank", "OptIn": " ∞",
                  "rules": {0: -10, 1: -6, 2: -5, 3: -4, 4: -3, 5: -2, 6: -1, 7: -1, 8: 2, 9: 3}},
        "Nutrition": {"points": 2, "example": "1 for goals met or 2 for not", "OptIn": "1 ",
                     "rules": {0: 0, 1: 2, 2: -2}},
        "Exercise": {"points": 4, "example": "1 for qty of times excercised during day. 0 for none", "OptIn" : " ∞",
                    "rules": {0: -2}},
        "Social Media": {"points": -1, "example": "30 for qty of time in minutes spent on social media.", "OptIn": "0",
                        "rules": {0: 4, 1: 2, 2: 1, 3: -2}},
        "Bed Time": {"points": 2, "example": "10 for 10pm, 1 for 1am times.",  "OptIn": "10 or 11",
                    "rules": {9: 2, 10: 3, 11: 2, 12: 1, 1: -1, 2: -2}}
    },
    "rewards": {
        "Movie (1 movie)": 4,
        "YouTube (30 min)": 2,
        "Music (2 hrs)": 5,
        "Gaming (30 min)": 3,
        "Podcasts (1 hr)": 4,
        "Comics (30 min)": 2,
        "Book (30 min)": 1,
        "TV (30min)": 3
    }
}
DATA_FILE = "token_system_data.json"
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            for username in data["users"]:
                if "daily_rewards" not in data["users"][username]:
                    data["users"][username]["daily_rewards"] = {
                        "date": "",
                        "available": [],
                        "redeemed": []
                    }
                if "task_history" not in data["users"][username]:
                    data["users"][username]["task_history"] = {}
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return default_data

def save_data(data):
    json.dump(data, open(DATA_FILE, "w"), indent=4)

def add_user(data, username):
    if username not in data["users"]:
        data["users"][username] = {
            "points": 0, 
            "streak": 0, 
            "redeemed_rewards": [],
            "daily_rewards": {
                "date": "",
                "available": [],
                "redeemed": []
            },
            "task_history": {}
        }
        print(f"User '{username}' added.")
        save_data(data)

def get_daily_double_tasks(day):
    return {"m":["Wake Time"],"tu":["Sleep Duration"],"w":["Stretching"],"th":["Water"],"f":["Nutrition"],
            "sa":["Exercise","Social Media"],"sun":["Meditating","Bed Time"]}.get(day)

def apply_task_points(data, task, qty):
    task_data = data["tasks"][task]
    if "rules" in task_data and qty in task_data["rules"]:
        return task_data["rules"][qty]
    return task_data["points"]
def calculate_level(points):
    return points // 10
def calculate_rank(level):
    return next((n for t,n in [(1000,"god"),(750,"Demigod"),(500,"King"),(250,"Prince"),(100,"Noble"),(50,"Soldier"),(10,"Servant")]if level>=t),"Slave")
def get_remaining_tasks(data, username):
    today = date.today().isoformat()
    user_data = data["users"][username]
    if today not in user_data.get("task_history", {}):
        return list(data["tasks"].keys())
    completed_tasks = set(user_data["task_history"][today].keys())
    all_tasks = set(data["tasks"].keys())
    return list(all_tasks - completed_tasks)
def log_tasks(data, username, day):
    if username not in data["users"]:
        print(f"User '{username}' does not exist.")
        return
    today = date.today().isoformat()
    user_data = data["users"][username]
    if today not in user_data["task_history"]:
        user_data["task_history"][today] = {}
    total_points = user_data["points"]
    daily_double_tasks = get_daily_double_tasks(day)
    task_quantities = {}
    task_summary = {}
    session_total = 0
    tasks_to_log = [task for task in data["tasks"] if task not in user_data["task_history"][today]]
    skipped_tasks = []
    while tasks_to_log or skipped_tasks:
        if skipped_tasks:
            print(f"")
        if not tasks_to_log:
            break
        task = tasks_to_log.pop(0)
        task_info = data["tasks"][task]
        print(f"\nTask: {task}")
        print(f"Example: {task_info['example']}")
        print(f"Optimal Input: {task_info['OptIn']}")
        qty_input = input(f"Enter qty for '{task}' (or press Enter to skip): ").strip()
        if qty_input == "":
            print(f"Skipped '{task}'")
            skipped_tasks.append(task)
            input("\nPress Enter to continue...")
            clear_terminal()
            continue
        try:
            qty = int(qty_input)
            task_quantities[task] = qty
            points = apply_task_points(data, task, qty)
            if task in daily_double_tasks:
                points *= 2
                print(f"Daily Double applied for '{task}'!")
            total_points += points
            session_total += points
            task_summary[task] = points
            user_data["task_history"][today][task] = qty
            print(f"Points for '{task}' ({qty}): {points}. Total Points so far: {session_total}")
            input("\nPress Enter to continue...")
            clear_terminal()
        except ValueError:
            print(f"Invalid input. Please enter a number for '{task}'.")
            tasks_to_log.insert(0, task)
    user_data["points"] = total_points
    remaining_tasks = get_remaining_tasks(data, username)
    if not remaining_tasks:
        user_data["streak"] += 1
        print("\nAll tasks completed for today! Streak increased to", user_data["streak"])
    else:
        print(f"\nStreak remains at {user_data['streak']}. Complete all tasks to increase your streak.")
    print("\nTask Summary:\n")
    for task, points in task_summary.items():
        print(f"{task}: {points} points")
    print(f"Total Points for this session: {session_total}")
    print(f"User's Total Points after this session: {total_points}\n")
    if skipped_tasks:
        print("\nNote: You have skipped these tasks:")
        for task in skipped_tasks:
            print(f"- {task}")
    input("\nPress Enter to continue...")
    clear_terminal()
    save_data(data)
def ensure_daily_rewards(data, username):
    today = date.today().isoformat()
    user_data = data["users"][username]
    if user_data["daily_rewards"]["date"] != today:
        available_rewards = list(data["rewards"].items())
        daily_rewards = random.sample(available_rewards, min(3, len(available_rewards)))
        user_data["daily_rewards"] = {
            "date": today,
            "available": daily_rewards,
            "redeemed": []
        }
        save_data(data)
        print(f"🎉New daily rewards generated for {username}! 🎉")
    return user_data["daily_rewards"]
def redeem_reward(data, username):
    if username not in data["users"]:
        print(f"User '{username}' not found.")
        return
    user_data = data["users"][username]
    daily_rewards = ensure_daily_rewards(data, username)
    print(f"\nStatus for '{username}': Points: {user_data['points']}, Streak: {user_data['streak']}")
    print("\nAvailable Rewards for Today:")
    if not daily_rewards["available"]:
        print("You have redeemed all available rewards for today!🎁")
        input("Press Enter to continue...")
        return
    for i, (reward, cost) in enumerate(daily_rewards["available"], start=1):
        print(f"{i}. {reward}: {cost} points")
    if daily_rewards["redeemed"]:
        print("\nAlready Redeemed Today:")
        for i, (reward, cost) in enumerate(daily_rewards["redeemed"], start=1):
            print(f"{i}. {reward}: {cost} points")
    while True:
        try:
            reward_choice = input("\nEnter the number of the reward you want to redeem (or press Enter to cancel): ").strip()
            if not reward_choice:
                print("Returning to the menu.")
                break
            choice_index = int(reward_choice) - 1
            if 0 <= choice_index < len(daily_rewards["available"]):
                reward, cost = daily_rewards["available"][choice_index]
                if user_data["points"] >= cost:
                    user_data["points"] -= cost
                    user_data["redeemed_rewards"].append(reward)
                    redeemed_item = daily_rewards["available"].pop(choice_index)
                    daily_rewards["redeemed"].append(redeemed_item)
                    print(f"'{username}' redeemed '{reward}' for {cost} points.")
                    save_data(data)
                    break
                else:
                    print(f"Not enough points for '{reward}'. You need {cost - user_data['points']} more points.")
            else:
                print("Invalid selection. Please choose a valid reward number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
def export_user_data(data, username):
    if username in data["users"]:
        user_data = data["users"][username]
        level = calculate_level(user_data["points"])
        rank = calculate_rank(level)
        print(f"Status for '{username}': Points: {user_data['points']}, Level: {level}, Rank: {rank}, Streak: {user_data['streak']}")
        generate_activity_report(username, user_data)
def generate_activity_report(username, user_data):
    level = calculate_level(user_data["points"])
    rank = calculate_rank(level)
    report = {
        "username": username,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "points": user_data["points"],
        "level": level,
        "rank": rank,
        "redeemed_rewards": user_data["redeemed_rewards"],
        "today_redeemed": user_data["daily_rewards"]["redeemed"],
        "task_history": user_data.get("task_history", {})
    }
    filename = f"Activity_Report_{datetime.now().strftime('%Y_%m_%d')}.json"
    with open(filename, "w") as file:
        json.dump(report, file, indent=4)
    print(f"Activity Report saved as '{filename}'.")
def view_todays_tasks(data, username):
    if username not in data["users"]:
        print(f"User '{username}' not found.")
        return
    today = date.today().isoformat()
    user_data = data["users"][username]
    if today not in user_data.get("task_history", {}):
        print("No tasks logged today.")
        return
    print("\nTasks logged today:")
    for task, qty in user_data["task_history"][today].items():
        print(f"{task}: {qty}")
    print("\nTasks not logged today:")
    completed_tasks = set(user_data["task_history"][today].keys())
    all_tasks = set(data["tasks"].keys())
    for task in all_tasks - completed_tasks:
        print(f"{task}")
    input("\nPress Enter to continue...")
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")
def main():
    data = load_data()
    clear_terminal()
    username = input("Enter your username 📝: ")
    add_user(data, username)
    clear_terminal()
    while True:
        user_data = data["users"][username]
        level = calculate_level(user_data["points"])
        rank = calculate_rank(level)
        print(f"Status for '{username}': Points: {user_data['points']}, Level: {level}, Rank: {rank}, Streak: {user_data['streak']}\n")
        remaining_tasks = get_remaining_tasks(data, username)
        if remaining_tasks:
            print("Tasks remaining for today:")
            for task in remaining_tasks:
                print(f"- {task}")
        else:
            print("All tasks completed for today! 🎉\n")
        # Show only today's redeemed rewards instead of historical ones
        todays_redeemed = [reward for reward, _ in data["users"][username]["daily_rewards"]["redeemed"]]
        if todays_redeemed:
            print(f"Today's redeemed rewards: {', '.join(todays_redeemed)}")
       
        daily_rewards = ensure_daily_rewards(data, username)
        available_count = len(daily_rewards["available"])
        redeemed_count = len(daily_rewards["redeemed"])
        print(f"\nDaily Rewards: {available_count} available, {redeemed_count} redeemed today\n1. Log Tasks\n2. Redeem Reward\n3. Export\n4. Exit")
        choice = input("Choose an option (1-4): ")
        if choice == "1":
            clear_terminal()
            while True:
                day = input("Enter the day (m, tu, w, th, f, sa, sun): ").strip().lower()
                if get_daily_double_tasks(day) is not None:
                    break
                print("Invalid day abbreviation. Please try again.")
            log_tasks(data, username, day)
        elif choice == "2":
            clear_terminal()
            redeem_reward(data, username)
        elif choice == "3":
            clear_terminal()
            export_user_data(data, username)
        elif choice == "4":
            clear_terminal()
            print("Goodbye!👋")
            break
        else:
            print("Invalid option.")
if __name__ == "__main__":
    main()
