import os
from hclasses import Habit, Daily, Weekly


def username_exists(username):
    database = str(username) + ".db"
    return os.path.exists(database)


def create_predefined_habits():
    Daily("Brush", "Brush your teeth at least once a day.")
    Daily("Duolingo", "Do a lesson on Duolingo.")
    Daily("Exercise", "Exercise for 30 minutes.")
    Weekly("Plants", "Water your plants every week.")
    Weekly("Clean", "Clean your apartment.")

    for habit in Habit.Instances.values():
        habit.save()


def create_habit(period, name, description):
    if period == "Daily":
        Daily(name, description)
    elif period == "Weekly":
        Weekly(name, description)

    Habit.Instances[name].save()


def habit_created_info(period, name, description):
    info = (f"\n" +
            f"You have created a '{period}' habit " +
            f"with the name '{name}' " +
            f"and the description '{description}'.\n")

    return info


def habit_info(habit):
    if habit.is_active():
        activity = "active"
    else:
        activity = "inactive"

    info = (f"\n" +
            f"Name: '{habit.name}', Description: '{habit.description}'\n" +
            f"Type: {habit.period}, Date of creation: {habit.date_created}\n" +
            f"Streak: {habit.streak()}, Longest streak: {habit.longest_streak()}\n" +
            f"This habit is currently {activity}.\n")

    return info


def list_habits(habit_dict, period=None):
    if period:
        return [habit for habit in habit_dict if habit_dict[habit].period == period]
    else:
        return [habit for habit in habit_dict]


def list_active(habit_dict, active=True):
    if active:
        return [habit for habit in habit_dict if habit_dict[habit].is_active()]
    else:
        return [habit for habit in habit_dict if not habit_dict[habit].is_active()]


def list_streak(habit_dict, habit=None):
    if habit:
        return habit_dict[habit].streak()
    else:
        streak_dict = {}
        for habit in habit_dict:
            streak_dict.update({habit: habit_dict[habit].streak()})

        return streak_dict


def list_longest_streak(habit_dict, habit=None):
    if habit:
        return habit_dict[habit].longest_streak()
    else:
        streak_dict = {}
        for habit in habit_dict:
            streak_dict.update({habit: habit_dict[habit].longest_streak()})

        return streak_dict


def habit_list_as_string(habit_list):
    separator = ", "
    return separator.join(habit_list)


def habit_streak_string(streak_dict):
    combined_list = [("Habit: " + habit + " - ") +
                     ("Streak: " + str(streak)) for habit, streak in zip(streak_dict.keys(), streak_dict.values())]
    separator = "\n"
    return separator.join(combined_list)
