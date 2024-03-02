# HW-1-task_02
"""
Напишіть консольного бота-помічника, який розпізнаватиме команди, що вводяться з клавіатури,
та буде відповідати відповідно до введеної команди.
По перше, треба систематизувати опис форматів команд для консольного бота-помічника. 
Це допоможе зрозуміти які функції треба зробити для кожної команди:

1. Команда "hello", тут можна обійтись поки без функції та використати звичайний print:
- Введення: "hello"
- Вивід: "How can I help you?"

2. Команда "add [ім'я] [номер телефону]". Для цієї команди зробимо функцію add_contact:
- Введення: "add John 1234567890"
- Вивід: "Contact added."

3. Команда "change [ім'я] [новий номер телефону]". Для цієї команди зробимо функцію change_contact:
- Введення: "change John 0987654321"
- Вивід: "Contact updated." або повідомлення про помилку, якщо ім'я не знайдено

4. Команда "phone [ім'я]". Для цієї команди зробимо функцію show_phone:
- Введення: "phone John"
- Вивід: [номер телефону] або повідомлення про помилку, якщо ім'я не знайдено

5. Команда "all". Для цієї команди зробимо функцію show_all:
- Введення: "all"
- Вивід: усі збережені контакти з номерами телефонів

6. Команда "close" або "exit". Оскільки тут треба перервати виконання програми, 
можна поки обійтись без функції для цих команд:
- Введення: будь-яке з цих слів
- Вивід: "Good bye!" та завершення роботи бота

Будь-яка команда, яка не відповідає вищезазначеним форматам, буде вважатися нами невірною,
і бот буде виводити повідомлення "Invalid command."

"""

# def parse_input(user_input):
#     command, *args = user_input.split()
#     command = command.strip().lower()
#     return command, *args


# def add_contact(args, contacts):
#     if len(args) == 2:
#         name, phone = args
#         contacts[name] = phone
#         return f"Contact {name} added."
#     else:
#         return "Invalid input. Please provide username and phone number."


# def change_contact(args, contacts):
#     if len(args) == 2:
#         name, phone = args
#         if name in contacts:
#             contacts[name] = phone
#             return f"Contact {name} updated."
#         else:
#             return f"Contact {name} not found."
#     else:
#         return "Invalid input. Please provide username and new phone number."


# def show_phone(args, contacts):
#     if len(args) == 1:
#         name = args[0]
#         if name in contacts:
#             return f"Phone number for {name}: {contacts[name]}"
#         else:
#             return f"Contact {name} not found."
#     else:
#         return "Invalid input. Please provide the username."


# def show_all(contacts):
#     if contacts:
#         for name, phone in contacts.items():
#             print(f"{name}: {phone}")
#     else:
#         print("No contacts available.")


# def main():
#     contacts = {}
#     print("Welcome to the assistant bot!")

#     while True:
#         user_input = input("Enter a command: ")
#         command, *args = parse_input(user_input)

#         if command in ["close", "exit"]:
#             print("Good bye!")
#             break
#         elif command == "hello":
#             print("How can I help you?")
#         elif command == "add":
#             print(add_contact(args, contacts))
#         elif command == "change":
#             print(change_contact(args, contacts))
#         elif command == "phone":
#             print(show_phone(args, contacts))
#         elif command == "all":
#             show_all(contacts)
#         else:
#             print("Invalid command.")


# if __name__ == "__main__":
#     main()


# HW-2-task_01
# Додайти обробку помилок (за допомогою декоратора input_error).


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid input. Give me name and phone please."
        except KeyError:
            return "Contact not found."

    return inner


@input_error
def add_contact(args, contacts):
    name, phone = args
    if not name:
        raise ValueError
    contacts[name] = phone
    return f"Contact {name} added."


@input_error
def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return f"Contact {name} updated."
    else:
        raise KeyError


@input_error
def show_phone(args, contacts):
    name = args[0]
    if name in contacts:
        return f"Phone number for {name}: {contacts[name]}"
    else:
        raise KeyError


def show_all(contacts):
    if contacts:
        for name, phone in contacts.items():
            print(f"{name}: {phone}")
    else:
        raise KeyError


def parse_input(user_input):
    command, *args = user_input.split()
    command = command.strip().lower()
    return command, args


def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            show_all(contacts)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()


# HW-2-task_02
# Додати внутрішню логіку асистента (робота з даними).
# У користувача має бути адресна книга, яка містить записи. Кожен запис містить деякий набір полів.
# Класи: Field, Name, Phone, Record, AddressBook.

from collections import UserDict


class Field:
    def __init__(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def set_value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if str(phone) != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        old_phone = self.find_phone(old_phone_number)
        old_phone.set_value(new_phone_number)

    def find_phone(self, phone_number):
        for phone in self.phones:
            if str(phone) == phone_number:
                return phone
        raise ValueError(f"Phone number {phone_number} not found.")

    def __str__(self):
        return f"Contact name: {self.name.get_value()}, phones: {'; '.join(str(p.get_value()) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.get_value()] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        self.data.pop(name, None)


book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

for name, record in book.data.items():
    print(record)

john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print(john)

found_phone = john.find_phone("5555555555")
print(f"{john.name.get_value()}: {found_phone.get_value()}")

book.delete("Jane")
