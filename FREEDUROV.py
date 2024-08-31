from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import json

class Note:
    def __init__(self, description: str, note_time: datetime):
        self._description = description
        self._note_time = note_time

    @property
    def description(self) -> str:
        return self._description

    @property
    def note_time(self) -> datetime:
        return self._note_time

    def to_dict(self):
        return {
            "description": self._description,
            "note_time": self._note_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    @staticmethod
    def from_dict(data: dict):
        note_time = datetime.strptime(data["note_time"], '%Y-%m-%d %H:%M:%S')
        return Note(description=data["description"], note_time=note_time)


class Scheduler:
    def __init__(self):
        self._notes = []

    def add_note(self, note: Note):
        self._notes.append(note)

    def get_notes(self):
        return self._notes

    def save_to_file(self, filename: str):
        with open(filename, 'w') as f:
            notes_dict = [note.to_dict() for note in self._notes]
            json.dump(notes_dict, f, indent=4)

    def load_from_file(self, filename: str):
        with open(filename, 'r') as f:
            notes_dict = json.load(f)
            self._notes = [Note.from_dict(note) for note in notes_dict]

    def sort_notes(self):
        self._notes.sort(key=lambda note: note.note_time)

    def find_notes_by_date(self, date: datetime):
        return [note for note in self._notes if note.note_time.date() == date.date()]

    def find_notes_by_week(self, date: datetime):
        start_of_week = date - timedelta(days=date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return [note for note in self._notes if start_of_week <= note.note_time.date() <= end_of_week]


class INoteView(ABC):
    @abstractmethod
    def show_notes(self, notes: list):
        pass

    @abstractmethod
    def show_message(self, message: str):
        pass


class ConsoleNoteView(INoteView):
    def show_notes(self, notes: list):
        if not notes:
            print("Нет записей.")
        for note in notes:
            print(f"{note.note_time.strftime('%Y-%m-%d %H:%M:%S')} - {note.description}")

    def show_message(self, message: str):
        print(message)


class SchedulerPresenter:
    def __init__(self, model: Scheduler, view: INoteView):
        self._model = model
        self._view = view

    def add_note(self, description: str, note_time: datetime):
        note = Note(description=description, note_time=note_time)
        self._model.add_note(note)
        self._view.show_message("Запись добавлена.")

    def display_notes(self):
        notes = self._model.get_notes()
        self._view.show_notes(notes)

    def save_notes(self, filename: str):
        self._model.save_to_file(filename)
        self._view.show_message(f"Записи сохранены в файл {filename}.")

    def load_notes(self, filename: str):
        self._model.load_from_file(filename)
        self._view.show_message(f"Записи загружены из файла {filename}.")

    def sort_and_display_notes(self):
        self._model.sort_notes()
        self.display_notes()

    def find_notes_by_date(self, date: datetime):
        notes = self._model.find_notes_by_date(date)
        self._view.show_notes(notes)

    def find_notes_by_week(self, date: datetime):
        notes = self._model.find_notes_by_week(date)
        self._view.show_notes(notes)


def main():
    scheduler = Scheduler()
    view = ConsoleNoteView()
    presenter = SchedulerPresenter(model=scheduler, view=view)

    while True:
        print("\nДоступные команды:")
        print("1. Добавить запись")
        print("2. Показать все записи")
        print("3. Сохранить записи в файл")
        print("4. Загрузить записи из файла")
        print("5. Сортировать и показать записи")
        print("6. Найти записи по дате")
        print("7. Найти записи за неделю")
        print("8. Выйти")

        command = input("Введите команду (1-8): ")
        if command == "1":
            description = input("Введите описание: ")
            date_str = input("Введите дату и время (в формате ГГГГ-ММ-ДД ЧЧ:ММ): ")
            note_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
            presenter.add_note(description, note_time)

        elif command == "2":
            presenter.display_notes()

        elif command == "3":
            filename = input("Введите имя файла для сохранения: ")
            presenter.save_notes(filename)

        elif command == "4":
            filename = input("Введите имя файла для загрузки: ")
            presenter.load_notes(filename)

        elif command == "5":
            presenter.sort_and_display_notes()

        elif command == "6":
            date_str = input("Введите дату (в формате ГГГГ-ММ-ДД): ")
            date = datetime.strptime(date_str, '%Y-%m-%d')
            presenter.find_notes_by_date(date)

        elif command == "7":
            date_str = input("Введите дату (в формате ГГГГ-ММ-ДД): ")
            date = datetime.strptime(date_str, '%Y-%m-%d')
            presenter.find_notes_by_week(date)

        elif command == "8":
            print("Выход из программы.")
            break

        else:
            print("Неверная команда. Попробуйте снова.")

if __name__ == "__main__":
    main()