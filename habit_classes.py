from abc import ABC, abstractmethod
import sqlite3
from datetime import datetime, timedelta
from week_tuple import Week_tuple


class Habit(ABC):
    """
    Abstract base class to implement different habit classes. Covers the basic functionality (i.e., saving, loading and
    deleting) of instances.

    Class attributes:
        Instances (dict): Dictionary, which contains all instances of all child classes. Keys: Habit.name, Values: Habit
        _DB_NAME (str): Database to which class connects (for loading, saving, etc.)

    Class methods:
        load()
        change_db()

    Instance methods:
        _initialize_db()
        _initialize_date_created()
        update_name()
        update_description()
        delete()
        save()

    Abstract methods:
        __init__()
        checkoff_streak()
        is_active()
        streak()
        longest_streak()
    """
    Instances = {}

    _DB_NAME = "_test.db"

    @classmethod
    def load(cls) -> None:
        """
        Class method to load all previously saved Habit instances.

        Connects to Habit._DB_NAME and initializes instances using 'period', 'name', 'description' values from 'habit'
        table. Then, restores id and date_created.
        Lastly, loads tracking data based on instance id from 'tracking' table.
        """
        # connect to user database
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
                Habit.Instances[habit["name"]]._id = habit["id"]
                Habit.Instances[habit["name"]]._date_created = habit["date_created"]

            # load tracking data for each habit
            for habit in Habit.Instances.values():
                cursor.execute("SELECT * FROM tracking WHERE habit_id=?", (habit._id,))
                dates = cursor.fetchall()

                for date in dates:
                    habit._dates_checked.append(datetime.strptime(date["date_checked"], "%Y-%m-%d").date())

    @classmethod
    def change_db(cls, username: str):
        """
        Class method to change user database (Habit._DB_NAME).

        Args:
            username (str): Enter a username / database name

        """
        if not type(username) is str:
            raise ValueError("username must be of type: str")

        cls._DB_NAME = username + ".db"

    @abstractmethod
    def __init__(self, name: str, description: str):
        """
        Abstract method to ensure implementation of __init__ in child classes.
        Child classes inherit this constructor method.

        Args:
            name (str): Enter a habit name.
            description (str): Enter a habit description.
        """
        if not type(name) is str or not type(description) is str:
            raise ValueError("name and description must be of type: str")

        self._name = name
        self._description = description
        self._date_created = None
        self._dates_checked = []
        self._id = None
        self._period = "None"
        Habit.Instances.update({self._name: self})
        self._initialize_db()
        self._initialize_date_created()

    def _initialize_db(self) -> None:
        """
        Connects to 'Habit._DB_NAME' and creates 'habit' and 'tracking' table if they do not exist already.
        """
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
        """
        Changes 'Habit.date_created' to current date.
        """
        if self._date_created is None:
            self._date_created = str(datetime.today().date())

    def update_name(self, new_name: str):
        """
        Changes 'Habit.name' to specified string and updates key in 'Habit.Instances'.

        Args:
            new_name (str): The new name to be entered.
        """
        if not type(new_name) is str:
            raise ValueError("new_name must be of type: str")

        # rename habit
        old_name = self._name
        self._name = new_name

        # update key in Habit.Instances
        Habit.Instances.pop(old_name)
        Habit.Instances.update({self._name: self})

    def update_description(self, new_description: str):
        """
        Changes to 'Habit.description' of instance to specified string.

        Args:
            new_description (str): New description to be entered.
        """
        if not type(new_description) is str:
            raise ValueError("new_description must be of type: str")

        self._description = new_description

    def delete(self) -> None:
        """
        Connects to 'Habit._DB_NAME' and removes the metadata and tracked dates of a Habit instance from tables
        'habits' and 'tracking' (based on 'Habit.id').
        Then, instance is removed 'Habit.Instances'.
        """
        # remove habit from database (by id)
        if self._id:
            with sqlite3.connect(Habit._DB_NAME) as conn:
                cursor = conn.cursor()

                cursor.execute("DELETE FROM habit WHERE id=?", (self._id,))
                cursor.execute("DELETE FROM tracking WHERE habit_id=?", (self._id,))

                conn.commit()

        # remove habit from Habit.Instances
        Habit.Instances.pop(self._name)

    def save(self) -> None:
        """
        Method to save instance data to user database.

        Connects to 'Habit._DB_NAME' and saves metadata and tracked dates of a Habit instance.
        If the Habit ('Habit.id') exists already, method will update name and description in 'habit' table.
        Otherwise, a new entry will be created.

        Dates associated with the Habit instance will be saved in 'tracking' table.
        """
        # if habit exists: update habit database (name, description), else: insert into habit database and add id
        with sqlite3.connect(Habit._DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # save habit meta data
            if self._id:
                cursor.execute("""
                    UPDATE habit SET name=?, description=? WHERE id=?
                    """, (self._name, self._description, self._id))
            else:
                cursor.execute("""
                    INSERT INTO habit (name, description, period, date_created) VALUES (?,?,?,?)
                    """, (self._name, self._description, self._period, self._date_created))
                self._id = cursor.lastrowid

            # save tracked dates if they do not exist already
            cursor.execute("""
                SELECT * FROM tracking WHERE habit_id = ?
                """, (self._id,))
            existing_dates = {row["date_checked"] for row in cursor.fetchall()}

            for date in self._dates_checked:
                if str(date) not in existing_dates:
                    cursor.execute("""
                        INSERT INTO tracking (habit_id, date_checked) VALUES (?, ?)
                        """, (self._id, date))

        conn.commit()

    def __str__(self):
        return (f"Habit ID: {self._id}\n" +
                f"Habit name: {self._name}\n" +
                f"Habit description: {self._description}\n" +
                f"Created: {self._date_created}\n" +
                f"Habit periodicity: {self._period}\n" +
                f"Is active: {self.is_active()}\n" +
                f"Current streak: {self.streak()}\n" +
                f"Longest streak: {self.longest_streak()}\n")

    @abstractmethod
    def checkoff_streak(self):
        """
        Abstract method to ensure implementation of 'checkoff_streak()' in child classes.
        """
        pass

    @abstractmethod
    def is_active(self):
        """
        Abstract method to ensure implementation of 'is_active()' in child classes.
        """
        pass

    @abstractmethod
    def streak(self):
        """
        Abstract method to ensure implementation of 'streak()' in child classes.
        """
        pass

    @abstractmethod
    def longest_streak(self):
        """
        Abstract method to ensure implementation of 'longest_streak()' in child classes.
        """
        pass


class Daily(Habit):
    """
    Class to create instances of daily habits.

    Inherits from Habit class.

    Instance attributes:
        name (str): Habit name
        description (str): Habit description
        date_created (str): Date of creation (format: YYYY-MM-DD)
        dates_checked (list): List containing all tracked dates (based on 'datetime' objects)
        id (int): Unique identifier for database interaction
        period (str) = "Daily": Shows periodicity of instance

    Instance methods:
        __init__()                      [partly inherited from Habit class]
        _initialize_db()                [inherited from Habit class]
        _initialize_date_created()      [inherited from Habit class]
        update_name()                   [inherited from Habit class]
        update_description()            [inherited from Habit class]
        delete()                        [inherited from Habit class]
        save()                          [inherited from Habit class]
        checkoff_streak()
        is_active()
        streak()
        longest_streak()
    """
    def __init__(self, name: str, description: str):
        """
        Creates instance of class Daily.

        Constructor inherited from Habit class. Overwrites 'self.period' to "Daily".

        Args:
            name (str): Enter a habit name.
            description (str): Enter a habit description.
        """
        super().__init__(name, description)
        self._period = "Daily"

    def is_active(self) -> bool:
        """
        Method to check completion/activity status of Daily instance. Is the current date in 'self.dates_checked'?

        Returns:
             bool
        """
        today = datetime.today().date()

        if len(self._dates_checked) > 0:
            if today in self._dates_checked:
                return True
            else:
                return False
        else:
            return False

    def checkoff_streak(self, date: str = "today"):
        """
        Method to mark habit as completed/to check-off habit.

        Appends the specified date to 'self.dates_checked' (default: current date) if it does not already exist.

        Args:
            date (str): Date to enter (in format: YYYY-MM-DD)
        """
        # add current or specified date to _dates_checked if not already existing
        if date == "today":
            new_date = datetime.today().date()
        else:
            new_date = datetime.strptime(date, "%Y-%m-%d").date()

        if new_date not in self._dates_checked:
            self._dates_checked.append(new_date)

    def streak(self) -> int:
        """
        Method to calculate length of current streak of instance.

        Returns:
            int
        """
        current_streak = 0
        today = datetime.today().date()

        while today in self._dates_checked:
            current_streak += 1
            today -= timedelta(days=1)

        return current_streak

    def longest_streak(self) -> int:
        """
        Method to calculate length of longest streak of instance.

        Returns:
            int
        """
        max_streak = 0
        # sort values
        self._dates_checked.sort(reverse=True)

        if len(self._dates_checked) > 0:
            streak_count = 1
            max_streak = 1
            for date in range(len(self._dates_checked) - 1):
                if (self._dates_checked[date] - self._dates_checked[date + 1]).days == 1:
                    streak_count += 1
                    if streak_count > max_streak:
                        max_streak = streak_count
                else:
                    streak_count = 1

        return max_streak


class Weekly(Habit):
    """
    Class to create instances of weekly habits.

    Inherits from Habit class.

    Instance attributes:
        name (str): Habit name
        description (str): Habit description
        date_created (str): Date of creation (format: YYYY-MM-DD)
        dates_checked (list): List containing all tracked dates (based on 'datetime' objects)
        id (int): Unique identifier for database interaction
        period (str) = "Weekly": Shows periodicity of instance

    Instance methods:
        __init__()                      [partly inherited from Habit class]
        _initialize_db()                [inherited from Habit class]
        _initialize_date_created()      [inherited from Habit class]
        update_name()                   [inherited from Habit class]
        update_description()            [inherited from Habit class]
        delete()                        [inherited from Habit class]
        save()                          [inherited from Habit class]
        checkoff_streak()
        is_active()
        streak()
        longest_streak()
        _convert_week()
        _previous_week()
    """
    def __init__(self, name: str, description: str):
        """
        Creates instance of class Daily.

        Constructor inherited from Habit class. Overwrites 'self.period' to "Weekly".

        Args:
            name (str): Enter a habit name.
            description (str): Enter a habit description.
        """
        super().__init__(name, description)
        self._period = "Weekly"

    def is_active(self) -> bool:
        """
        Method to check completion/activity status of Weekly instance. Is the week of the current date in
        'self.dates_checked'?

        Returns:
             bool
        """
        active = False
        # convert today and dates_checked to Week_tuple
        this_week = Week_tuple(datetime.today().isocalendar().year, datetime.today().isocalendar().week)
        weeks_checked = self._convert_week()

        if len(weeks_checked) > 0:
            if this_week in weeks_checked:
                active = True

        return active

    def checkoff_streak(self, date: str = "today"):
        """
        Method to mark habit as completed/to check-off habit.

        Appends the specified date to 'self.dates_checked' (default: current date) if it does not already contain a date
        from the same week.

        Args:
            date (str): Date to enter (in format: YYYY-MM-DD)
        """
        if date == "today":
            new_day = datetime.today().date()
            new_week = Week_tuple(new_day.isocalendar().year, new_day.isocalendar().week)
        else:
            new_day = datetime.strptime(date, "%Y-%m-%d").date()
            new_week = Week_tuple(new_day.isocalendar().year, new_day.isocalendar().week)

        weeks_checked = self._convert_week()

        if new_week not in weeks_checked:
            self._dates_checked.append(new_day)

    def streak(self) -> int:
        """
        Method to calculate length of current streak of instance.

        Returns:
            int
        """
        current_streak = 0
        # convert current week and dates_checked to Week_tuple
        weeks_checked = self._convert_week()
        this_week = Week_tuple(datetime.today().isocalendar().year, datetime.today().isocalendar().week)

        while this_week in weeks_checked:
            current_streak += 1
            this_week = Weekly._previous_week(this_week)

        return current_streak

    def longest_streak(self) -> int:
        """
        Method to calculate length of longest streak of instance.

        Returns:
            int
        """
        max_streak = 0
        # convert dates to Week_tuple and sort
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

    def _convert_week(self) -> list:
        """
        Method to convert all 'datetime' objects in 'self.dates_checked' into 'Week_tuple' objects.

        Returns:
            list of 'Week_tuple' objects
        """
        iso_list = [date.isocalendar() for date in self._dates_checked]

        return [Week_tuple(iso.year, iso.week) for iso in iso_list]

    @staticmethod
    def _previous_week(date: Week_tuple) -> Week_tuple:
        """
        Method to create a 'Week_tuple' objects of the previous week of input.

        Args:
            date (Week_tuple): Week from which to previous week will be calculated.

        Returns:
            Week_tuple
        """
        # compute previous week based on fixed week day (here: monday) - difference exactly 1 week
        monday = datetime.fromisocalendar(date.year, date.week, 1)
        previous_monday = (monday - timedelta(weeks=1)).isocalendar()

        return Week_tuple(previous_monday.year, previous_monday.week)
