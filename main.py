# Лабораторная работа по курсу "Техноогии программирования"
# СИБ-501-О, Даргин Егор
# Часть 1

from random import randint


# Класс игрока
class Player:
    def __init__(self, name):
        self.name = name
        self.checks = [1, 2, 3, 4, 5, 6]
        self.score = 0

    # Совершить ход
    def move(self, check):
        return self.checks.pop(self.checks.index(check))


# Одна игровая сессия
def session():
    print("Welcome, player!\nDo you like games?\nI want to play a game with you...\nEnter your name:")
    player = Player(input())
    ai = Player("AI")
    while len(player.checks)+len(ai.checks) > 0:
        a = 0
        print("Make a turn: ")
        while a == 0:
            try:
                a = player.move(int(input()))
            except :
                print("No such check! Be careful, " + player.name + "...\nTry again: ")
                continue
        b = ai.move(ai.checks[randint(0, len(ai.checks)-1)])
        # print("DEBUG: ai.checks = " + str(ai.checks))
        if a > b:
            player.score += (a+b)
        else:
            ai.score += (a+b)
        print("Good job...\nYour checks: " + str(player.checks))
        # print("DEBUG: score =  " + str(player.score) + ":" + str(ai.score))
    print("Game finished!\nFinal score is " + str(player.score) + ":" + str(ai.score))
    if player.score > ai.score:
        print("Congratulations, " + player.name + "! You won... your freedom.")
    elif ai.score > player.score:
        print("Sorry, my dear... it's time to die...")
    else:
        print("Hmmm... Draw...")


def main():
    c = 0
    while c == 0:
        session()
        print("Enter '0' to retry, any other key to exit...")
        try:
            c = int(input())
        except ValueError:
            break

main()
