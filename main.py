# Лабораторная работа по курсу "Техноогии программирования"
# СИБ-501-О, Даргин Егор
# Часть 2

from random import randint, choice
import sys
from PyQt5 import QtCore, QtWidgets, uic
from gui import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.ui_player1_checks.setDisabled(True)
        self.ui.ui_player1_move.setDisabled(True)
        self.ui.ui_player2_checks.setDisabled(True)
        self.ui.ui_player2_move.setDisabled(True)
        self.ui.ui_start.clicked.connect(self.start_game)
        self.ui.ui_player1_move.clicked.connect(self.move_1)
        self.ui.ui_player2_move.clicked.connect(self.move_2)

    def start_game(self):
        try:
            self.game = Game(int(self.ui.ui_check_count.text()))
            self.game.players[0].set_type(self.ui.ui_player1_type.currentIndex())
            self.game.players[1].set_type(self.ui.ui_player2_type.currentIndex())
        except:
            pass
        else:
            self.ui.ui_start.setDisabled(True)
            self.ui.ui_log.append(self.game.start())
            self.ui.ui_log.append(self.ui.ui_player1_type.currentText() + " vs " + self.ui.ui_player2_type.currentText())
            self.ui.ui_check_count.setDisabled(True)
            self.ui.ui_player1_type.setDisabled(True)
            self.ui.ui_player2_type.setDisabled(True)
            self.ui.ui_player1_checks.addItems([str(i) for i in range(1, self.game.checks_count+1)])
            self.ui.ui_player2_checks.addItems([str(i) for i in range(1, self.game.checks_count+1)])
            if self.game.players[0].type == 0:
                self.ui.ui_player1_move.setEnabled(True)
                self.ui.ui_player1_checks.setEnabled(True)
            else:
                self.move_1()

    def move_1(self):
        print (int(self.ui.ui_player1_checks.currentText()))
        self.game.next_turn(0, int(self.ui.ui_player1_checks.currentText()), 1)
        self.ui.ui_player1_checks.removeItem(self.ui.ui_player1_checks.currentIndex())
        self.ui.ui_log.append("Игрок #1: ход фишкой " + str(self.game.temp))
        if len(self.game.players[1].unused()) > 0:
            if self.game.players[1].type == 0:
                self.ui.ui_player2_move.setEnabled(True)
                self.ui.ui_player2_checks.setEnabled(True)
                self.ui.ui_player1_checks.setDisabled(True)
                self.ui.ui_player1_move.setDisabled(True)
            else:
                self.move_2()
        else:
            self.finish()

    def move_2(self):
        self.game.next_turn(1, int(self.ui.ui_player2_checks.currentText()), 0)
        self.ui.ui_log.append("Игрок #2: ход фишкой " + str(self.ui.ui_player2_checks.currentText()))
        self.ui.ui_player2_checks.removeItem(self.ui.ui_player2_checks.currentIndex())
        if len(self.game.players[0].unused()) > 0:
            if self.game.players[0].type == 0:
                self.ui.ui_player1_move.setEnabled(True)
                self.ui.ui_player1_checks.setEnabled(True)
                self.ui.ui_player2_checks.setDisabled(True)
                self.ui.ui_player2_move.setDisabled(True)
            else:
                self.move_1()
        else:
            self.finish()

    def finish(self):
        self.ui.ui_log.append("Игра завершена со счётом " + str(self.game.players[0].score) + " : " +  str(self.game.players[1].score))
        self.ui.ui_player1_checks.setDisabled(True)
        self.ui.ui_player1_move.setDisabled(True)
        self.ui.ui_player2_checks.setDisabled(True)
        self.ui.ui_player2_move.setDisabled(True)
        self.ui.ui_check_count.setEnabled(True)
        self.ui.ui_player1_type.setEnabled(True)
        self.ui.ui_player2_type.setEnabled(True)
        self.ui.ui_start.setEnabled(True)


# Класс игрока
class Player:
    def __init__(self, i):
        # self.name = self.set_name()
        self.type = None
        self.checks = {j+1: True for j in range(i)}
        self.score = 0

    # Сеттер типа
    def set_type(self, t):
        self.type = t

    # Совершить ход
    def use(self, check):
        if self.checks[check]:
            self.checks[check] = False
            return check
        else:
            if self.type == 1:
                print("Такую фишку использовать нельзя!")
            raise ValueError()

    # Оставшиеся фишки
    def unused(self):
        return [i for i in self.checks.keys() if self.checks[i]]


class Game:
    def __init__(self, checks_count):
        self.checks_count = checks_count
        self.temp = 0
        print("Игрок №1")
        self.players = [Player(checks_count), Player(checks_count)]
        print("Игрок №2")

    # ЗАпуск игры
    def start(self):
        return "Игра началась!"

    # Один игровой ход
    def next_turn(self, player, check, opp):
        if self.players[player].type == 0:
            a = check
        elif self.players[player].type == 2 or len(self.players[opp].unused()) == 0:
            a = choice(self.players[player].unused())
        elif len(self.players[0].unused()) == self.checks_count:
            a = randint(1, self.checks_count)  # Первый рандомный ход для компьютера-тактика
        else:
            a = max(self.players[opp].unused())+1
            print("Tactic move" + str(a))
        for i in range(self.checks_count+1):
            try:
                self.players[player].use(a)
                break
            except KeyError:
                a = 1
                continue
            except ValueError:
                a += 1
                continue
        if player == 1:
            if self.temp > a:
                self.players[0].score += (self.temp + a)
                # print(self.player1.name + " получает " + str(a+b) + " очков")
            elif self.temp < a:
                self.players[1].score += (self.temp + a)
                # print(self.player2.name + " получает " + str(a+b) + " очков")
        else:
            self.temp = a
        return True


def main():
    my_app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(my_app.exec_())
    # print("По сколько фишек раздаем?")
    # a = int(input())
    # game = Game(a)
    # game.start()

main()
