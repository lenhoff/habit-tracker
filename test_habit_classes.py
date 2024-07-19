import pytest
from datetime import datetime
from habit_classes import Habit, Daily, Weekly
from week_tuple import Week_tuple
from freezegun import freeze_time
import sqlite3


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
    conn.close()

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


class TestHabit:

    def test_change_database(self, predefined_habits):
        Habit.change_db("abc")
        assert Habit._DB_NAME == "abc.db"

    def test_habit_creation(self):
        assert len(Habit.Instances) == 0
        Daily("Test", "Description")

        assert len(Habit.Instances) == 1
        assert "Test" in Habit.Instances
        assert Habit.Instances["Test"]._name == "Test"
        assert Habit.Instances["Test"]._description == "Description"
        assert Habit.Instances["Test"]._id is None
        assert Habit.Instances["Test"]._dates_checked == []

    def test_initialize_date_created(self, predefined_habits):
        Habit.Instances["Brush"]._initialize_date_created()
        assert Habit.Instances["Brush"]._date_created == str(datetime.today().date())

    def test_update_name(self, predefined_habits):
        habit = Habit.Instances["Brush"]

        habit.update_name("Test")
        assert habit._name == "Test"
        assert "Test" in Habit.Instances

    def test_update_description(self, predefined_habits):
        Habit.Instances["Brush"].update_description("Description")
        assert Habit.Instances["Brush"]._description == "Description"


class TestDaily:

    def test_checkoff_streak(self, predefined_habits):
        Habit.Instances["Brush"].checkoff_streak()
        assert datetime.today().date() in Habit.Instances["Brush"]._dates_checked

    def test_checkoff_streak_custom(self, predefined_habits):
        Habit.Instances["Brush"].checkoff_streak(date="1999-12-12")
        assert datetime(1999, 12, 12).date() in Habit.Instances["Brush"]._dates_checked

    def test_checkoff_streak_repeated(self, predefined_habits):
        Habit.Instances["Brush"].checkoff_streak()
        Habit.Instances["Brush"].checkoff_streak()
        assert Habit.Instances["Brush"]._dates_checked.count(datetime.today().date()) == 1

        Habit.Instances["Brush"].checkoff_streak(date="1999-12-12")
        Habit.Instances["Brush"].checkoff_streak(date="1999-12-12")
        assert Habit.Instances["Brush"]._dates_checked.count(datetime(1999, 12, 12).date()) == 1

    def test_is_active(self, predefined_habits):
        assert Habit.Instances["Brush"].is_active() is False
        Habit.Instances["Brush"].checkoff_streak()
        assert Habit.Instances["Brush"].is_active() is True

    @freeze_time("2015-01-18")
    def test_streak(self, predefined_habits):
        assert Habit.Instances["Brush"].streak() == 13
        assert Habit.Instances["Duolingo"].streak() == 13
        assert Habit.Instances["Exercise"].streak() == 0

    @freeze_time("2015-01-18")
    def test_longest_streak(self, predefined_habits):
        assert Habit.Instances["Brush"].longest_streak() == 14
        assert Habit.Instances["Duolingo"].longest_streak() == 14
        assert Habit.Instances["Exercise"].longest_streak() == 20


