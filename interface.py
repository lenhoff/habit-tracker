import constants as const
import questionary
import functions as func
from hclasses import Habit
from validator import user_name_validator, habit_name_validator, habit_description_validator, date_validator
from hanalytics import list_habits, list_active, list_streak, list_longest_streak


def user_login():
    print(" Welcome to your habit tracker.")
    while const.run_login:

        username = questionary.text(
            "Please enter your name to login or to create a new account:",
            validate=user_name_validator).ask()

        if func.username_exists(username):
            const.run_login = False
            Habit.change_database(username)

        else:
            create_username = questionary.select(
                "Username not found. Create new account?",
                choices=["Yes",
                         "No"]).ask()

            if create_username == "Yes":
                const.run_login = False
                Habit.change_database(username)
                func.create_predefined_habits()


def main_menu():
    while const.run_main:
        if const.ask_main_question:
            const.main_question = questionary.select(
                "What do you want to do?",
                choices=["Manage habits",
                         "Check-off habits",
                         "Analyze habits",
                         "Exit"]
            ).ask()

        # Work in progress: return
        if const.main_question == "Manage habits":
            manage_habit_question = questionary.select(
                "Manage your habits",
                choices=["Create habit",
                         "Edit habit",
                         "Delete habit",
                         "Inspect habits",
                         "Back"
                         ]).ask()

            # Work in progress: return
            if manage_habit_question == "Create habit":
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
                const.ask_main_question = False
                const.main_question = "Manage habits"

            # Work in progress: return
            elif manage_habit_question == "Edit habit":
                edit_habit = questionary.select(
                    "Which habit would you like to edit?",
                    choices=list_habits(const.habit_dictionary)
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
                    const.habit_dictionary[edit_habit].update_name(new_name)
                    const.habit_dictionary[new_name].save()

                elif edit_attribute == "Description":
                    new_description = questionary.text(
                        "Please enter a new description:",
                        validate=habit_description_validator).ask()
                    # change habit description and save
                    const.habit_dictionary[edit_habit].update_description(new_description)
                    const.habit_dictionary[edit_habit].save()

                # return to "Manage habits" menu
                const.ask_main_question = False
                const.main_question = "Manage habits"

            # Work in progress: return
            elif manage_habit_question == "Delete habit":
                del_habit = questionary.select(
                    "Which habit would you like to delete?",
                    choices=list_habits(const.habit_dictionary)
                ).ask()
                confirm_deletion = questionary.select(
                    f"Delete {del_habit}?",
                    choices=["Yes",
                             "No"
                             ]).ask()
                if confirm_deletion == "Yes":
                    const.habit_dictionary[del_habit].delete()
                elif confirm_deletion == "No":
                    # return to manage habits, ideally should return to delete
                    const.ask_main_question = False
                    const.main_question = "Manage habits"

            # Work in progress: return
            elif manage_habit_question == "Inspect habits":
                list_habit_question = questionary.select(
                    "Choose habit type:",
                    choices=["All",
                             "Daily",
                             "Weekly"
                             ]).ask()
                if list_habit_question == "All":
                    list_choice = questionary.select(
                        "Choose habit:",
                        choices=list_habits(const.habit_dictionary)
                    ).ask()
                else:
                    list_choice = questionary.select(
                        f"Choose {list_habit_question} habit:",
                        choices=list_habits(const.habit_dictionary, period=list_habit_question)
                    ).ask()

                # print habit
                print(func.habit_info(const.habit_dictionary[list_choice]))

                # return to "Manage habits" menu
                const.ask_main_question = False
                const.main_question = "Manage habits"

            # DONE
            elif manage_habit_question == "Back":
                const.ask_main_question = True

        # Work in progress: return, maybe add "check all"
        elif const.main_question == "Check-off habits":
            check_menu = questionary.select(
                "What would you like to do?",
                choices=["Check-off",
                         "Manual check-off",
                         "Back"
                         ]).ask()

            # Work in progress: return
            if check_menu == "Check-off":
                check_habit = questionary.select(
                    "Which habit would you like to check-off?",
                    choices=list_habits(const.habit_dictionary)).ask()

                const.habit_dictionary[check_habit].check_streak()
                const.habit_dictionary[check_habit].save()

                # return to "Check-off habits" menu
                const.ask_main_question = False
                const.main_question = "Check-off habits"

            # Work in progress: return
            elif check_menu == "Manual check-off":
                check_habit = questionary.select(
                    "Which habit would you like to check-off?",
                    choices=list_habits(const.habit_dictionary)).ask()
                check_date = questionary.text(
                    "Please enter the date:",
                    validate=date_validator).ask()

                const.habit_dictionary[check_habit].check_streak(date=check_date)
                const.habit_dictionary[check_habit].save()

                # return to "Check-off habits" menu
                const.ask_main_question = False
                const.main_question = "Check-off habits"

            # DONE
            elif check_menu == "Back":
                const.ask_main_question = True

        # DONE
        elif const.main_question == "Analyze habits":
            analyze_habit_question = questionary.select(
                "Analyze your habits",
                choices=["Show active habits",
                         "Show inactive habits",
                         "Show current streak",
                         "Show longest streak",
                         "Back"
                         ]).ask()

            # DONE
            if analyze_habit_question == "Show active habits":
                print(f"These are your active habits: " +
                      f"{func.habit_list_as_string(list_active(const.habit_dictionary))}")

                # return to "Analyze habits" menu
                const.ask_main_question = False
                const.main_question = "Analyze habits"

            # DONE
            if analyze_habit_question == "Show inactive habits":
                print(f"These are your inactive habits: " +
                      f"{func.habit_list_as_string(list_active(const.habit_dictionary, active=False))}")

                # return to "Analyze habits" menu
                const.ask_main_question = False
                const.main_question = "Analyze habits"

            # DONE
            if analyze_habit_question == "Show current streak":
                analyze_streak_question = questionary.select(
                    "Do you want to analyze a single habit or all habits?",
                    choices=["Single",
                             "All"]).ask()

                if analyze_streak_question == "Single":
                    single_longest_question = questionary.select(
                        "For which habit do you want to analyze the streak?",
                        choices=list_habits(const.habit_dictionary)).ask()

                    print(f"Your current streak for the habit {single_longest_question} is: " +
                          str(const.habit_dictionary[single_longest_question].streak()))

                    # return to "Analyze habits" menu
                    const.ask_main_question = False
                    const.main_question = "Analyze habits"

                elif analyze_streak_question == "All":
                    print("Here are the current streaks for all your habits:\n" +
                          func.habit_streak_string(list_streak(const.habit_dictionary)))

                    # return to "Analyze habits" menu
                    const.ask_main_question = False
                    const.main_question = "Analyze habits"

            # DONE
            elif analyze_habit_question == "Show longest streak":
                analyze_longest_question = questionary.select(
                    "Do you want to analyze a single habit or all habits?",
                    choices=["Single",
                             "All"]).ask()

                if analyze_longest_question == "Single":
                    single_longest_question = questionary.select(
                        "For which habit do you want to analyze the longest streak?",
                        choices=list_habits(const.habit_dictionary)).ask()

                    print(f"Your longest streak for the habit {single_longest_question} is: " +
                          str(const.habit_dictionary[single_longest_question].longest_streak()))

                    # return to "Analyze habits" menu
                    const.ask_main_question = False
                    const.main_question = "Analyze habits"

                elif analyze_longest_question == "All":
                    print("Here are the longest streaks for all your habits:\n" +
                          func.habit_streak_string(list_longest_streak(const.habit_dictionary)))

                    # return to "Analyze habits" menu
                    const.ask_main_question = False
                    const.main_question = "Analyze habits"

            # DONE
            elif analyze_habit_question == "Back":
                const.ask_main_question = True

        elif const.main_question == "Exit":
            const.run_main = False
