import questionary
import functions as func
from hclasses import Habit
from validator import user_name_validator, habit_name_validator, habit_description_validator, date_validator


habit_dictionary = Habit.Instances
run_main = True
ask_main_question = True
main_question = ""


def user_login():
    run_login = True
    print("Welcome to your habit tracker.")

    while run_login:

        username = questionary.text(
            "Please enter your name to login or to create a new account:",
            validate=user_name_validator).ask()

        if func.username_exists(username):
            run_login = False
            Habit.change_db(username)
            Habit.load()

        else:
            create_username = questionary.select(
                "Username not found. Create new account?",
                choices=["Yes",
                         "No"]).ask()

            if create_username == "Yes":
                run_login = False
                Habit.change_db(username)
                func.create_predefined_habits()


def main_menu():
    global run_main
    global main_question

    while run_main:
        if ask_main_question:
            main_question = questionary.select(
                "What do you want to do?",
                choices=["Manage habits",
                         "Check-off habits",
                         "Analyze habits",
                         "Exit"]).ask()

        if main_question == "Manage habits":
            manage_habits_menu()

        elif main_question == "Check-off habits":
            checkoff_habits_menu()

        elif main_question == "Analyze habits":
            analyze_habits_menu()

        elif main_question == "Exit":
            run_main = False


def manage_habits_menu():
    global ask_main_question
    global main_question

    manage_menu_question = questionary.select(
        "Manage your habits",
        choices=["Create habit",
                 "Edit habit",
                 "Delete habit",
                 "Inspect habits",
                 "Back"
                 ]).ask()

    if manage_menu_question == "Create habit":
        create_habit_period = questionary.select(
            "What type of habit do you want to create?",
            choices=["Daily",
                     "Weekly"]).ask()
        create_habit_name = questionary.text(
            "Please enter your habit name:",
            validate=habit_name_validator).ask()
        create_habit_description = questionary.text(
            "Please enter a habit description:",
            validate=habit_description_validator).ask()

        # create habit and print message
        func.create_habit(create_habit_period, create_habit_name, create_habit_description)
        print(func.habit_created_info(create_habit_period, create_habit_name, create_habit_description))

        # return to "Manage habits" menu
        return_manage_habit_menu()

    elif manage_menu_question == "Edit habit":
        edit_habit = questionary.select(
            "Which habit would you like to edit?",
            choices=func.list_habits(habit_dictionary)
        ).ask()
        edit_attribute = questionary.select(
            "What would you like to change?",
            choices=["Name",
                     "Description"
                     ]).ask()

        if edit_attribute == "Name":
            new_name = questionary.text(
                "Please enter a new habit name:",
                validate=habit_name_validator).ask()
            # change habit name and save
            habit_dictionary[edit_habit].update_name(new_name)
            habit_dictionary[new_name].save()

        elif edit_attribute == "Description":
            new_description = questionary.text(
                "Please enter a new description:",
                validate=habit_description_validator).ask()
            # change habit description and save
            habit_dictionary[edit_habit].update_description(new_description)
            habit_dictionary[edit_habit].save()

        # return to "Manage habits" menu
        return_manage_habit_menu()

    elif manage_menu_question == "Delete habit":
        del_habit = questionary.select(
            "Which habit would you like to delete?",
            choices=func.list_habits(habit_dictionary)
        ).ask()
        confirm_deletion = questionary.select(
            f"Delete {del_habit}?",
            choices=["Yes",
                     "No"
                     ]).ask()
        if confirm_deletion == "Yes":
            habit_dictionary[del_habit].delete()
        elif confirm_deletion == "No":
            # return to manage habits, ideally should return to delete
            return_manage_habit_menu()

    elif manage_menu_question == "Inspect habits":
        list_habit_question = questionary.select(
            "Choose habit type:",
            choices=["All",
                     "Daily",
                     "Weekly"
                     ]).ask()
        if list_habit_question == "All":
            list_choice = questionary.select(
                "Choose habit:",
                choices=func.list_habits(habit_dictionary)
            ).ask()
        else:
            list_choice = questionary.select(
                f"Choose {list_habit_question} habit:",
                choices=func.list_habits(habit_dictionary, period=list_habit_question)
            ).ask()

        # print habit
        print(func.habit_info(habit_dictionary[list_choice]))

        # return to "Manage habits" menu
        return_manage_habit_menu()

    elif manage_menu_question == "Back":
        return_main_menu()


