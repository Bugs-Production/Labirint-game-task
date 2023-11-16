import random as rnd


# функция чтения лабиринта из файла basic_lab.txt
def load_lab():
    lab = {}
    with open("basic_lab.txt", "r") as f:
        for k in f.__iter__():
            # paramlist - список параметров текущего зала
            paramlist = k.split('\t')
            # извлекаем перечень дверей, преобразуя его в список
            doorlist = []
            for door in paramlist[1].split(','):
                doorlist.append(int(door))
            # формируем словарь, содержащий параметры текущего зала
            hall = {
                'weapon': rnd.randint(1, 3),  # Создаем рандомно какого уровня оружие дать игроку
                'doors': doorlist,
                'name': paramlist[2],
                'coins': int(paramlist[3]),
                'monster': paramlist[4],
                'monstlevel': int(paramlist[5]),
                # с помощью тернарного оператора: если принцесса есть, то True, иначе False
                'princess': True if paramlist[6][0] == '1' else False
            }
            # записываем текущий зал в лабиринт
            lab.update({int(paramlist[0]): hall})
    return lab


# Функция для генерации оружия из файла
def weapon_generate():
    weapon_lst = []
    with open('weapon.txt', 'r') as f:
        for k in f.__iter__():
            if k != '\n':
                weapon_lst.append(k.replace('\n', ''))

    weapon = rnd.choice(weapon_lst)
    return weapon


# функция, описывающая 1 ход игрока
def turn(hall, hallparams, coins, level):
    # прибавляем монеты, лежащие в зале. Потом добавить сюда удаление монет из параметров лабиринта
    coins += hallparams['coins']

    # Текст для каждого раунда
    if hallparams['monstlevel'] != 0:
        print(f'Welcome to {hallparams["name"]}! You got weapon {weapon_generate()}'
              f' of {hallparams["weapon"]} level. You {level} level. Now you got {coins} coins. '
              f'There is a monster of {hallparams["monstlevel"]} level, it"s {hallparams["monster"]}')
    else:
        print(f'Welcome to {hallparams["name"]}! You {level} level. Now you got {coins} coins.')

    # Если оружие есть, прибавить его к уровню игрока
    if 'weapon' in hallparams:
        level += hallparams['weapon']

    # смотрим, есть ли монстр. Сюда потом вставить вызов функции боя
    if hallparams['monstlevel'] != 0:
        print(f"Attention! There is a monster! It is {hallparams['monster']}")
        result_fight = fight_monster(level, hallparams['monstlevel'])
        if result_fight:
            # если лвл игрока больше чем у монстра, то он выигрывает и получает лвл
            level += hallparams['monstlevel']
            print('You win!')
        else:
            # если нет, то умирает и соответственно его уровень падает к 0(смерть)
            print('You dead')
            return False

    # считаем, что монстра победили, смотрим, есть ли принцесса
    if hallparams['princess'] and level != 0:
        return (coins, hallparams['princess'], level)
    # если принцессы нет, смотрим на двери
    print(f"Doors available: {hallparams['doors']}")
    return (coins, hallparams['doors'], hallparams['princess'], level)


# функция проверяющая исход битвы
def fight_monster(player_lvl, monster_lvl):
    if player_lvl > monster_lvl:
        return True
    else:
        return False


coins = 0
level = 1
curhall = 0  # переменная, хранящая номер текущего зала
labirint = load_lab()
halltuple = (0, False)

# главный цикл игры
while True:
    # запрашиваем кортеж результатов прохождения зала
    halltuple = turn(curhall, labirint[curhall], coins, level)

    # остановка игры если функция возвращает false
    if not halltuple:
        break

    # получаем монеты и уровень
    coins = halltuple[0]
    level = halltuple[3]

    # мы выиграли, если нашли принцессу
    if halltuple[2]:
        print(f'You won! The princess is here! Your level is {level}')
        break
    # если принцессы не было, продолжаем игру
    userchoice = int(input('Select a door'))
    # Нужна проверка, есть ли такой зал вообще (проверяем через halltuple[1])
    while userchoice not in halltuple[1]:
        userchoice = int(input('Select a correct door'))

    curhall = userchoice
