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