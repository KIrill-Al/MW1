'''Дан каталог книг. Про книгу  известно: уникальный номер, автор, название, год издания.
Реализовать CRUD(создание-чтение-изменение-удаление), показ всех книг на экран и поиск по каждому из полей.
Учитывать, что каждое поле соответствует определенному типу данных.'''

import csv
import fileinput


def main(filename):
    print('Выберите действие:\n',
          '0 - показать все книги\n',
          '1 - поиск книги\n',
          '2 - удаление книги\n',
          '3 - добавление книги\n'
          '4 - выход', sep='')
    i = int(input())
    if i == 0:
        find_book(filename, '0')
        main(filename)
    elif i == 1:
        print('По какому полю выполнить поиск?\n',
              '1 - по ID\n',
              '2 - по автору\n',
              '3 - по названию\n',
              '4 - по году\n',
              'Если не знаете что выбрать, просто введите строку для поиска.', sep='')
        key = input()
        find_book(filename, key)
        main(filename)
    elif i == 2:
        book_id = get_id()
        delete_book(filename, book_id)
        main(filename)
    elif i == 3:
        author = input('Введите имя автора: ')
        title = input('Введите название: ')
        year = get_year()
        add_book(filename, author, title, year)
        main(filename)
    elif i == 4:
        exit()
    else:
        print('Введён неизвестный запрос.')
        main(filename)


def get_id():
    ident = input('Введите ID: ')
    if ident.isdigit():
        return ident
    else:
        print('ID введён некорректно')
        return get_id()


def get_year():
    year = input('Введите год: ')
    if year.isdigit():
        return year
    else:
        print('Год введён некорректно')
        return get_year()


def find_by_id(books, wanted):
    return list(filter(lambda book: int(book['id']) == wanted, books))


def find_by_year(books, wanted):
    return list(filter(lambda book: int(book['year']) == wanted, books))


def find_by_author(books, wanted):
    return list(filter(lambda book: wanted in book['author'].lower(), books))


def find_by_title(books, wanted):
    return list(filter(lambda book: wanted in book['title'].lower(), books))


def print_inquiry(inquiry):  # форматированный вывод запроса
    if inquiry == []:
        print('Ничего не найдено.')
    else:
        id_len = max([len(book['id']) for book in inquiry])
        author_len = max([len(book['author']) for book in inquiry])
        title_len = max([len(book['title']) for book in inquiry])
        year_len = max([len(book['year']) for book in inquiry])
        print('\n{}\t{}\t{}\t{}'.format('ID'.ljust(id_len, ' '),
                                        'Автор'.ljust(author_len, ' '),
                                        'Название'.ljust(title_len, ' '),
                                        'Год'.ljust(year_len, ' ')))
        for book in inquiry:
            print('{}\t{}\t{}\t{}'.format(book['id'].ljust(id_len, ' '),
                                            book['author'].ljust(author_len, ' '),
                                            book['title'].ljust(title_len, ' '),
                                            book['year'].ljust(year_len, ' ')))
        print()


def find_book(filename, key):
    try:
        f = open(filename)
    except FileNotFoundError:
        print('Файл не найден. Исправьте имя или укажите другой файл.')
    else:
        with f:
            reader = csv.DictReader(f, delimiter=';')
            books = [row for row in reader]
        if key == '0':
            print_inquiry(books)
        elif key == '1':
            wanted = int(get_id())
            print_inquiry(find_by_id(books, wanted))
        elif key == '2':
            wanted = input('Введите автора: ').lower()
            print_inquiry(find_by_author(books,wanted))
        elif key == '3':
            wanted = input('Введите название: ').lower()
            print_inquiry(find_by_title(books, wanted))
        elif key == '4':
            wanted = int(get_year())
            print_inquiry(find_by_year(books, wanted))
        elif key.isdigit():
            print('Введено неизвестное значение. Попробуем что-нибудь найти.\n',
                  'Поиск по id...')
            print_inquiry(find_by_id(books, int(key)))
            print('Поиск по году...')
            print_inquiry(find_by_year(books, int(key)))
        else:
            print('Введено неизвестное значение. Попробуем что-нибудь найти.\n',
                  'Поиск по автору...')
            print_inquiry(find_by_author(books, key.lower()))
            print('Поиск по названию...')
            print_inquiry(find_by_title(books, key.lower()))


def delete_book(filename, book_id):
    try:
        f = open(filename)
    except FileNotFoundError:
        print('Файл не найден. Исправьте имя или укажите другой файл.')
    else:
        with fileinput.input(filename, inplace=True) as f:
            for line in f:
                ident = list(line.split(';'))[0]
                if book_id == ident:
                    print('', end='')
                else:
                    print(line, end='')


def add_book(filename, author, title, year):
    fieldnames = ['id', 'author', 'title', 'year']
    try:
        f = open(filename)
    except FileNotFoundError:
        line = [1, author, title, year]
        with open(filename, 'w') as f:
            writer = csv.DictWriter(f, delimiter=';', fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(dict(zip(fieldnames, line)))
    else:
        with f:
            reader = csv.DictReader(f, delimiter=';')
            books = [row for row in reader]
        ident = max(list(int(book['id']) for book in books)) + 1
        line = [ident, author, title, year]
        with open(filename, 'a') as f:
            writer = csv.DictWriter(f, delimiter=';', fieldnames=fieldnames)
            writer.writerow(dict(zip(fieldnames, line)))


source = 'source.txt'
main(source)