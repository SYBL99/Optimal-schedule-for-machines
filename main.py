import copy
import plotly.figure_factory as ff
from datetime import date, timedelta, datetime


def data_to_order(order):
    buff = [[0] * len(data[0]) for _ in range(len(data))]
    for i in range(len(order)):
        order[i] -= 1
    for i in range(len(data[0])):
        for j in range(len(data)):
            buff[j][i] = data[j][order[i]]
    return buff


def gantt_draw(order):
    data_temp = data_to_order(order)
    df = []
    for j in range(len(data[0])):
        for i in range(len(data)):
            if j == 0:
                if i == 0:
                    df.append(dict(Task='Станок ' + str(i + 1), Start=str(date.today()), Finish=str(date.today() + timedelta(days=data_temp[i][j])), Resource='Деталь ' + str(order[j] + 1)))
                else:
                    df.append(dict(Task='Станок ' + str(i + 1), Start=df[len(df)-1]['Finish'], Finish=str(datetime.strptime(df[len(df)-1]['Finish'],'%Y-%m-%d').date() + timedelta(days=data_temp[i][j])), Resource='Деталь ' + str(order[j] + 1)))
            else:
                if i == 0:
                    df.append(dict(Task='Станок ' + str(i + 1), Start=df[len(df)-len(data)]['Finish'], Finish=str(datetime.strptime(df[len(df)-len(data)]['Finish'],'%Y-%m-%d').date() + timedelta(days=data_temp[i][j])), Resource='Деталь ' + str(order[j] + 1)))
                else:
                    df.append(dict(Task='Станок ' + str(i + 1), Start=max(df[len(df)-1]['Finish'], df[len(df)-len(data)]['Finish']),
                                   Finish=str(datetime.strptime(max(df[len(df)-1]['Finish'], df[len(df)-len(data)]['Finish']),'%Y-%m-%d').date() + timedelta(days=data_temp[i][j])), Resource='Деталь ' + str(order[j] + 1)))
    fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True, group_tasks=True, title='Диаграмма Ганта для очереди '+str(order))
    fig.show()


def read_from_file():
    with open('data.txt', 'r') as file:
        for line in file:
            data.append(list(map(int, line.split())))
    order = [i + 1 for i in range(len(data[0]))]
    gantt_draw(order)


def print_matrix():
    for row in data:
        for x in row:
            print("{:3d}".format(x), end="")
        print()


def petrov_sokol():
    rez = []
    sum1_mass = []
    sum2_mass = []
    for i in range(len(data[0])):
        sum1 = 0
        sum2 = 0
        for j in range(len(data)):
            if (j != 0):
                sum1 += data[j][i]
            if (j != len(data) - 1):
                sum2 += data[j][i]
        sum1_mass.append(sum1)
        sum2_mass.append(sum2)
    sum3_mass = [sum1_mass[i] - sum2_mass[i] for i in range(len(sum1_mass))]
    duration = []
    data_temp = []
    sum1_mass_s = sorted(sum1_mass, reverse=True)
    rng1 = []
    for i in range(len(sum1_mass_s)):
        if sum1_mass.index(sum1_mass_s[i]) not in rng1:
            rng1.append(sum1_mass.index(sum1_mass_s[i]))
        else:
            rng1.append(sum1_mass.index(sum1_mass_s[i], sum1_mass.index(sum1_mass_s[i]) + 1))
    for i in range(len(data)):
        buff = []
        for j in rng1:
            buff.append(data[i][j])
        data_temp.append(buff)
    for i in range(len(data_temp)):
        buff = []
        for j in range(len(data_temp[0])):
            if i == 0 and j == 0:
                buff.append(data_temp[i][j])
            if i == 0 and j != 0:
                buff.append(data_temp[i][j] + buff[len(buff) - 1])
            if i != 0 and j == 0:
                buff.append(duration[i-1][j] + data_temp[i][j])
            if i != 0 and j != 0:
                buff.append(max(duration[i-1][j], buff[len(buff) - 1]) + data_temp[i][j])
        duration.append(buff)
    print('Длинна по 1ому критерию', max(duration[len(duration) - 1]))
    rez.append(max(duration[len(duration) - 1]))
    duration = []
    data_temp = []
    sum2_mass_s = sorted(sum2_mass)
    rng2 = []
    for i in range(len(sum2_mass_s)):
        if sum2_mass.index(sum2_mass_s[i]) not in rng2:
            rng2.append(sum2_mass.index(sum2_mass_s[i]))
        else:
            rng2.append(sum2_mass.index(sum2_mass_s[i], sum2_mass.index(sum2_mass_s[i]) + 1))
    for i in range(len(data)):
        buff = []
        for j in rng2:
            buff.append(data[i][j])
        data_temp.append(buff)
    for i in range(len(data_temp)):
        buff = []
        for j in range(len(data_temp[0])):
            if i == 0 and j == 0:
                buff.append(data_temp[i][j])
            if i == 0 and j != 0:
                buff.append(data_temp[i][j] + buff[len(buff) - 1])
            if i != 0 and j == 0:
                buff.append(duration[i-1][j] + data_temp[i][j])
            if i != 0 and j != 0:
                buff.append(max(duration[i-1][j], buff[len(buff) - 1]) + data_temp[i][j])
        duration.append(buff)
    print('Длинна по 2ому критерию', max(duration[len(duration) - 1]))
    rez.append(max(duration[len(duration) - 1]))
    duration = []
    data_temp = []
    sum3_mass_s = sorted(sum3_mass, reverse=True)
    rng3 = []
    for i in range(len(sum3_mass_s)):
        if sum3_mass.index(sum3_mass_s[i]) not in rng3:
            rng3.append(sum3_mass.index(sum3_mass_s[i]))
        else:
            rng3.append(sum3_mass.index(sum3_mass_s[i], sum3_mass.index(sum3_mass_s[i]) + 1))
    for i in range(len(data)):
        buff = []
        for j in rng3:
            buff.append(data[i][j])
        data_temp.append(buff)
    for i in range(len(data_temp)):
        buff = []
        for j in range(len(data_temp[0])):
            if i == 0 and j == 0:
                buff.append(data_temp[i][j])
            if i == 0 and j != 0:
                buff.append(data_temp[i][j] + buff[len(buff) - 1])
            if i != 0 and j == 0:
                buff.append(duration[i-1][j] + data_temp[i][j])
            if i != 0 and j != 0:
                buff.append(max(duration[i-1][j], buff[len(buff) - 1]) + data_temp[i][j])
        duration.append(buff)
    print('Длинна по 3ему критерию', max(duration[len(duration) - 1]))
    rez.append(max(duration[len(duration) - 1]))
    rng = [rng1, rng2, rng3]
    test = rng[rez.index(min(rez))]
    for i in range(len(test)):
        test[i] += 1
    print('Оптимальный порядок', rng[rez.index(min(rez))], 'с длинной', min(rez))
    gantt_draw(test)


