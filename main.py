from interface import main_menu, user_login
from hclasses import Habit


# start
# ask for username and set database
user_login()

# load habit from user database
Habit.load()

# run main interface
main_menu()
