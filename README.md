# Habit tracker
A simple app to track habits based on command line interface.
Users can create and delete habits, complete them on a daily or weekly basis and analyze their streaks.

---

## Author
Lennart Hoffmann

---

## Installation
To run the program clone the GitHub repository and run the following code:
```console
pip install -r requirements.txt
python main.py
```

Note: This app was only tested on Windows using Python 3.11.7.

---

## Usage

### User login
* After you start the app, you will be asked to enter a username. If the username does not exist
yet, a new account (with five predefined example habits) will be created for you. If your username
exists, you will be logged into an existing account with that username. Afterwards, you will enter the
main menu.\
\
Note: Usernames must be between 1 and 20 characters long and cannot contain special characters.

### Main menu
* To use the app navigate through the main menu using the arrow keys.

### 1. Manage habits
* This part of the menu covers everything related to habit management. Here you can create
new habits, edit them, and delete habits you don't need anymore.

#### 1.1. Create habit
* Choose this option if you want to create a new habit. You can decide to create a daily or a
weekly habit. Daily habits are intended to be completed on a daily basis, whereas weekly habits
should be checked off once a week. For every habit you create, you must enter a name
and a description.\
\
Note: Names must be unique and between 1 and 50 characters long. Descriptions must be between
1 and 100 characters long.


#### 1.2. Edit habit
* Choose this option if you want to change the name or the description of an existing habit.

#### 1.3. Delete habit
* Choose this option if you want to delete an existing habit. Simply choose an item from the list
and confirm the deletion.

#### 1.4. Inspect habit
* Choose this option to inspect habit details (name, description, date of creation, current and
longest streak).

#### 1.5. Back
* Return to main menu.

### 2. Check-off habits
* In this part of the menu you can complete ("check off") habits.

#### 2.1. Check-off
* Choose this option if you want to check-off a habit that you have completed today. To check-off a habit, 
simply choose an item from the list.

#### 2.2. Manual check-off
* Choose this option if you want to manually insert a date to be checked off (e.g. if you forgot to check-off
a habit in the past). Choose an item from the list and enter the desired date.\
\
Note: Only date of the following format will be accepted: YYYY-MM-DD (Y: year, M: month, D: day)

#### 2.3. Back
* Return to main menu.

### 3. Analyze habits
* In this section of the menu you can get an overview over the activity and streaks of your habits.

#### 3.1. Show active habits
* Choose this option to list all your active habits.

#### 3.2. Show inactive habits
* Choose this option to list all your inactive habits

#### 3.3. Show current streak
* Choose this option to list the streaks of your habits. Choose 'Single' if you want to see the streak
of a single habit or 'All' to look at the streaks of all your habits.

#### 3.4. Show longest streak
* Choose this option to list the longest streaks of your habits. Choose 'Single' if you want to see the longest streak
of a single habit or 'All' to inspect the longest streaks of all your habits.

#### 3.5. Back
* Return to main menu.

### 4. Exit
* Exit the habit tracker program.

---

## Testing
The habit tracker comes with a testing suite to ensure correct behaviour of all its functionality.
To run the test scripts execute:
```console
pytest test_habit_classes.py
pytest test_functions.py
```


