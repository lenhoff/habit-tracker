from hanalytics import list_habits
from hclasses import Habit
from datetime import datetime


# example = ["a", "aa"]  # will be replaced with Habit.instances


def user_name_validator(name):
    pass


def habit_name_validator(string):
    if len(string) == 0:
        return "Habit name must be at least one character long."
    elif string in list_habits(Habit.instances):
        return "Habit name already taken."
    else:
        return True


def habit_description_validator(string):
    if len(string) == 0:
        return "Description must be at least one character long."
    if len(string) > 100:
        return "Description must be 100 characters or shorter"
    else:
        return True


def date_validator(string):
    try:
        date = datetime.strptime(string, "%Y-%m-%d").date()
    except ValueError:
        return "Date must match format YYYY-MM-DD"
    else:
        today = datetime.today().date()
        if (today - date).days < 0:
            return "Future dates cannot be entered."
        else:
            return True

