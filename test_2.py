import csv


def read_file(file_name):
    '''
    Считывает файл с данными
    '''
    with open(file_name, 'r', newline='') as csvfile:
        df = csv.reader(csvfile, delimiter=';')
        db = list(df)
        features_ix = {feature: db[0].index(feature) for feature in db[0]}
        features = {feature: [row[ix] for row in db[1:]] for feature, ix in features_ix.items()}
        features['Оклад'] = list(map(int, features['Оклад']))
    return features


def menu(file_name):
    '''
    Предоставляет интерфейс для управления
    набором опций по обработке данных.
    '''
    features = read_file(file_name)
    print('Что нужно сделать:\n')
    print('Вывести в понятном виде иерархию команд,\n'
          'т.е. департамент и все команды, которые входят в него -', 1, '\n')
    print('Вывести сводный отчёт по департаментам:\n'
          'название, численность, "вилка" зарплат в виде мин – макс, среднюю зарплату -', 2, '\n')
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


def struct_depts(features):
    '''
    Формирует структуру департаментов и печатает ее
    '''
    set_depts = set(features['Департамент'])
    set_pairs = set(zip(features['Департамент'], features['Отдел']))
    dict_struct = dict()
    for dept in set_depts:
        print(dept)
        flr = filter(lambda x: x[0] == dept, set_pairs)
        dict_struct[dept] = [item[1] for item in flr]
        [print('    ' + x) for x in dict_struct[dept]]
    return


def struct_salary(features, key):
    '''
    Формирует таблицу сводного отчета по департаментам.+
    Если key = 2, то печатает ее,
    если key = 3, то записывает ее в файл.
    '''
    set_depts = set(features['Департамент'])
    list_pairs = list(zip(features['Департамент'], features['Оклад']))
    dict_struct = dict()
    for dept in set_depts:
        flr = filter(lambda x: x[0] == dept, list_pairs)
        dict_struct[dept] = [item[1] for item in flr]
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
    return


if __name__ == '__main__':
    menu('Corp_Summary.csv')