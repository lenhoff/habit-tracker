import pytest
import sqlite3
from habit_classes import Habit, Daily, Weekly
import functions as func
import os
from freezegun import freeze_time


@pytest.fixture
def temporary_database():
    # setup: create test database
    Habit.Instances = {}
    Habit.change_db("_test")

    # refresh database (drop habit and tracking table and create them again)
    conn = sqlite3.connect(Habit._DB_NAME)

    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS habit")
    cursor.execute("DROP TABLE IF EXISTS tracking")
    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS habit (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            description TEXT NOT NULL,
                            period TEXT NOT NULL,
                            date_created TEXT NOT NULL
                        )        
                    """)
    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS tracking (
                            id INTEGER PRIMARY KEY,
                            habit_id INTEGER,
                            date_checked TEXT,
                            FOREIGN KEY (habit_id) REFERENCES habit(id)
                        )   
                    """)
    conn.commit()

    yield

    # teardown: close database connection, delete habits
    conn.close()
    Habit.Instances = {}


@pytest.fixture
def predefined_habits():
    # setup: create five predefined habits
    # habit 1 - Brush teeth, Daily
    example_habit_1 = Daily("Brush", "Brush your teeth at least once a day.")
    # tracked dates from 22.12.14 to 18.01.15, missing date: 05.01.15
    # expected streak on 18.01.15: 13, expected longest streak: 14
    example_dates_1 = ["2014-12-22", "2014-12-23", "2014-12-24", "2014-12-25", "2014-12-26", "2014-12-27", "2014-12-28",
                       "2014-12-29", "2014-12-30", "2014-12-31", "2015-01-01", "2015-01-02", "2015-01-03", "2015-01-04",
                       "2015-01-06", "2015-01-07", "2015-01-08", "2015-01-09", "2015-01-10", "2015-01-11",
                       "2015-01-12", "2015-01-13", "2015-01-14", "2015-01-15", "2015-01-16", "2015-01-17", "2015-01-18"]

    for date in example_dates_1:
        example_habit_1.checkoff_streak(date=date)

    # habit 2 - Duolingo, Daily
    example_habit_2 = Daily("Duolingo", "Do a lesson on Duolingo.")
    # tracked dates from 22.12.14 to 18.01.15, missing date: 05.01.15, dates are scrambled
    # expected streak on 18.01.15: 13, expected longest streak: 14
    example_dates_2 = ["2014-12-23", "2014-12-22", "2014-12-25", "2014-12-24", "2014-12-27", "2014-12-26", "2014-12-29",
                       "2014-12-28", "2014-12-31", "2014-12-30", "2015-01-02", "2015-01-01", "2015-01-04", "2015-01-03",
                       "2015-01-11", "2015-01-10", "2015-01-09", "2015-01-08", "2015-01-07", "2015-01-06",
                       "2015-01-18", "2015-01-17", "2015-01-16", "2015-01-15", "2015-01-14", "2015-01-13", "2015-01-12"]

    for date in example_dates_2:
        example_habit_2.checkoff_streak(date=date)

    # habit 3 - Exercise, Daily
    example_habit_3 = Daily("Exercise", "Exercise for 30 minutes.")
    # tracked dates from 22.12.14 to 18.01.15, missing dates: 28.12.14, 18.01.15
    # expected streak on 18.01.15: 0, expected longest streak: 20
    example_dates_3 = ["2014-12-22", "2014-12-23", "2014-12-24", "2014-12-25", "2014-12-26", "2014-12-27",
                       "2014-12-29", "2014-12-30", "2014-12-31", "2015-01-01", "2015-01-02", "2015-01-03", "2015-01-04",
                       "2015-01-05", "2015-01-06", "2015-01-07", "2015-01-08", "2015-01-09", "2015-01-10", "2015-01-11",
                       "2015-01-12", "2015-01-13", "2015-01-14", "2015-01-15", "2015-01-16", "2015-01-17"]

    for date in example_dates_3:
        example_habit_3.checkoff_streak(date=date)

    # habit 4 - Plants, Weekly
    example_habit_4 = Weekly("Plants", "Water your plants every week.")
    # tracked dates from 22.12.14 (week 52) to 18.01.15 (week 3), date entered every week
    # expected streak on 18.01.15: 4, expected longest streak: 4
    example_dates_4 = ["2014-12-22",
                       "2015-01-04",
                       "2015-01-05",
                       "2015-01-18"]
    for date in example_dates_4:
        example_habit_4.checkoff_streak(date=date)

    # habit 5 - Clean, Weekly
    example_habit_5 = Weekly("Clean", "Clean your apartment.")
    # tracked dates from 22.12.14 (week 52) to 18.01.15 (week 3), no date entered for week 2 (05.01.14 - 11.01.15)
    # expected streak on 18.01.14: 1, expected longest streak: 2
    example_dates_5 = ["2014-12-24",
                       "2015-01-01",
                       "2015-01-18"]
    for date in example_dates_5:
        example_habit_5.checkoff_streak(date=date)

    yield [example_habit_1, example_habit_2, example_habit_3, example_habit_4, example_habit_5]

    # teardown: delete habits and reset database
    Habit.Instances = {}
    Habit._DB_NAME = "_test.db"


