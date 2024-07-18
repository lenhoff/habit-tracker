from functions import list_habits
from hclasses import Habit
from datetime import datetime


def user_name_validator(name):
    if len(name) == 0:
        return "Username must be at least one character long."
    elif len(name) > 20:
        return "Username cannot exceed 20 characters."
    elif not name.isalnum():
        return "Username cannot contain special characters."
    elif name == "_test":
        return f"Username {name} is reserved for test purposes."
    else:
        return True


def habit_name_validator(habit_name):
    if len(habit_name) == 0:
        return "Habit name must be at least one character long."
    elif habit_name in list_habits(Habit.Instances):
        return "Habit name already taken."
    else:
        return True


def habit_description_validator(description):
    if len(description) == 0:
        return "Description must be at least one character long."
    if len(description) > 100:
        return "Description must be 100 characters or shorter"
    else:
        return True


def date_validator(date_entered):
    try:
        date = datetime.strptime(date_entered, "%Y-%m-%d").date()
    except ValueError:
        return "Date must match format YYYY-MM-DD"
    else:
        today = datetime.today().date()
        if (today - date).days < 0:
            return "Future dates cannot be entered."
        else:
            return True
