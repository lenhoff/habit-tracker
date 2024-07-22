from functions import list_habits
from habit_classes import Habit
from datetime import datetime


def user_name_validator(name: str):
    if len(name) == 0:
        return "Username must be at least one character long."
    elif len(name) > 20:
        return "Username cannot exceed 20 characters."
    elif not name.isalnum():
        return "Username cannot contain special characters."
    else:
        return True


def habit_name_validator(habit_name: str):
    if len(habit_name) == 0 or len(habit_name) > 50:
        return "Habit name must be between 1 and 50 characters long."
    elif habit_name in list_habits(Habit.Instances):
        return "Habit name already taken."
    else:
        return True


def habit_description_validator(description: str):
    if len(description) == 0 or len(description) > 100:
        return "Description must be between 1 and 100 characters long."
    else:
        return True


def date_validator(date_entered: str):
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
