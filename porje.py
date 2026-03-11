import json
import os
from datetime import datetime, timedelta

FILE_NAME = "podii.json"


def load_events():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_events(events):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=4, ensure_ascii=False)


def generate_id(events):
    if not events:
        return 1
    return max(event["id"] for event in events) + 1


def parse_datetime(date_str, time_str):
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")


def greeting():
    print("Вітаю! Я бот-організатор подій.")


def help_command():
    print("""
Доступні команди:
- додати подію
- показати події
- події на тиждень
- фільтр дата
- фільтр період
- фільтр категорія
- редагувати подію
- видалити подію
- події сьогодні
- події завтра
- найближча
- допомога
- вийти
""")


def check_conflict(events, new_event):
    new_start = parse_datetime(new_event["date"], new_event["start_time"])
    new_end = parse_datetime(new_event["date"], new_event["end_time"])

    for event in events:
        if event["date"] == new_event["date"]:
            start = parse_datetime(event["date"], event["start_time"])
            end = parse_datetime(event["date"], event["end_time"])

            if new_start < end and new_end > start:
                return True
    return False


def add_event(events):
    print("=== Додавання події ===")

    title = input("Назва події: ")
    date = input("Дата (YYYY-MM-DD): ")
    start_time = input("Час початку (HH:MM): ")

    end_time = input("Час завершення (HH:MM) або Enter: ")
    if end_time == "":
        duration = int(input("Тривалість у хвилинах: "))
        start = parse_datetime(date, start_time)
        end = start + timedelta(minutes=duration)
        end_time = end.strftime("%H:%M")

    category = input("Категорія / опис: ")

    new_event = {
        "id": generate_id(events),
        "title": title,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "category": category
    }

    if check_conflict(events, new_event):
        print("⚠ Увага! Подія конфліктує з іншою!")
    else:
        events.append(new_event)
        save_events(events)
        print("Подію додано!")


def show_events(events):
    if not events:
        print("Подій немає.")
        return

    for event in events:
        print(f'{event["id"]}. {event["title"]} | {event["date"]} '
              f'{event["start_time"]}-{event["end_time"]} | {event["category"]}')


def events_week(events):
    today = datetime.now()
    end_week = today + timedelta(days=7)

    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d")

        if today <= event_date <= end_week:
            print(event["title"], event["date"])


def filter_date(events):
    date = input("Введіть дату: ")

    for event in events:
        if event["date"] == date:
            print(event["title"], event["start_time"])


def filter_period(events):
    start = input("Дата початку: ")
    end = input("Дата кінця: ")

    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")

    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d")

        if start <= event_date <= end:
            print(event["title"], event["date"])


def filter_category(events):
    category = input("Введіть категорію: ").lower()

    for event in events:
        if category in event["category"].lower():
            print(event["title"], event["date"])


def events_today(events):
    today = datetime.now().strftime("%Y-%m-%d")

    for event in events:
        if event["date"] == today:
            print(event["title"], event["start_time"])


def events_tomorrow(events):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    for event in events:
        if event["date"] == tomorrow:
            print(event["title"], event["start_time"])


def nearest_event(events):
    now = datetime.now()
    future = []

    for event in events:
        event_time = parse_datetime(event["date"], event["start_time"])

        if event_time > now:
            future.append((event_time, event))

    if future:
        future.sort()
        print("Найближча подія:", future[0][1]["title"])
    else:
        print("Майбутніх подій немає.")


def delete_event(events):
    show_events(events)

    event_id = int(input("ID події для видалення: "))

    events[:] = [e for e in events if e["id"] != event_id]

    save_events(events)

    print("Подію видалено.")


def edit_event(events):
    show_events(events)

    event_id = int(input("ID події для редагування: "))

    for event in events:
        if event["id"] == event_id:

            event["title"] = input("Нова назва: ")
            event["date"] = input("Нова дата: ")
            event["start_time"] = input("Новий час початку: ")
            event["end_time"] = input("Новий час завершення: ")
            event["category"] = input("Нова категорія: ")

            save_events(events)

            print("Подію змінено.")
            return

    print("Подію не знайдено.")


def main():

    events = load_events()

    greeting()

    help_command()

    while True:

        command = input("\nВведіть команду: ").lower()

        if command == "додати подію":
            add_event(events)

        elif command == "показати події":
            show_events(events)

        elif command == "події на тиждень":
            events_week(events)

        elif command == "фільтр дата":
            filter_date(events)

        elif command == "фільтр період":
            filter_period(events)

        elif command == "фільтр категорія":
            filter_category(events)

        elif command == "події сьогодні":
            events_today(events)

        elif command == "події завтра":
            events_tomorrow(events)

        elif command == "найближча":
            nearest_event(events)

        elif command == "редагувати подію":
            edit_event(events)

        elif command == "видалити подію":
            delete_event(events)

        elif command == "допомога":
            help_command()

        elif command == "вийти":
            print("До побачення!")
            break

        else:
            print("Невідома команда")


if __name__ == "__main__":
    main()