def test_username_exists():
    username = "Mark"

    # delete database if exists
    if os.path.exists(username):
        os.remove(username + ".db")
    assert func.username_exists(username) is False

    # create database with username
    with open(username + ".db", "w"):
        pass

    assert func.username_exists(username) is True

    # delete database
    os.remove(username + ".db")


def test_create_habit(temporary_database):
    Habit.Instances = {}
    d_name = "Test daily"
    d_description = "Test description daily"
    w_name = "Test weekly"
    w_description = "Test description weekly"

    func.create_habit("Daily", d_name, d_description)
    func.create_habit("Weekly", w_name, w_description)

    # check habit creation
    assert len(Habit.Instances) == 2
    assert isinstance(Habit.Instances[d_name], Daily)
    assert isinstance(Habit.Instances[w_name], Weekly)

    # check habit saving
    with sqlite3.connect(Habit._DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM habit")
        existing_habits = cursor.fetchall()

    assert len(existing_habits) == 2
    assert existing_habits[0]["name"] == d_name
    assert existing_habits[0]["description"] == d_description
    assert existing_habits[1]["name"] == w_name
    assert existing_habits[1]["description"] == w_description


def test_list_habits(predefined_habits):
    habit_list = func.list_habits(Habit.Instances)

    assert [habit for habit in habit_list] == ["Brush", "Duolingo", "Exercise", "Plants", "Clean"]


def test_list_habits_period(predefined_habits):
    habit_list_daily = func.list_habits(Habit.Instances, period="Daily")
    habit_list_weekly = func.list_habits(Habit.Instances, period="Weekly")

    assert [habit for habit in habit_list_daily] == ["Brush", "Duolingo", "Exercise"]
    assert [habit for habit in habit_list_weekly] == ["Plants", "Clean"]


@freeze_time("2015-01-18")
def test_list_active(predefined_habits):
    habit_list_active = func.list_active(Habit.Instances)
    habit_list_inactive = func.list_active(Habit.Instances, active=False)

    assert [habit for habit in habit_list_active] == ["Brush", "Duolingo", "Plants", "Clean"]
    assert [habit for habit in habit_list_inactive] == ["Exercise"]


@freeze_time("2015-01-18")
def test_list_streak(predefined_habits):
    streak_dictionary = func.list_streak(Habit.Instances)

    assert len(streak_dictionary) == 5
    assert [key for key in streak_dictionary] == ["Brush", "Duolingo", "Exercise", "Plants", "Clean"]
    assert [streak for streak in streak_dictionary.values()] == [13, 13, 0, 4, 1]


@freeze_time("2015-01-18")
def test_list_longest_streak(predefined_habits):
    streak_dictionary = func.list_longest_streak(Habit.Instances)

    assert len(streak_dictionary) == 5
    assert [key for key in streak_dictionary] == ["Brush", "Duolingo", "Exercise", "Plants", "Clean"]
    assert [streak for streak in streak_dictionary.values()] == [14, 14, 20, 4, 2]


def test_habit_list_as_string(predefined_habits):
    habit_list = func.list_habits(Habit.Instances)

    assert func.habit_list_as_string(habit_list) == "Brush, Duolingo, Exercise, Plants, Clean"


@freeze_time("2015-01-18")
def test_habit_streak_string(predefined_habits):
    streak_dictionary = func.list_streak(Habit.Instances)
    longest_streak_dictionary = func.list_longest_streak(Habit.Instances)

    streak_string = func.habit_streak_string(streak_dictionary)
    longest_streak_string = func.habit_streak_string(longest_streak_dictionary)

    # "Habit: 'habit' - Streak: 'streak'"
    assert streak_string == ("Habit: Brush - Streak: 13\n" +
                             "Habit: Duolingo - Streak: 13\n" +
                             "Habit: Exercise - Streak: 0\n" +
                             "Habit: Plants - Streak: 4\n" +
                             "Habit: Clean - Streak: 1")

    assert longest_streak_string == ("Habit: Brush - Streak: 14\n" +
                                     "Habit: Duolingo - Streak: 14\n" +
                                     "Habit: Exercise - Streak: 20\n" +
                                     "Habit: Plants - Streak: 4\n" +
                                     "Habit: Clean - Streak: 2")
