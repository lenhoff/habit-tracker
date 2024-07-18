from abc import ABC, abstractmethod
import sqlite3
from datetime import datetime, timedelta
from week_tuple_class import Week_tuple


class Habit(ABC):

    Instances = {}

    _DB_NAME = "_test.db"

    @classmethod
    def load(cls):
        with sqlite3.connect(cls._DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM habit")
            existing_habits = cursor.fetchall()

            # initialize all habits
            for habit in existing_habits:
                if habit["period"] == "Daily":
                    Daily(habit["name"], habit["description"])
                elif habit["period"] == "Weekly":
                    Weekly(habit["name"], habit["description"])
                Habit.Instances[habit["name"]].id = habit["id"]
                Habit.Instances[habit["name"]].date_created = habit["date_created"]

            # load tracking data for each habit
            for habit in Habit.Instances.values():
                cursor.execute("SELECT * FROM tracking WHERE habit_id=?", (habit.id, ))
                dates = cursor.fetchall()

                for date in dates:
                    habit.dates_checked.append(datetime.strptime(date["date_checked"], "%Y-%m-%d").date())

    # DONE
    @classmethod
    def change_db(cls, username):
        cls._DB_NAME = str(username) + ".db"

    @abstractmethod
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.date_created = None
        self.dates_checked = []
        self.id = None
        self.period = "None"
        Habit.Instances.update({self.name: self})
        self._initialize_db()
        self._initialize_date_created()

    def _initialize_db(self):
        with sqlite3.connect(self._DB_NAME) as conn:
            cursor = conn.cursor()
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

    def _initialize_date_created(self):
        if self.date_created is None:
            self.date_created = str(datetime.today().date())

    def update_name(self, new_name):
        old_name = self.name
        self.name = str(new_name)

        Habit.Instances.pop(old_name)
        Habit.Instances.update({self.name: self})

    def update_description(self, new_description):
        self.description = str(new_description)

    def delete(self):
        if self.id:
            with sqlite3.connect(Habit._DB_NAME) as conn:
                cursor = conn.cursor()

                cursor.execute("DELETE FROM habit WHERE id=?", (self.id,))
                cursor.execute("DELETE FROM tracking WHERE habit_id=?", (self.id,))

                conn.commit()

        Habit.Instances.pop(self.name)

    def save(self):
        with sqlite3.connect(Habit._DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # save habit meta data
            if self.id:
                cursor.execute("""
                    UPDATE habit SET name=?, description=? WHERE id=?
                    """, (self.name, self.description, self.id))
            else:
                cursor.execute("""
                    INSERT INTO habit (name, description, period, date_created) VALUES (?,?,?,?)
                    """, (self.name, self.description, self.period, self.date_created))
                self.id = cursor.lastrowid

            # save checked dates
            cursor.execute("""
                SELECT * FROM tracking WHERE habit_id = ?
                """, (self.id, ))
            existing_dates = {row["date_checked"] for row in cursor.fetchall()}

            for date in self.dates_checked:
                if str(date) not in existing_dates:
                    cursor.execute("""
                        INSERT INTO tracking (habit_id, date_checked) VALUES (?, ?)
                        """, (self.id, date))

        conn.commit()

    def __str__(self):
        return (f"Habit ID: {self.id}\n" +
                f"Habit name: {self.name}\n" +
                f"Habit description: {self.description}\n" +
                f"Created: {self.date_created}\n" +
                f"Habit periodicity: {self.period}\n" +
                f"Is active: {self.is_active()}\n" +
                f"Current streak: {self.streak()}\n" +
                f"Longest streak: {self.longest_streak()}\n")

    @abstractmethod
    def checkoff_streak(self):
        pass

    @abstractmethod
    def is_active(self):
        pass

    @abstractmethod
    def streak(self):
        pass

    @abstractmethod
    def longest_streak(self):
        pass


class Daily(Habit):

    def __init__(self, name, description):
        super().__init__(name, description)
        self.period = "Daily"

    def is_active(self):
        today = datetime.today().date()

        if len(self.dates_checked) > 0:
            if today in self.dates_checked:
                return True
            else:
                return False
        else:
            return False

    def checkoff_streak(self, date="today"):
        if date == "today":
            new_date = datetime.today().date()
        else:
            new_date = datetime.strptime(date, "%Y-%m-%d").date()

        if new_date not in self.dates_checked:
            self.dates_checked.append(new_date)

    def streak(self):
        current_streak = 0
        today = datetime.today().date()

        while today in self.dates_checked:
            current_streak += 1
            today -= timedelta(days=1)

        return current_streak

    def longest_streak(self):

        max_streak = 0
        self.dates_checked.sort(reverse=True)

        if len(self.dates_checked) > 0:
            streak_count = 1
            max_streak = 1
            for date in range(len(self.dates_checked)-1):
                if (self.dates_checked[date] - self.dates_checked[date+1]).days == 1:
                    streak_count += 1
                    if streak_count > max_streak:
                        max_streak = streak_count
                else:
                    streak_count = 1

        return max_streak


class Weekly(Habit):

    def __init__(self, name, description):
        super().__init__(name, description)
        self.period = "Weekly"

    def is_active(self):
        active = False
        this_week = Week_tuple(datetime.today().isocalendar().year, datetime.today().isocalendar().week)
        weeks_checked = self._convert_week()

        if len(weeks_checked) > 0:
            if this_week in weeks_checked:
                active = True

        return active

    def checkoff_streak(self, date="today"):
        if date == "today":
            new_day = datetime.today().date()
            new_week = Week_tuple(new_day.isocalendar().year, new_day.isocalendar().week)
        else:
            new_day = datetime.strptime(date, "%Y-%m-%d").date()
            new_week = Week_tuple(new_day.isocalendar().year, new_day.isocalendar().week)

        weeks_checked = self._convert_week()

        if new_week not in weeks_checked:
            self.dates_checked.append(new_day)

    def streak(self):
        current_streak = 0
        weeks_checked = self._convert_week()
        this_week = Week_tuple(datetime.today().isocalendar().year, datetime.today().isocalendar().week)

        while this_week in weeks_checked:
            current_streak += 1
            this_week = Weekly._previous_week(this_week)

        return current_streak

    def longest_streak(self):
        max_streak = 0
        weeks_checked = self._convert_week()
        weeks_checked.sort(reverse=True)

        if len(weeks_checked) > 0:
            streak = 1
            max_streak = 1
            for date in range(len(weeks_checked) - 1):
                if Weekly._previous_week(weeks_checked[date]) == weeks_checked[date + 1]:
                    streak += 1
                    if streak > max_streak:
                        max_streak = streak
                else:
                    streak = 1

        return max_streak

    def _convert_week(self):
        iso_list = [date.isocalendar() for date in self.dates_checked]

        return [Week_tuple(iso.year, iso.week) for iso in iso_list]

    @staticmethod
    def _previous_week(date: Week_tuple):
        monday = datetime.fromisocalendar(date.year, date.week, 1)

        previous_monday = (monday - timedelta(weeks=1)).isocalendar()

        return Week_tuple(previous_monday.year, previous_monday.week)

