import os
from habit_classes import Habit, Daily, Weekly


def username_exists(username: str) -> bool:
    """
    Function to check if username exists in current path.

    Returns:
        int
    """
    if not type(username) is str:
        raise ValueError("username must be of type: str")

    database = username + ".db"
    return os.path.exists(database)


def create_predefined_habits() -> None:
    """
    Function to create five pre-defined habits and save them to user database.
    """
    Daily("Brush", "Brush your teeth at least once a day.")
    Daily("Duolingo", "Do a lesson on Duolingo.")
    Daily("Exercise", "Exercise for 30 minutes.")
    Weekly("Plants", "Water your plants every week.")
    Weekly("Clean", "Clean your apartment.")

    for habit in Habit.Instances.values():
        habit.save()


def create_habit(period: str, name: str, description: str):
    """
    Function to create a habit and save it to the database.

    Args:
        period (str): Desired periodicity of habit ('Daily'/'Weekly')
        name (str): Name of habit
        description (str): Description of habit

    """
    if not period == "Daily" and not period == "Weekly":
        raise ValueError("period must be 'Daily' or 'Weekly'")
    if not type(name) is str or not type(description) is str:
        raise ValueError("name and description must be of type: str")

    if period == "Daily":
        Daily(name, description)
    elif period == "Weekly":
        Weekly(name, description)

    Habit.Instances[name].save()


def habit_created_info(period: str, name: str, description: str) -> str:
    """
        Function to return an info string for a created habit.

        Args:
            period (str): Desired periodicity of habit ('Daily'/'Weekly')
            name (str): Name of habit
            description (str): Description of habit

        Returns:
            str
    """
    info = (f"\n" +
            f"You have created a '{period}' habit " +
            f"with the name '{name}' " +
            f"and the description '{description}'.\n")

    return info


def habit_info(habit: Habit) -> str:
    """
        Function to return an info string for a habit.

        Args:
            habit (Habit): A 'Daily'/'Weekly' object

        Returns:
            str
    """
    if habit.is_active():
        activity = "active"
    else:
        activity = "inactive"

    info = (f"\n" +
            f"Name: '{habit._name}', Description: '{habit._description}'\n" +
            f"Type: {habit._period}, Date of creation: {habit._date_created}\n" +
            f"Streak: {habit.streak()}, Longest streak: {habit.longest_streak()}\n" +
            f"This habit is currently {activity}.\n")

    return info


def list_habits(habit_dict: dict, period: str = None) -> list:
    """
    Function to create a list of all Habit instances ('Daily'/'Weekly').

    Args:
        habit_dict (dict): Desired habit dictionary. Should be Habit.Instances!
        period (str) = None: Optional argument to specify habit type to be listed ('Daily'/'Weekly')

    Returns:
        list
    """
    if not type(habit_dict) is dict:
        raise ValueError("habit_dict should be of type: dict --- ideally Habit.Instances!")
    if type(period) is not str and period is not None:
        raise ValueError("period should be of type: str --- ideally 'Daily'/'Weekly'")

    if period:
        return [habit for habit in habit_dict if habit_dict[habit]._period == period]
    else:
        return [habit for habit in habit_dict]


def list_active(habit_dict: dict, active: bool = True) -> list:
    """
    Function to create a list of active/inactive habits.

    Args:
        habit_dict (dict): Desired habit dictionary. Should be Habit.Instances!
        active (bool) = True: Argument to choose whether active or inactive habits should be listed

    Returns:
        list
    """
    if not type(habit_dict) is dict:
        raise ValueError("habit_dict should be of type: dict --- ideally Habit.Instances!")
    if not type(active) is bool:
        raise ValueError("active should be of type: bool")

    if active:
        return [habit for habit in habit_dict if habit_dict[habit].is_active()]
    else:
        return [habit for habit in habit_dict if not habit_dict[habit].is_active()]


def list_streak(habit_dict: dict) -> dict:
    """
       Function to return a dictionary containing all habits and their streaks. Key: habit, value: streak

       Args:
           habit_dict (dict): Desired habit dictionary. Should be Habit.Instances!

       Returns:
           dict
   """
    if not type(habit_dict) is dict:
        raise ValueError("habit_dict should be of type: dict --- ideally Habit.Instances!")

    streak_dict = {}
    for habit in habit_dict:
        streak_dict.update({habit: habit_dict[habit].streak()})

    return streak_dict


def list_longest_streak(habit_dict: dict) -> dict:
    """
       Function to return a dictionary containing all habits and their longest streaks. Key: habit,
       value: longest streak

       Args:
           habit_dict (dict): Desired habit dictionary. Should be Habit.Instances!

       Returns:
           dict
   """
    if not type(habit_dict) is dict:
        raise ValueError("habit_dict should be of type: dict --- ideally Habit.Instances!")

    streak_dict = {}
    for habit in habit_dict:
        streak_dict.update({habit: habit_dict[habit].longest_streak()})

    return streak_dict


def habit_list_as_string(habit_list: list) -> str:
    """
       Function to convert a list of habits to a formatted string separated by commas.

       Args:
           habit_list (list): List of habits. Ideally created by list_habits() or list_active()

       Returns:
           str
   """
    if not type(habit_list) is list:
        raise ValueError("habit_list should be of type: list")

    separator = ", "
    return separator.join(habit_list)


def habit_streak_string(streak_dict: dict) -> str:
    """
       Function to convert streak dictionary (key: habit, value: streak) into a formatted string.
       Format - Habit: 'habit' - Streak: 'streak'

       Args:
           streak_dict (dict): Streak dictionary. Ideally created by list_streak() or list_longest_streak()

       Returns:
           str
   """
    if not type(streak_dict) is dict:
        raise ValueError("streak_dict should be of type: dict")

    combined_list = [("Habit: " + habit + " - ") +
                     ("Streak: " + str(streak)) for habit, streak in zip(streak_dict.keys(), streak_dict.values())]
    separator = "\n"
    return separator.join(combined_list)
