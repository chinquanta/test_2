import csv


def read_file(file_name: str) -> list:
    """
    Считывает файл с данными в список строк.
    """
    with open(file_name, 'r', newline='') as csvfile:
        db = csv.reader(csvfile, delimiter=';')
        db = list(db)
        return db


def menu(file_name: str):
    """
    Предоставляет интерфейс для управления
    набором опций по обработке данных.
    """
    features = read_file(file_name)
    print('Что нужно сделать:\n')
    print('Вывести в понятном виде иерархию команд,\n'
          'т.е. департамент и все команды, которые входят в него -', 1, '\n')
    print('Вывести сводный отчёт по департаментам:\n название, численность,'
          '"вилка" зарплат в виде мин – макс, среднюю зарплату -', 2, '\n')
    print('Сохранить сводный отчёт из предыдущего пункта в виде csv-файла.\n'
          'При этом необязательно вызывать сначала команду из п.2 -', 3, '\n')
    print('Закончить - 4')
    while True:
        inp = input()
        if inp == '1':
            print('Выводим структуру:')
            struct_depts(features)
        elif inp == '2':
            print('Получаем сводный отчет:')
            struct_salary(features, inp)
        elif inp == '3':
            print('Записываем сводный отчет в файл')
            struct_salary(features, inp)
        elif inp == '4':
            print('Завершаем работу')
            return
        else:
            print('Выберите: 1, 2, 3 или 4')


def struct_depts(db: list):
    """
    Формирует структуру департаментов и печатает ее
    """
    columns = db[0]
    data = db[1:]
    ix_dep, ix_sub = [columns.index('Департамент'), columns.index('Отдел')]
    struct_set = {(x[ix_dep], x[ix_sub]) for x in data}
    struct_set = sorted(struct_set, key = lambda x: x[0])
    dep = ''
    for x in struct_set:
        if x[0] != dep:
            print(x[0])
            dep = x[0]
        print('    ' + x[1])


def struct_salary(db: list, key: str):
    """
    Формирует таблицу сводного отчета по департаментам.
    Если key = 2, то печатает ее,
    если key = 3, то записывает ее в файл.
    """
    columns = db[0]
    data = db[1:]
    ix_dep, ix_sal = [columns.index('Департамент'), columns.index('Оклад')]
    set_depts = {x[ix_dep] for x in data}
    dict_struct = dict()
    for dept in set_depts:
        flr = filter(lambda x: x[ix_dep] == dept, db)
        dict_struct[dept] = [int(item[ix_sal]) for item in flr]
        dict_struct[dept] = [len(dict_struct[dept]), min(dict_struct[dept]),
                            sum(dict_struct[dept]) / len(dict_struct[dept]),
                            max(dict_struct[dept])]
    if key == '3':
        with open('result.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Департ.', 'числ-ть', 'мин.', 'ср.знач.', 'макс.'])
            for dept in set_depts:
                writer.writerow([dept] + dict_struct[dept])
    if key == '2':
        print('Департ.', 'числ-ть', 'мин.', 'ср.знач.', 'макс.')
        for dept in set_depts:
            print(dept, *dict_struct[dept])


if __name__ == '__main__':
    menu('Corp_Summary.csv')