class TestWeekly:

    def test_previous_week(self, predefined_habits):
        example_week = Week_tuple(2024, 2)
        assert Habit.Instances["Plants"]._previous_week(example_week) == Week_tuple(2024, 1)

        # test for changes between years with 52 weeks
        example_week = Week_tuple(2024, 1)
        assert Habit.Instances["Plants"]._previous_week(example_week) == Week_tuple(2023, 52)

        # test for changes between years with 53 weeks
        example_week = Week_tuple(2021, 1)
        assert Habit.Instances["Plants"]._previous_week(example_week) == Week_tuple(2020, 53)

    def test_convert_week(self, predefined_habits):
        Habit.Instances["Plants"]._dates_checked = []
        # check-off January 4th of multiple years (is always in the first week of the year)
        Habit.Instances["Plants"].checkoff_streak("1999-01-04")
        Habit.Instances["Plants"].checkoff_streak("2000-01-04")
        Habit.Instances["Plants"].checkoff_streak("2001-01-04")

        expected_list = [Week_tuple(1999, 1), Week_tuple(2000, 1), Week_tuple(2001, 1)]

        assert Habit.Instances["Plants"]._convert_week() == expected_list

    def test_checkoff_streak(self, predefined_habits):
        Habit.Instances["Plants"].checkoff_streak()
        assert datetime.today().date() in Habit.Instances["Plants"]._dates_checked

    def test_checkoff_week_custom(self, predefined_habits):
        Habit.Instances["Plants"].checkoff_streak("1999-12-12")
        assert datetime(1999, 12, 12).date() in Habit.Instances["Plants"]._dates_checked

    def test_checkoff_week_repeated(self, predefined_habits):
        Habit.Instances["Plants"].checkoff_streak("1999-12-12")
        Habit.Instances["Plants"].checkoff_streak("1999-12-12")
        assert Habit.Instances["Plants"]._dates_checked.count(datetime(1999, 12, 12).date()) == 1

        Habit.Instances["Plants"].checkoff_streak()
        Habit.Instances["Plants"].checkoff_streak()
        assert Habit.Instances["Plants"]._dates_checked.count(datetime.today().date()) == 1

    def test_is_active(self, predefined_habits):
        assert Habit.Instances["Plants"].is_active() is False
        Habit.Instances["Plants"].checkoff_streak()
        assert Habit.Instances["Plants"].is_active() is True

    @freeze_time("2015-01-18")
    def test_streak(self, predefined_habits):
        assert Habit.Instances["Plants"].streak() == 4
        assert Habit.Instances["Clean"].streak() == 1

    @freeze_time("2015-01-18")
    def test_longest_streak(self, predefined_habits):
        assert Habit.Instances["Plants"].longest_streak() == 4
        assert Habit.Instances["Clean"].longest_streak() == 2


class TestDatabase:

    def test_save_and_load_habit(self, temporary_database, predefined_habits):
        # create habit and save to database
        Habit.Instances["Brush"].save()

        # delete habit by clearing class dictionary
        Habit.Instances = {}
        assert len(Habit.Instances) == 0

        # load habit from database
        Habit.load()
        assert len(Habit.Instances) == 1
        assert Habit.Instances["Brush"]._name == "Brush"
        assert Habit.Instances["Brush"]._description == "Brush your teeth at least once a day."
        assert Habit.Instances["Brush"]._date_created == str(datetime.today().date())
        assert Habit.Instances["Brush"]._period == "Daily"
        assert Habit.Instances["Brush"]._id == 1
        assert len(Habit.Instances["Brush"]._dates_checked) == 27
        assert Habit.Instances["Brush"].longest_streak() == 14
        assert Habit.Instances["Brush"].streak() == 0
        assert Habit.Instances["Brush"].is_active() is False

    def test_save_and_load_multiple(self, temporary_database, predefined_habits):
        for habit in Habit.Instances.values():
            habit.save()

        # delete habit by clearing class dictionary
        Habit.Instances = {}
        assert len(Habit.Instances) == 0

        # load habits from database
        Habit.load()
        assert len(Habit.Instances) == 5
        assert Habit.Instances["Brush"]._id == 1
        assert Habit.Instances["Clean"]._id == 5
        assert Habit.Instances["Brush"].streak() == 0
        assert Habit.Instances["Brush"].longest_streak() == 14
        assert Habit.Instances["Clean"].streak() == 0
        assert Habit.Instances["Clean"].longest_streak() == 2

    def test_update_database(self, temporary_database, predefined_habits):
        # create habit and save
        Habit.Instances["Brush"].save()

        # delete habit by clearing class dictionary
        Habit.Instances = {}
        assert len(Habit.Instances) == 0

        # update name, description, check-off date and save
        Habit.load()
        Habit.Instances["Brush"].update_name("new_name")
        Habit.Instances["new_name"].update_description("new description")
        Habit.Instances["new_name"].checkoff_streak()
        Habit.Instances["new_name"].save()
        # keep habit id
        old_id = Habit.Instances["new_name"]._id

        # delete habit by clearing class dictionary
        Habit.Instances = {}
        assert len(Habit.Instances) == 0

        # load habit with updated attributes from database
        Habit.load()
        assert Habit.Instances["new_name"]._id == old_id
        assert Habit.Instances["new_name"]._name == "new_name"
        assert Habit.Instances["new_name"]._description == "new description"
        assert Habit.Instances["new_name"].streak() == 1
        assert Habit.Instances["new_name"].is_active() is True

    def test_delete(self, temporary_database, predefined_habits):
        assert len(Habit.Instances) == 5
        for habit in Habit.Instances.values():
            habit.save()

        habit_names = [name for name in Habit.Instances.keys()]

        for name in habit_names:
            Habit.Instances[name].delete()

        assert len(Habit.Instances) == 0
