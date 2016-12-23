# Лабораторная работа по курсу "Техноогии программирования"
# СИБ-501-О, Даргин Егор
# Часть 2

from random import randint, choice
import sys
import json
import time
from PyQt5.QtWidgets import QMessageBox
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
        self.ui.ui_savestat.setDisabled(True)
        self.ui.ui_savestat.clicked.connect(self.savestat)
        self.ui.ui_showstat.clicked.connect(self.showstat)
        self.stat = {}

    # Начало игры
    def start_game(self):
        m = QMessageBox()
        m.setWindowTitle("Ошибка")
        try:
            self.game = Game(int(self.ui.ui_check_count.text()))
            self.game.players[0].set_type(self.ui.ui_player1_type.currentIndex())
            self.game.players[1].set_type(self.ui.ui_player2_type.currentIndex())
        except ValueError:
            m.setText("Введите число от 2 до 100")
            m.exec()
            return
        else:
            self.ui.ui_start.setDisabled(True)
            self.ui.ui_log.append(self.game.start())
            self.ui.ui_log.append(
                self.ui.ui_player1_type.currentText() + " vs " + self.ui.ui_player2_type.currentText())
            self.ui.ui_check_count.setDisabled(True)
            self.ui.ui_player1_type.setDisabled(True)
            self.ui.ui_player2_type.setDisabled(True)
            self.ui.ui_player1_checks.addItems([str(i) for i in range(1, self.game.checks_count + 1)])
            self.ui.ui_player2_checks.addItems([str(i) for i in range(1, self.game.checks_count + 1)])
            if self.game.players[0].type == 0:
                self.ui.ui_player1_move.setEnabled(True)
                self.ui.ui_player1_checks.setEnabled(True)
            else:
                self.move_1()

    # Ход первого игрока
    def move_1(self):
        print(int(self.ui.ui_player1_checks.currentText()))
        cc = self.game.next_turn(0, int(self.ui.ui_player1_checks.currentText()), 1)
        self.ui.ui_player1_checks.removeItem(self.ui.ui_player1_checks.currentIndex())
        self.ui.ui_log.append("Игрок #1: ход фишкой " + str(cc))
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

    # Ход второго игрока
    def move_2(self):
        cc = self.game.next_turn(1, int(self.ui.ui_player2_checks.currentText()), 0)
        self.ui.ui_log.append("Игрок #2: ход фишкой " + str(cc))
        self.ui.ui_player2_checks.removeItem(self.ui.ui_player2_checks.currentIndex())
        self.ui.ui_log.append("Текущий счёт " + str(self.game.players[0].score) + ":" + str(self.game.players[1].score))
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

    # Окончание партии
    def finish(self):
        self.ui.ui_log.append(
            "Игра завершена со счётом " + str(self.game.players[0].score) + " : " + str(self.game.players[1].score))
        self.ui.ui_player1_checks.setDisabled(True)
        self.ui.ui_player1_move.setDisabled(True)
        self.ui.ui_player2_checks.setDisabled(True)
        self.ui.ui_player2_move.setDisabled(True)
        self.ui.ui_check_count.setEnabled(True)
        self.ui.ui_player1_type.setEnabled(True)
        self.ui.ui_player2_type.setEnabled(True)
        self.ui.ui_start.setEnabled(True)
        self.stat = {
            "id": int(time.time()),
            "player1": self.game.players[0].type,
            "player2": self.game.players[1].type,
            "checks": self.game.checks_count,
            "player1_score": self.game.players[0].score,
            "player2_score": self.game.players[1].score,
        }
        self.ui.ui_savestat.setEnabled(True)

    # Сохранение статистики
    def savestat(self):
        m = QMessageBox()
        m.setWindowTitle(" ")
        m.setText('Статистика сохранена')
        try:
            with open('stats.log', 'r') as f:
                a = json.load(f)
        except FileNotFoundError:
            f = open('stats.log', 'w')
            a = [self.stat]
            json.dump(a, f, indent='\n', ensure_ascii=False)
            m.exec()
            return
        a.append(self.stat)
        with open('stats.log', 'w') as f:
            json.dump(a, f, indent='\n', ensure_ascii=False)
            f.close()
            m.exec()
        self.ui.ui_savestat.setDisabled(True)

    # Отображение статистики
    def showstat(self):
        m = QMessageBox()
        m.setWindowTitle(" ")
        try:
            with open('stats.log', 'r') as f:
                a = json.load(f)
        except FileNotFoundError:
            m.setText('Статистика пуста')
            m.exec()
            return
        wins = self.winsstat(a)
        scores = self.scorestat(a)
        t = "Игр сохранено: " + str(len(a)) + "\n"
        t += str(wins[0]) + " человеческих побед\n"
        t += str(wins[1]) + " побед генератора\n"
        t += str(wins[2]) + " побед тактика\n"
        t += str(scores[0] + " очков у человеков\n")
        t += str(scores[1] + " очков у генератора\n")
        t += str(scores[2] + " очков у тактика\n")
        m.setText(t)
        m.exec()

    # Проценты побед
    def winsstat(self, a):
        b = [0, 0, 0]
        с = [0, 0, 0]
        for i in a:
            if i["player1_score"] > i["player2_score"]:
                b[i["player1"]] += 1
            elif i["player1_score"] < i["player2_score"]:
                b[i["player2"]] += 1
        return [str(i / len(a) * 100)[0:4] + "%" for i in b]

    # Проценты очков
    def scorestat(self, a):
        score_total = 0
        scores = [0, 0, 0]
        for i in a:
            score_total += sum(range(1, i["checks"]+1))*2
            scores[i["player1"]] += i["player1_score"]
            scores[i["player2"]] += i["player2_score"]
        return [str(i / score_total * 100)[0:4] + "%" for i in scores]


# Класс игрока
class Player:
    def __init__(self, i):
        # self.name = self.set_name()
        self.type = None
        self.checks = {j + 1: True for j in range(i)}
        self.score = 0

    # Сеттер типа
    def set_type(self, t):
        self.type = t

    # Использовать фишку
    def use(self, check):
        if self.checks[check]:
            self.checks[check] = False
            return check
        else:
            raise ValueError()

    # Оставшиеся фишки
    def unused(self):
        return [i for i in self.checks.keys() if self.checks[i]]


# Игра
class Game:
    def __init__(self, checks_count):
        if 2 <= checks_count <= 100:
            self.checks_count = checks_count
        else:
            raise ValueError()
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
            a = max(self.players[opp].unused()) + 1
            print("Tactic move" + str(a))
        for i in range(self.checks_count + 1):
            try:
                self.players[player].use(a)
                if player == 0:
                    self.temp = a
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
        # else:
        #     self.temp = a
        #     print("DNIWE: " + str(self.temp))
        return a


def main():
    my_app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(my_app.exec_())
main()
