# Лабораторная работа по курсу "Техноогии программирования"
# СИБ-501-О, Даргин Егор
# Часть 2

from random import randint, choice


# Класс игрока
class Player:
    def __init__(self, i):
        self.name = self.set_name()
        self.is_user = self.set_type()
        self.checks = {j+1: True for j in range(i)}
        self.score = 0

    # Сеттер имени
    def set_name(self):
        a = ""
        while not 1 < len(a) < 12:
            print("Имя:")
            a = input()
            if 1 < len(a) < 12:
                return a
            else:
                print("Недопустимое кол-во символов!")

    # Сеттер типа
    def set_type(self):
        a = 0
        while a not in ['1', '2']:
            print("Тип (1 -  пользователь, 2 - компьютер):")
            a = input()
        return True if a == '1' else False

    # Совершить ход
    def use(self, check):
        if self.checks[check]:
            self.checks[check] = False
            return check
        else:
            if self.is_user:
                print("Такую фишку использовать нельзя!")
            raise ValueError()

    # Оставшиеся фишки
    def unused(self):
        return [i for i in self.checks.keys() if self.checks[i]]


class Game:
    def __init__(self, checks_count):
        self.checks_count = checks_count
        print("Игрок №1")
        self.player1 = Player(checks_count)
        print("Игрок №2")
        self.player2 = Player(checks_count)

    # ЗАпуск игры
    def start(self):
        for i in range(self.checks_count):
            self.next_turn()
        print("Игра окончена со счётом " + str(self.player1.score) + ":" + str(self.player2.score))

    # Один игровой ход
    def next_turn(self):

        # Ход первого игрока
        if self.player1.is_user:
            a = 0
            print(self.player1.name + " ходит: ")
            while a not in self.player1.unused():
                a = int(input())
        elif len(self.player1.checks) == self.checks_count:
            a = randint(1, self.checks_count)
        else:
            a = max(self.player2.unused())+1
        for i in range(self.checks_count+1):
            try:
                self.player1.use(a)
                print(">> " + self.player1.name + " использует " + str(a) + ", остаток: " + str(self.player1.unused()))
                break
            except KeyError:
                a = 1
                continue
            except ValueError:
                a += 1
                continue

        # Ход второго игрока
        if self.player2.is_user:
            b = 0
            print(self.player2.name + " ходит: ")
            while b not in self.player2.unused():
                b = int(input())
        elif len(self.player1.unused()) == 0:
            b = choice(self.player2.checks)
        else:
            b = max(self.player1.unused())+1
        for i in range(self.checks_count+1):
            try:
                self.player2.use(b)
                print("<< " + self.player2.name + " ходит...")
                break
            except KeyError:
                b = 1
                continue
            except ValueError:
                b += 1
                continue

        # Присвоение очков
        if a > b:
            self.player1.score += (a+b)
            # print(self.player1.name + " получает " + str(a+b) + " очков")
        elif a < b:
            self.player2.score += (a+b)
            # print(self.player2.name + " получает " + str(a+b) + " очков")


def main():
    print("По сколько фишек раздаем?")
    a = int(input())
    game = Game(a)
    game.start()

main()