def johnson_for_n():
    cr1_mass = data[0][::]
    cr1_mass_s = sorted(data[0])
    cr1 = []
    for i in range(len(cr1_mass_s)):
        cr1.append(cr1_mass.index(cr1_mass_s[i]))
        cr1_mass[cr1_mass.index(cr1_mass_s[i])] = None
    cr2 = []
    cr2_mass = data[len(data) - 1][::]
    cr2_mass_s = sorted(data[len(data) - 1], reverse=True)
    for i in range(len(cr2_mass_s)):
        cr2.append(cr2_mass.index(cr2_mass_s[i]))
        cr2_mass[cr2_mass.index(cr2_mass_s[i])] = None
    cr3 = []
    pair = []
    for i in range(len(data[0])):
        buff = []
        for j in range(len(data)):
            buff.append(data[j][i])
        pair.append([buff.index(max(buff)), max(buff)])
    for i in range(len(data)):
        for j in range(len(pair)):
            if pair[j][0] == len(data) - i - 1:
                cr3.append(j)
    sum_mass = [0] * len(data[0])
    for i in range(len(data[0])):
        colom_sum = 0
        for j in range(len(data)):
            colom_sum += data[j][i]
        sum_mass[i] = colom_sum
    sum4_mass_s = sorted(sum_mass, reverse=True)
    cr4 = []
    for i in range(len(sum4_mass_s)):
        if sum_mass.index(sum4_mass_s[i]) not in cr4:
            cr4.append(sum_mass.index(sum4_mass_s[i]))
        else:
            cr4.append(sum_mass.index(sum4_mass_s[i], sum_mass.index(sum4_mass_s[i]) + 1))
    sum_cr = [(cr1[i]+cr2[i]+cr3[i]+cr4[i]) for i in range(len(data[0]))]
    sum_cr_s = sorted(sum_cr)
    med_cr = []
    for i in range(len(sum_cr_s)):
        if sum_cr.index(sum_cr_s[i]) not in med_cr:
            med_cr.append(sum_cr.index(sum_cr_s[i]))
            sum_cr[sum_cr.index(sum_cr_s[i])] = None
    for i in range(len(med_cr)):
        med_cr[i] += 1
    print('Оптимальный порядок', med_cr)
    gantt_draw(med_cr)


def johnson_for_two():
    end = ''
    start = ''
    buff = copy.deepcopy(data)
    while len(buff[0]) > 1:
        if min(buff[0] + buff[1]) in buff[1] and len(buff[0]) > 1:
            ind = buff[1].index(min(buff[1]))
            end = str(data[1].index(min(buff[1])) + 1) + end
            del (buff[0][ind])
            del (buff[1][ind])
            print(buff)
        if min(buff[0] + buff[1]) in buff[0] and len(buff[0]) > 1:
            ind = buff[0].index(min(buff[0]))
            start = start + str(data[0].index(min(buff[0])) + 1)
            del (buff[0][ind])
            del (buff[1][ind])
            print(buff)
    else:
        mid = str(data[0].index(min(buff[0])) + 1)
    ord = []
    for i in start + mid + end:
        ord.append(int(i))
    print(ord)
    gantt_draw(ord)


def exit():
    global work
    work = False


data = []
switch = {1: read_from_file,
          2: print_matrix,
          3: johnson_for_two,
          4: johnson_for_n,
          5: petrov_sokol,
          0: exit}
work = True
while work:
    print('0.Выход' + '\n' + '1.Считать из файла' + '\n' '2.Вывести матрицу' +
          '\n' '3.Джонсон для 2ух' + '\n' '4.Джонсон для n' + '\n' '5.Петров-Соколицин')
    choice = int(input())
    switch[choice]()
