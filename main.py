import questionary
from main_functions import create_predefined_habits, habit_info, create_habit, habit_created_info
from validator import user_name_validator, habit_name_validator, habit_description_validator, date_validator
from hclasses import Habit, Daily, Weekly
from hanalytics import list_habits, list_active

is_running = True
ask_main = True
main_question = ""
habit_dictionary = Habit.instances

# start
# create_predefined_habits()
Habit.load()

while is_running:
    if ask_main:
        main_question = questionary.select(
            "What do you want to do?",
            choices=["Manage habits",
                     "Check-off habits",
                     "Analyze habits",
                     "Exit"]
        ).ask()

    # Work in progress: return
    if main_question == "Manage habits":
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
            create_habit(create_habit_period, create_habit_name, create_habit_description)
            print(habit_created_info(create_habit_period, create_habit_name, create_habit_description))

            # return to "Manage habits" menu
            ask_main = False
            main_question = "Manage habits"

        # Work in progress: return
        elif manage_habit_question == "Edit habit":
            edit_habit = questionary.select(
                "Which habit would you like to edit?",
                choices=list_habits(habit_dictionary)
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
            ask_main = False
            main_question = "Manage habits"

        # Work in progress: return
        elif manage_habit_question == "Delete habit":
            del_habit = questionary.select(
                "Which habit would you like to delete?",
                choices=list_habits(habit_dictionary)
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
                ask_main = False
                main_question = "Manage habits"

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
                    choices=list_habits(habit_dictionary)
                ).ask()
            else:
                list_choice = questionary.select(
                    f"Choose {list_habit_question} habit:",
                    choices=list_habits(habit_dictionary, period=list_habit_question)
                ).ask()

            # print habit
            print(habit_info(habit_dictionary[list_choice]))

            # return to "Manage habits" menu
            ask_main = False
            main_question = "Manage habits"

        # DONE
        elif manage_habit_question == "Back":
            ask_main = True

    # Work in progress: return
    elif main_question == "Check-off habits":
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
                choices=list_habits(habit_dictionary)).ask()

            habit_dictionary[check_habit].check_streak()
            habit_dictionary[check_habit].save()

            # return to "Check-off habits" menu
            ask_main = False
            main_question = "Check-off habits"

        # Work in progress: return
        elif check_menu == "Manual check-off":
            check_habit = questionary.select(
                "Which habit would you like to check-off?",
                choices=list_habits(habit_dictionary)).ask()
            check_date = questionary.text(
                "Please enter the date:",
                validate=date_validator).ask()

            habit_dictionary[check_habit].check_streak(date=check_date)
            habit_dictionary[check_habit].save()

            # return to "Check-off habits" menu
            ask_main = False
            main_question = "Check-off habits"

        # DONE
        elif check_menu == "Back":
            ask_main = True

    # Work in progress: Analyze streak, analyze longest_streak
    elif main_question == "Analyze habits":
        analyze_habit_question = questionary.select(
            "Analyze your habits",
            choices=["Show active habits",
                     "Show inactive habits",
                     "Show current streak",
                     "Show longest streak",
                     "Back"
                     ]).ask()

        # Improve string return
        if analyze_habit_question == "Show active habits":
            print(list_active(habit_dictionary))

            # return to "Analyze habits" menu
            ask_main = False
            main_question = "Analyze habits"

        # Improve string return
        if analyze_habit_question == "Show inactive habits":
            print(list_active(habit_dictionary, active=False))

            # return to "Analyze habits" menu
            ask_main = False
            main_question = "Analyze habits"

        # All vs single
        if analyze_habit_question == "Show current streak":
            print("Showing current streak!")

        # All vs single
        elif analyze_habit_question == "Show longest streak":
            print("Showing longest streak!")

        # DONE
        elif analyze_habit_question == "Back":
            ask_main = True

    elif main_question == "Exit":
        is_running = False
