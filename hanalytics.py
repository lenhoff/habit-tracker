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