def checkoff_habits_menu():
    global ask_main_question
    global main_question

    checkoff_menu_question = questionary.select(
        "What would you like to do?",
        choices=["Check-off",
                 "Manual check-off",
                 "Back"
                 ]).ask()

    if checkoff_menu_question == "Check-off":
        check_habit = questionary.select(
            "Which habit would you like to check-off?",
            choices=func.list_habits(habit_dictionary)).ask()

        habit_dictionary[check_habit].checkoff_streak()
        habit_dictionary[check_habit].save()

        # return to "Check-off habits" menu
        return_checkoff_menu()

    elif checkoff_menu_question == "Manual check-off":
        check_habit = questionary.select(
            "Which habit would you like to check-off?",
            choices=func.list_habits(habit_dictionary)).ask()
        check_date = questionary.text(
            "Please enter the date:",
            validate=date_validator).ask()

        habit_dictionary[check_habit].checkoff_streak(date=check_date)
        habit_dictionary[check_habit].save()

        # return to "Check-off habits" menu
        return_checkoff_menu()

    elif checkoff_menu_question == "Back":
        return_main_menu()


def analyze_habits_menu():
    global ask_main_question
    global main_question

    analyze_habit_question = questionary.select(
        "Analyze your habits",
        choices=["Show active habits",
                 "Show inactive habits",
                 "Show current streak",
                 "Show longest streak",
                 "Back"
                 ]).ask()

    if analyze_habit_question == "Show active habits":
        print(f"These are your active habits: " +
              f"{func.habit_list_as_string(func.list_active(habit_dictionary))}")

        # return to "Analyze habits" menu
        return_analyze_menu()

    if analyze_habit_question == "Show inactive habits":
        print(f"These are your inactive habits: " +
              f"{func.habit_list_as_string(func.list_active(habit_dictionary, active=False))}")

        # return to "Analyze habits" menu
        return_analyze_menu()

    if analyze_habit_question == "Show current streak":
        analyze_streak_question = questionary.select(
            "Do you want to analyze a single habit or all habits?",
            choices=["Single",
                     "All"]).ask()

        if analyze_streak_question == "Single":
            single_streak_question = questionary.select(
                "For which habit do you want to analyze the streak?",
                choices=func.list_habits(habit_dictionary)).ask()

            print(f"Your current streak for the habit {single_streak_question} is: " +
                  str(habit_dictionary[single_streak_question].streak()))

        elif analyze_streak_question == "All":
            print("Here are the current streaks for all your habits:\n" +
                  func.habit_streak_string(func.list_streak(habit_dictionary)))

        # return to "Analyze habits" menu
        return_analyze_menu()

    elif analyze_habit_question == "Show longest streak":
        analyze_longest_question = questionary.select(
            "Do you want to analyze a single habit or all habits?",
            choices=["Single",
                     "All"]).ask()

        if analyze_longest_question == "Single":
            single_longest_question = questionary.select(
                "For which habit do you want to analyze the longest streak?",
                choices=func.list_habits(habit_dictionary)).ask()

            print(f"Your longest streak for the habit {single_longest_question} is: " +
                  str(habit_dictionary[single_longest_question].longest_streak()))

        elif analyze_longest_question == "All":
            print("Here are the longest streaks for all your habits:\n" +
                  func.habit_streak_string(func.list_longest_streak(habit_dictionary)))

        # return to "Analyze habits" menu
        return_analyze_menu()

    elif analyze_habit_question == "Back":
        return_main_menu()


def return_main_menu():
    global main_question
    global ask_main_question

    main_question = "Main"
    ask_main_question = True


def return_manage_habit_menu():
    global ask_main_question
    global main_question

    ask_main_question = False
    main_question = "Manage habits"


def return_checkoff_menu():
    global ask_main_question
    global main_question

    ask_main_question = False
    main_question = "Check-off habits"


def return_analyze_menu():
    global ask_main_question
    global main_question

    ask_main_question = False
    main_question = "Analyze habits"
