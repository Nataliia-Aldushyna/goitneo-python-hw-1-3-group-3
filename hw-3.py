# HW-3-final code

from collections import UserDict, defaultdict
from datetime import datetime, timedelta


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."

    return inner


class Birthday:
    def __init__(self, value):
        try:
            self._value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY.")

    def get_value(self):
        return self._value

    def __str__(self):
        return self._value.strftime("%d.%m.%Y")


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
            raise ValueError("Invalid phone number format - must be 10 digits long.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if str(phone) != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        old_phone = self.find_phone(old_phone_number)
        old_phone.set_value(new_phone_number)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def find_phone(self, phone_number):
        for phone in self.phones:
            if str(phone) == phone_number:
                return phone
        raise ValueError(f"Phone number {phone_number} not found.")

    def __str__(self):
        phones_str = "; ".join(str(p.get_value()) for p in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return (
            f"Contact name: {self.name.get_value()}, phones: {phones_str}{birthday_str}"
        )


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.get_value()] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        self.data.pop(name, None)

    def get_birthdays_per_week(self):
        birthdays_per_week = defaultdict(list)
        today = datetime.today().date()

        for record in self.data.values():
            name = record.name.get_value()
            birthday = record.birthday.get_value() if record.birthday else None

            if birthday:
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if 0 <= delta_days < 7:
                    day_of_week = (today + timedelta(days=delta_days)).weekday()
                    if day_of_week >= 5:
                        day_of_week = 0

                    birthdays_per_week[day_of_week].append(name)

        for day in range(5):
            names = birthdays_per_week[day]
            if names:
                day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][day]
                print(f"{day_name}: {', '.join(names)}")


@input_error
def add_contact(args, address_book):
    try:
        if len(args) < 2:
            raise ValueError("Invalid input. Give me name and phone please.")

        name, phone = args

        if not name:
            raise ValueError("Name cannot be empty.")

        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Invalid phone number format - must be 10 digits long.")

        record = Record(name)
        record.add_phone(phone)
        address_book.add_record(record)
        return f"Contact {name} added."
    except ValueError as e:
        return str(e)


@input_error
def change_contact(args, address_book):
    if len(args) == 2:
        name, phone = args
        record = address_book.find(name)
        if record:
            record.edit_phone(record.phones[0].get_value(), phone)
            return f"Contact {name} updated."
        else:
            raise KeyError("Contact not found.")
    else:
        raise ValueError("Invalid input. Give me name and phone please.")


@input_error
def show_phone(args, address_book):
    if args:
        name = args[0]
        record = address_book.find(name)
        if record:
            return f"Phone number for {name}: {record.phones[0].get_value()}"
        else:
            raise KeyError("Contact not found.")
    else:
        raise ValueError("Invalid input. Give me name and phone please.")


@input_error
def show_all(args, address_book):
    address_book.get_birthdays_per_week()
    if address_book.data:
        for record in address_book.data.values():
            print(record)
    else:
        raise KeyError


@input_error
def add_birthday(args, address_book):
    if len(args) == 2:
        name, birthday = args
        record = address_book.find(name)
        if record:
            record.add_birthday(birthday)
            return f"Birthday added for {name}."
        else:
            raise KeyError("Contact not found.")
    else:
        raise ValueError("Invalid input. Give me name and birthday please.")


@input_error
def show_birthday(args, address_book):
    if args:
        name = args[0]
        record = address_book.find(name)
        if record and record.birthday:
            return f"Birthday for {name}: {record.birthday}"
        else:
            raise KeyError("Contact not found or no birthday available.")
    else:
        raise ValueError("Invalid input. Give me name please.")


def birthdays(args, address_book):
    address_book.get_birthdays_per_week()


def parse_input(user_input):
    command, *args = user_input.split()
    command = command.strip().lower()
    return command, args


def main():
    address_book = AddressBook()
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
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "phone":
            print(show_phone(args, address_book))
        elif command == "all":
            show_all(args, address_book)
        elif command == "add-birthday":
            print(add_birthday(args, address_book))
        elif command == "show-birthday":
            print(show_birthday(args, address_book))
        elif command == "birthdays":
            birthdays(args, address_book)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
