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

def parse_input(user_input):
    command, *args = user_input.split()
    command = command.strip().lower()
    return command, *args


def add_contact(args, contacts):
    if len(args) == 2:
        name, phone = args
        contacts[name] = phone
        return f"Contact {name} added."
    else:
        return "Invalid input. Please provide username and phone number."


def change_contact(args, contacts):
    if len(args) == 2:
        name, phone = args
        if name in contacts:
            contacts[name] = phone
            return f"Contact {name} updated."
        else:
            return f"Contact {name} not found."
    else:
        return "Invalid input. Please provide username and new phone number."


def show_phone(args, contacts):
    if len(args) == 1:
        name = args[0]
        if name in contacts:
            return f"Phone number for {name}: {contacts[name]}"
        else:
            return f"Contact {name} not found."
    else:
        return "Invalid input. Please provide the username."


def show_all(contacts):
    if contacts:
        for name, phone in contacts.items():
            print(f"{name}: {phone}")
    else:
        print("No contacts available.")


def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

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
