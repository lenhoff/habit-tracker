from hclasses import Habit, Daily, Weekly
from datetime import datetime
from hanalytics import list_habits, list_streak, list_longest_streak, list_active
from main_functions import create_predefined_habits


def test_create_habits():
    Daily(name="brushing teeth", description="brush twice per day")
    Weekly(name="gym", description="work out once a week")

    example_date_1 = datetime(2024, 7, 8).date()
    example_date_2 = datetime(2024, 7, 1).date()

    Habit.instances["brushing teeth"].dates_checked.append(example_date_1)
    Habit.instances["gym"].dates_checked.append(example_date_2)


# test_create_habits()
# create_predefined_habits()
Habit.load()

# for habit in Habit.instances.values():
#     habit.save()

print(list_habits(Habit.instances, period="Daily"))
print(Habit.instances["Exercise"].dates_checked)
Habit.instances["Exercise"].check_streak(date="2024-07-10")
print(Habit.instances["Exercise"].dates_checked)
Habit.instances["Exercise"].check_streak(date="2024-07-12")
print(Habit.instances["Exercise"])

