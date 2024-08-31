date_str = input("Введите дату (в формате ГГГГ-ММ-ДД): ")
date = datetime.strptime(date_str[:10], '%Y-%m-%d')