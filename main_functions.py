from hclasses import Habit, Daily, Weekly
from datetime import datetime


def create_predefined_habits():
    Daily("Brush teeth", "Brush your teeth at least once a week. Ideally twice.")
    Daily("Duolingo", "Do a lesson on Duolingo.")
    Daily("Exercise", "Exercise for 30 minutes.")
    Weekly("Plants", "Water your plants every week.")
    Weekly("Clean", "Clean your apartment.")

    for habit in Habit.instances.values():
        habit.save()


def create_habit(period, name, description):
    if period == "Daily":
        Daily(name, description)
    elif period == "Weekly":
        Weekly(name, description)

    Habit.instances[name].save()


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

