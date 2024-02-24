"""
Завдання написати функцію get_birthdays_per_week, яка отримує на вхід список users
і виводить у консоль (за допомогою print) список користувачів, 
яких потрібно привітати по днях на наступному тижні.
У вас є список словників users, кожен словник у ньому обов'язково має ключі name та birthday. 
Така структура представляє модель списку користувачів з їх іменами та днями народження. 
Де name — це рядок з ім'ям користувача, а birthday — це datetime об'єкт, 
в якому записаний день народження.
"""

from collections import defaultdict
from datetime import datetime, timedelta


def get_birthdays_per_week(users):
    birthdays_per_week = defaultdict(list)

    today = datetime.today().date()  # поточна дата

    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()  # конвертуємо до типу date
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        delta_days = (birthday_this_year - today).days  # порівняння з поточною датою

        if 0 <= delta_days < 7:
            day_of_week = (today + timedelta(days=delta_days)).weekday()
            if (
                day_of_week >= 5
            ):
                day_of_week = 0  # ДН на вихідних переносяться на понеділок

            birthdays_per_week[day_of_week].append(name)

    for day in range(5):  # понеділок - п'ятниця
        names = birthdays_per_week[day]
        if names:
            day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][day]
            print(f"{day_name}: {', '.join(names)}")


users = [
    {"name": "Bill Gates", "birthday": datetime(1955, 10, 28)},
    {"name": "Kim Kardashian", "birthday": datetime(1980, 10, 21)},
    {"name": "Jill Valentine", "birthday": datetime(1990, 5, 15)},
    {"name": "Jan Koum", "birthday": datetime(1980, 2, 24)},
    {"name": "Alex Test", "birthday": datetime(1980, 2, 23)},
    {"name": "Saturday Test", "birthday": datetime(1980, 2, 24)},
    {"name": "Sunday Test", "birthday": datetime(1980, 2, 25)},
    {"name": "Alex Monday", "birthday": datetime(1980, 2, 26)},
    {"name": "Alex Tuesday", "birthday": datetime(1980, 2, 27)},
    {"name": "Alex Wednesday", "birthday": datetime(1980, 2, 28)},
    {"name": "Alex Thursday", "birthday": datetime(1980, 2, 29)},
    {"name": "Alex Friday", "birthday": datetime(1980, 3, 1)},
    {"name": "Alex Saturday", "birthday": datetime(1980, 3, 2)},  # Saturday next week
]

get_birthdays_per_week(users)
